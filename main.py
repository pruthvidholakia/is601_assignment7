#!/usr/bin/env python3
"""
simple_qr.py
Light-weight QR-code generator that:
1. Loads optional settings from .env
2. Logs actions to the console
3. Validates the URL
4. Saves the PNG in ./qr_codes/ with a timestamped filename
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import qrcode
import validators
from dotenv import load_dotenv

# --------------------------------------------------------------------------- 
#  Load environment variables (.env is optional)                              
# --------------------------------------------------------------------------- 
load_dotenv()

# Directory & color defaults can be overridden via environment variables
QR_DIRECTORY = os.getenv("QR_CODE_DIR", "qr_codes")
FILL_COLOR   = os.getenv("FILL_COLOR", "red")
BACK_COLOR   = os.getenv("BACK_COLOR", "white")


# --------------------------------------------------------------------------- 
#  Helper functions                                                           
# --------------------------------------------------------------------------- 
def setup_logging() -> None:
    """Configure the root logger with a simple timestamped format."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def create_directory(path: Path) -> None:
    """Ensure *path* exists, creating parent directories as needed."""
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        logging.error("Cannot create directory %s: %s", path, exc)
        sys.exit(1)


def is_valid_url(url: str) -> bool:
    """Return True if *url* is plausibly valid."""
    return validators.url(url)


def generate_qr_code(
    data: str,
    path: Path,
    fill_color: str = "red",
    back_color: str = "white",
) -> None:
    """
    Create a QR code from *data* and save it to *path*.
    """
    if not is_valid_url(data):
        logging.error("Invalid URL provided: %s", data)
        sys.exit(1)

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save(path)
    logging.info("QR code saved to %s", path.resolve())


# --------------------------------------------------------------------------- 
#  Main entry-point                                                           
# ---------------------------------------------------------------------------
def main() -> None:
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Generate a QR code.")
    parser.add_argument(
        "--url",
        help="The URL to encode in the QR code",
        default="https://github.com/pruthvidholakia",
    )
    args = parser.parse_args()

    # Initial logging setup
    setup_logging()

    # Generate a timestamped filename for the QR code
    timestamp   = datetime.now().strftime("%Y%m%d%H%M%S")
    qr_filename = f"QRCode_{timestamp}.png"

    # Create the full path for the QR code file
    qr_code_full_path = Path.cwd() / QR_DIRECTORY / qr_filename

    # Ensure the QR code directory exists
    create_directory(Path.cwd() / QR_DIRECTORY)

    # Generate and save the QR code
    generate_qr_code(args.url, qr_code_full_path, FILL_COLOR, BACK_COLOR)


if __name__ == "__main__":
    main()
