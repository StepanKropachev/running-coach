import logging
import os
from pathlib import Path


def setup_logging(debug: bool = False) -> None:
    """Configure logging for the application."""
    # Create logs directory in user's home
    log_dir = Path.home() / ".running_coach" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "running_coach.log"

    # Set up basic configuration
    level = logging.DEBUG if debug else logging.INFO
    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),  # Also log to console
        ],
    )

    # Create logger for the package
    logger = logging.getLogger("running_coach")
    logger.setLevel(level)

    # Log startup message
    logger.info("Logging initialized")
