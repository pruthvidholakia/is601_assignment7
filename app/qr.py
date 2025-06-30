import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import qrcode
import validators
from dotenv import load_dotenv

# --------------------------------------------------------------------------- #
#  Environment variables (optional .env)                                      #
# --------------------------------------------------------------------------- #
load_dotenv()

QR_DIRECTORY = os.getenv("QR_CODE_DIR", "qr_codes")
FILL_COLOR   = os.getenv("FILL_COLOR", "red")
BACK_COLOR   = os.getenv("BACK_COLOR", "white")

# --------------------------------------------------------------------------- #
#  Helpers                                                                    #
# --------------------------------------------------------------------------- #
def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def create_directory(path: Path) -> None:
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        logging.error("Cannot create directory %s: %s", path, exc)
        sys.exit(1)


def is_valid_url(url: str) -> bool:
    return validators.url(url)


def generate_qr_code(
    data: str,
    path: Path,
    fill_color: str = FILL_COLOR,
    back_color: str = BACK_COLOR,
) -> None:
    if not is_valid_url(data):
        logging.error("Invalid URL provided: %s", data)
        sys.exit(1)

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save(path)
    logging.info("QR code saved to %s", path.resolve())


# --------------------------------------------------------------------------- #
#  Public CLI                                                                 #
# --------------------------------------------------------------------------- #
def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a QR code.")
    parser.add_argument(
        "--url",
        default="https://github.com/pruthvidholakia",
        help="URL to encode in the QR code",
    )
    args = parser.parse_args()

    setup_logging()

    timestamp   = datetime.now().strftime("%Y%m%d%H%M%S")
    filename    = f"QRCode_{timestamp}.png"
    out_dir     = Path.cwd() / QR_DIRECTORY
    out_path    = out_dir / filename

    create_directory(out_dir)
    generate_qr_code(args.url, out_path)


# Module is import-safe; CLI only runs if executed directly
if __name__ == "__main__":
    main()