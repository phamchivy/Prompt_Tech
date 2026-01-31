"""
Centralized Logger Module
Provides unified logging configuration for all services
"""

import logging
import logging.config
import yaml
from pathlib import Path
from typing import Optional


class LoggerManager:
    """
    Singleton manager for logging configuration
    """
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not LoggerManager._initialized:
            self.config_path = None
            self.log_dir = None
            LoggerManager._initialized = True
    
    def setup(self, config_path: Optional[str] = None):
        """
        Setup logging configuration from YAML file
        
        Args:
            config_path: Path to logging_config.yaml
        """
        if config_path is None:
            # Default: config/logging_config.yaml
            base_dir = Path(__file__).parent.parent
            config_path = base_dir / "config" / "logging_config.yaml"
        
        self.config_path = Path(config_path)
        
        # Create log directory if not exists
        self.log_dir = Path(__file__).parent / "log_files"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        if not self.config_path.exists():
            raise FileNotFoundError(f"Logging config not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Apply configuration
        logging.config.dictConfig(config)
        
        # Log initialization
        root_logger = logging.getLogger()
        root_logger.info("=" * 60)
        root_logger.info("Logging system initialized")
        root_logger.info(f"Config: {self.config_path}")
        root_logger.info(f"Log directory: {self.log_dir}")
        root_logger.info("=" * 60)
    
    def get_logger(self, name: str) -> logging.Logger:
        """
        Get logger instance for a module
        
        Args:
            name: Logger name (usually __name__)
        
        Returns:
            Logger instance
        """
        return logging.getLogger(name)


# Singleton instance
_manager = LoggerManager()


def setup_logging(config_path: Optional[str] = None):
    """
    Initialize logging system (call once at application start)
    
    Args:
        config_path: Optional path to logging_config.yaml
    """
    _manager.setup(config_path)


def get_logger(name: str) -> logging.Logger:
    """
    Get logger for a module
    
    Args:
        name: Module name (use __name__)
    
    Returns:
        Logger instance
    
    Example:
        >>> from logging.logger import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing started")
    """
    return _manager.get_logger(name)


# Convenience function for getting class-specific logger
def get_class_logger(cls) -> logging.Logger:
    """
    Get logger for a class
    
    Args:
        cls: Class object
    
    Returns:
        Logger instance
    
    Example:
        >>> class MyService:
        >>>     def __init__(self):
        >>>         self.logger = get_class_logger(self.__class__)
    """
    module = cls.__module__
    class_name = cls.__name__
    return logging.getLogger(f"{module}.{class_name}")