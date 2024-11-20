import logging
import sys

from rich import pretty
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme
from rich.traceback import install

# Install rich traceback handler for better error visibility
install(show_locals=True)

# Enable rich pretty printing for data structures
pretty.install()

# Custom theme for logging output
custom_theme = Theme({
    "debug": "#005fff",
    "info": "#00d7af",
    "warning": "#d7d700",
    "error": "#ff005f",
    "critical": "#ff005f on #d7d7ff",
})

# Custom log level configuration using RichHandler's built-in styling options
class CustomRichHandler(RichHandler):
    LEVEL_STYLES = {
        logging.DEBUG: "#005fff",
        logging.INFO: "#00d7af",
        logging.WARNING: "#d7d700",
        logging.ERROR: "#ff005f",
        logging.CRITICAL: "#ff005f on #d7d7ff",
    }

    def __init__(self, console=None, *args, **kwargs):
        console = Console(theme=custom_theme, log_path=False, file=sys.stdout, soft_wrap=True)
        super().__init__(console=console, *args, **kwargs)

# Global Logger Module
def setup_global_logger(name: str = __name__, level: int = logging.DEBUG) -> logging.Logger:
    """
    Sets up a global logger using the CustomRichHandler.

    Args:
        name (str): The name of the logger. Defaults to the current module's name.
        level (int): The logging level. Defaults to DEBUG.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger("rich")
    logger.setLevel(level)

    # Avoid adding duplicate handlers
    if not logger.hasHandlers():
        console = Console(theme=custom_theme, log_path=False, file=sys.stdout, soft_wrap=True)
        logging.basicConfig(
        handlers = [RichHandler(console=console, show_time=False, show_path=True)],
        )
    return logger

# Exported instance of the global logger to be used across the project
logger = setup_global_logger("project_logger")

logger.info("Global logger initialized successfully.")

