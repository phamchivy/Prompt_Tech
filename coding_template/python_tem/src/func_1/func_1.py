"""
Document Converter Service
Converts .doc and .docx files to Markdown format

Comment chức năng của files ở đây
Mỗi hàm, mỗi class đều có comment ngắn gọn mô tả chức năng

"""

import yaml
from pathlib import Path
from typing import Tuple, List, Dict
import logging

# For .docx files
from docx import Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import Table
from docx.text.paragraph import Paragraph

# For .doc files (older format)
import subprocess
import tempfile
import platform

# For image extraction
from docx.document import Document as DocumentType
from docx.parts.image import ImagePart
import base64


class DocumentConverter:
    """
    Converts document files (.doc, .docx) to Markdown
    Extracts embedded images and saves them separately
    """
    
    def __init__(self, config_path: str = "config/preprocessing_rules.yaml"):
        """Initialize converter with configuration"""
        self.config = self._load_config(config_path)
        self.setup_logging()
        
        self.input_base = Path(self.config['documents']['input_base'])
        self.output_base = Path(self.config['documents']['output_base'])
        self.folders = self.config['documents']['folders']
        self.supported_formats = self.config['documents']['supported_formats']
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_config = self.config['logging']
        log_file = Path(log_config['log_file'])
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, log_config['level']),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def convert_all(self) -> Dict[str, int]:
        """
        Convert all documents in configured folders
        Returns: Dictionary with conversion statistics
        """
        stats = {'success': 0, 'failed': 0, 'skipped': 0}
        
        for folder in self.folders:
            folder_path = self.input_base / folder
            
            if not folder_path.exists():
                self.logger.warning(f"Folder not found: {folder_path}")
                continue
            
            self.logger.info(f"Processing folder: {folder}")
            
            # Process all supported document files
            for ext in self.supported_formats:
                for doc_file in folder_path.glob(f"*{ext}"):
                    try:
                        self.logger.info(f"Converting: {doc_file.name}")
                        self.convert_file(doc_file, folder)
                        stats['success'] += 1
                    except Exception as e:
                        self.logger.error(f"Failed to convert {doc_file.name}: {str(e)}")
                        stats['failed'] += 1
        
        self.logger.info(f"Conversion complete. Stats: {stats}")
        return stats
    
    def convert_file(self, input_path: Path, folder_name: str) -> Tuple[str, List[Path]]:
        """
        Convert a single document file to Markdown
        
        Args:
            input_path: Path to input document
            folder_name: Folder name (DB or HLD)
        
        Returns:
            Tuple of (markdown_content, list_of_image_paths)
        """
        # Handle .doc vs .docx
        if input_path.suffix == '.doc':
            return self._convert_doc(input_path, folder_name)
        elif input_path.suffix == '.docx':
            return self._convert_docx(input_path, folder_name)
        else:
            raise ValueError(f"Unsupported format: {input_path.suffix}")
    
    def _convert_docx(self, input_path: Path, folder_name: str) -> Tuple[str, List[Path]]:
        """
        Convert .docx to Markdown with image extraction
        """
        doc = Document(input_path)
        
        # Setup output paths
        output_dir = self.output_base / folder_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        images_dir = output_dir / self.config['documents']['image_extraction']['output_folder']
        images_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract images
        image_paths = []
        if self.config['documents']['image_extraction']['enabled']:
            image_paths = self._extract_images_from_docx(doc, images_dir, input_path.stem)
        
        # Convert content to Markdown
        markdown_content = self._docx_to_markdown(doc, image_paths, folder_name)
        
        # Write output
        output_file = output_dir / f"{input_path.stem}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        self.logger.info(f"Converted {input_path.name} -> {output_file}")
        
        return markdown_content, image_paths
    
    def _convert_doc(self, input_path: Path, folder_name: str) -> Tuple[str, List[Path]]:
        """
        Convert .doc (old format) to Markdown
        Uses LibreOffice/unoconv to convert .doc -> .docx first
        """
        self.logger.info(f"Converting old .doc format: {input_path.name}")
        
        # Create temporary docx file
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
            tmp_docx = Path(tmp.name)
        
        try:
            # Convert .doc to .docx using LibreOffice
            self._doc_to_docx(input_path, tmp_docx)
            
            # Now convert the .docx
            return self._convert_docx(tmp_docx, folder_name)
        
        finally:
            # Cleanup temp file
            if tmp_docx.exists():
                tmp_docx.unlink()
    
    def _doc_to_docx(self, doc_path: Path, output_path: Path):
        """
        Convert .doc to .docx using LibreOffice
        Requires LibreOffice to be installed
        """
        system = platform.system()
        
        if system == "Windows":
            soffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
        elif system == "Darwin":  # macOS
            soffice_path = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
        else:  # Linux
            soffice_path = "soffice"
        
        cmd = [
            soffice_path,
            '--headless',
            '--convert-to', 'docx',
            '--outdir', str(output_path.parent),
            str(doc_path)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            # Rename output to expected name
            converted = output_path.parent / f"{doc_path.stem}.docx"
            if converted.exists() and converted != output_path:
                converted.rename(output_path)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"LibreOffice conversion failed: {e.stderr.decode()}")
        except FileNotFoundError:
            raise RuntimeError("LibreOffice not found. Please install LibreOffice for .doc support")
    
    def _extract_images_from_docx(self, doc: DocumentType, images_dir: Path, base_name: str) -> List[Path]:
        """
        Extract all images from docx file
        Returns list of saved image paths
        """
        image_paths = []
        image_counter = 1
        
        # Iterate through all parts to find images
        for rel in doc.part.rels.values():
            if isinstance(rel.target_part, ImagePart):
                image_part = rel.target_part
                
                # Get image extension
                ext = image_part.content_type.split('/')[-1]
                if ext == 'jpeg':
                    ext = 'jpg'
                
                # Generate filename
                image_filename = f"{base_name}_img_{image_counter:03d}.{ext}"
                image_path = images_dir / image_filename
                
                # Save image
                with open(image_path, 'wb') as f:
                    f.write(image_part.blob)
                
                image_paths.append(image_path)
                image_counter += 1
                
                self.logger.debug(f"Extracted image: {image_filename}")
        
        return image_paths
    
    def _docx_to_markdown(self, doc: DocumentType, image_paths: List[Path], folder_name: str) -> str:
        """
        Convert docx content to Markdown format
        """
        markdown_lines = []
        image_index = 0
        
        # Add document title
        markdown_lines.append(f"# {doc.core_properties.title or 'Document'}\n")
        
        for element in doc.element.body:
            if isinstance(element, CT_P):
                para = Paragraph(element, doc)
                para_text = para.text.strip()
                
                if not para_text:
                    markdown_lines.append("")
                    continue
                
                # Handle headings
                if para.style.name.startswith('Heading'):
                    level = int(para.style.name.split()[-1])
                    markdown_lines.append(f"{'#' * level} {para_text}\n")
                
                # Handle list items
                elif para.style.name.startswith('List'):
                    markdown_lines.append(f"- {para_text}")
                
                # Regular paragraph
                else:
                    markdown_lines.append(f"{para_text}\n")
            
            elif isinstance(element, CT_Tbl):
                table = Table(element, doc)
                markdown_lines.append(self._table_to_markdown(table))
                markdown_lines.append("")
        
        # Add image references at the end
        if image_paths:
            markdown_lines.append("\n## Images\n")
            for i, img_path in enumerate(image_paths, 1):
                rel_path = f"images/{img_path.name}"
                markdown_lines.append(f"![Image {i}]({rel_path})\n")
        
        return "\n".join(markdown_lines)
    
    def _table_to_markdown(self, table: Table) -> str:
        """Convert docx table to Markdown table"""
        lines = []
        
        for i, row in enumerate(table.rows):
            cells = [cell.text.strip() for cell in row.cells]
            lines.append("| " + " | ".join(cells) + " |")
            
            # Add header separator after first row
            if i == 0:
                lines.append("| " + " | ".join(["---"] * len(cells)) + " |")
        
        return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    converter = DocumentConverter()
    stats = converter.convert_all()
    print(f"Conversion complete: {stats}")