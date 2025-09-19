"""
Logging configuration presets for different environments.
These can be used to quickly configure logging for development, testing, and production.
"""

from .logger import LoggerConfig

class DevelopmentConfig(LoggerConfig):
    """Development logging configuration"""

    def __init__(self):
        super().__init__()
        self.level = "DEBUG"
        self.console_enabled = True
        self.console_colored = True
        self.file_enabled = True
        self.file_path = "logs/dev.log"

class ProductionConfig(LoggerConfig):
    """Production logging configuration"""

    def __init__(self):
        super().__init__()
        self.level = "WARNING"
        self.console_enabled = True
        self.console_colored = True
        self.file_enabled = True
        self.file_path = "logs/prod.log"
        self.file_max_bytes = 52428800  # 50MB
        self.file_backup_count = 10

class TestingConfig(LoggerConfig):
    """Testing logging configuration"""

    def __init__(self):
        super().__init__()
        self.level = "ERROR"
        self.console_enabled = False
        self.console_colored = False
        self.file_enabled = False

# Configuration mapping
CONFIGS = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}