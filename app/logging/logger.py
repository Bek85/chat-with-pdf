import logging
import os
from typing import Optional
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output"""

    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    BOLD = '\033[1m'

    def format(self, record):
        # Get the original formatted message
        original_format = super().format(record)

        # Get color for log level
        color = self.COLORS.get(record.levelname, '')

        if color:
            # Make the level name bold and colored
            level_name = f"{self.BOLD}{color}{record.levelname}{self.RESET}"
            # Replace the level name in the formatted message
            colored_format = original_format.replace(record.levelname, level_name)

            # Also color the logger name (module path)
            if hasattr(record, 'name') and record.name:
                colored_name = f"{color}{record.name}{self.RESET}"
                colored_format = colored_format.replace(record.name, colored_name)

            return colored_format

        return original_format

class LoggerConfig:
    """Configuration class for logging settings"""

    def __init__(self):
        self.level = os.getenv("LOG_LEVEL", "INFO").upper()
        self.format = os.getenv(
            "LOG_FORMAT",
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.date_format = os.getenv("LOG_DATE_FORMAT", "%Y-%m-%d %H:%M:%S")
        self.file_enabled = os.getenv("LOG_FILE_ENABLED", "false").lower() == "true"
        self.file_path = os.getenv("LOG_FILE_PATH", "logs/app.log")
        self.file_max_bytes = int(os.getenv("LOG_FILE_MAX_BYTES", "10485760"))  # 10MB
        self.file_backup_count = int(os.getenv("LOG_FILE_BACKUP_COUNT", "5"))
        self.console_enabled = os.getenv("LOG_CONSOLE_ENABLED", "true").lower() == "true"
        self.console_colored = os.getenv("LOG_CONSOLE_COLORED", "true").lower() == "true"

_config = LoggerConfig()
_configured = False

def configure_logging(config: Optional[LoggerConfig] = None) -> None:
    """
    Configure the root logger with the specified configuration.

    Args:
        config: Optional LoggerConfig instance. If None, uses default configuration.
    """
    global _configured, _config

    if config:
        _config = config

    if _configured:
        return

    # Fix Windows encoding issues by forcing UTF-8 for all stream outputs
    import sys
    import io
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, _config.level))

    # Clear any existing handlers
    root_logger.handlers.clear()

    # Create formatters
    file_formatter = logging.Formatter(
        fmt=_config.format,
        datefmt=_config.date_format
    )

    # Console handler
    if _config.console_enabled:
        console_handler = logging.StreamHandler()

        # Use colored formatter for console if enabled
        if _config.console_colored:
            console_formatter = ColoredFormatter(
                fmt=_config.format,
                datefmt=_config.date_format
            )
            console_handler.setFormatter(console_formatter)
        else:
            console_handler.setFormatter(file_formatter)

        root_logger.addHandler(console_handler)

    # File handler
    if _config.file_enabled:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(_config.file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        file_handler = RotatingFileHandler(
            _config.file_path,
            maxBytes=_config.file_max_bytes,
            backupCount=_config.file_backup_count
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    _configured = True

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name: The name of the logger (typically __name__)

    Returns:
        A configured logger instance
    """
    # Ensure logging is configured
    if not _configured:
        configure_logging()

    return logging.getLogger(name)

def get_module_logger(module_name: str) -> logging.Logger:
    """
    Get a logger for a specific module with standardized naming.

    Args:
        module_name: The module name (e.g., 'web.api', 'chat.vector_stores')

    Returns:
        A configured logger instance with app.{module_name} naming
    """
    logger_name = f"app.{module_name}"
    return get_logger(logger_name)