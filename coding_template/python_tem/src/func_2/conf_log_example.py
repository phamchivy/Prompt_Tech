"""
Document Converter Service
"""

import yaml
from pathlib import Path
from typing import Tuple, List, Dict
# REMOVE: import logging

# ADD: Use centralized logger
from log_service.logger import get_logger

# ... other imports ...

from config import get_project_root, load_config

root = get_project_root()
# Done! No Path().parent.parent

class DocumentConverter:
    """Converts document files to Markdown"""
    
    def __init__(self, config_path: str = None):
        """Initialize converter with configuration"""
        if config_path is None:
            config_path = root / "config" / "preprocessing_rules.yaml"
        
        self.config = load_config(str(config_path))
        
        # REPLACE setup_logging() with get_logger()
        self.logger = get_logger(__name__)
        
        self.input_base = Path(self.config['documents']['input_base'])
        self.output_base = Path(self.config['documents']['output_base'])
        # ... rest of init
    
    # REMOVE setup_logging() method entirely
    # def setup_logging(self):
    #     """Setup logging configuration"""
    #     ...
    
    # ... rest of class methods unchanged