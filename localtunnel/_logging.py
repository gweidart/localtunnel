# localtunnel/ _logging.py
from pathlib import Path
import sys

from loguru import logger

# Define log directory and file
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "localtunnel.log"

# Define custom colors and icons for each log level
LOG_LEVEL_STYLES = {
    "DEBUG": {"color": "<dim><blue>", "icon": "🐞 "},
    "INFO": {"color": "<green>", "icon": "ℹ️"},
    "WARNING": {"color": "<bold><yellow>", "icon": "⚠️"},
    "ERROR": {"color": "<bold><red>", "icon": "❌ "},
    "CRITICAL": {"color": "<underline><bg_red><bright_white>", "icon": "🔥 "},
}


# Define a custom format function for log messages
def custom_format(record):
    # Extract log level and message
    level = record["level"].name
    message = record["message"]

    # Apply custom styling for each log level
    style = LOG_LEVEL_STYLES.get(level, {})
    color = style.get("color", "")
    icon = style.get("icon", "")

    # Construct the formatted log line
    formatted_message = (
        f"{color}{icon} {level:<8}</color> | "
        f"<bright_white>{record['name']}</bright_white>:<bright_blue>{record['function']}</bright_blue>:<magenta>{record['line']}</magenta> - "
        f"{color}{message}</color>"
    )
    return formatted_message


# Configure the global logger
def configure_logger():
    logger.remove()  # Remove default handler to prevent duplicates

    # Console (stdout) handler
    logger.add(
        sys.stdout,
        format=custom_format,  # Use the custom format function
        level="DEBUG",  # Adjust the minimum log level for console
        colorize=True,
        enqueue=True,
    )

    # File handler for persistent logs (without colors for simplicity)
    logger.add(
        LOG_FILE,
        format=("{time:HH:mm} | {level: <8} | {name}:{function}:{line} - {message}"),
        level="DEBUG",
        rotation="10 MB",  # Rotate log files when they reach 10 MB
        retention="30 days",  # Retain log files for 30 days
        compression="zip",  # Compress old log files
        enqueue=True,
    )

    # Return the global logger instance
    return logger


def handle_exception(exc_type, exc_value, exc_traceback):
    """Custom handler for unhandled exceptions."""
    if issubclass(exc_type, KeyboardInterrupt):
        # Allow Ctrl+C to exit cleanly
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.opt(exception=(exc_type, exc_value, exc_traceback)).critical(
        "Unhandled exception occurred!"
    )


# Register the custom exception handler
sys.excepthook = handle_exception

# Expose logger as a module-level attribute
configure_logger()
