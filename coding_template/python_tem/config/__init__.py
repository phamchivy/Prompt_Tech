from pathlib import Path
import yaml

# Project root - calculated once
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

def get_project_root():
    """Get absolute project root path"""
    return PROJECT_ROOT

def load_config(config_name):
    config_path = PROJECT_ROOT / "config" / f"{config_name}.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)