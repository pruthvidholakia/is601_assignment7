"""
Entry point so users can still run:
    python main.py --url https://example.com
while all real work happens in app.qr.
"""
from app.qr import main

if __name__ == "__main__":
    main()