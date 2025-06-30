# tests/test_qr.py
from pathlib import Path

from main import is_valid_url, generate_qr_code


def test_is_valid_url_good():
    # A well-formed URL should be truthy
    assert is_valid_url("https://www.example.com")


def test_is_valid_url_bad():
    # A malformed URL should evaluate to False
    assert not is_valid_url("not-a-url")


def test_generate_qr_code_creates_file(tmp_path):
    """
    generate_qr_code should create a non-empty PNG at the given path.
    """
    qr_path = tmp_path / "qr.png"

    generate_qr_code(
        data="https://www.example.com",
        path=qr_path,
        fill_color="black",
        back_color="white",
    )

    assert qr_path.exists() and qr_path.stat().st_size > 0
