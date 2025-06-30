import runpy
import sys
from pathlib import Path

import pytest

from app import qr
from app.qr import is_valid_url, generate_qr_code


def test_main_cli_creates_png(tmp_path, monkeypatch):
    """Run qr.main() with a temp cwd and be sure a PNG appears."""
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)             # fake cwd
    monkeypatch.setattr(sys, "argv", ["prog", "--url", "https://example.org"])
    qr.main()                                                      # runs CLI

    generated = list((tmp_path / qr.QR_DIRECTORY).glob("QRCode_*.png"))
    assert generated and generated[0].stat().st_size > 0


def test_generate_qr_code_rejects_bad_url(tmp_path):
    with pytest.raises(SystemExit):
        qr.generate_qr_code("not-a-url", tmp_path / "x.png")


def test_is_valid_url_good():
    assert is_valid_url("https://example.com")


def test_is_valid_url_bad():
    assert not is_valid_url("not-a-url")


def test_generate_qr_code_creates_file(tmp_path):
    outfile = tmp_path / "qr.png"
    generate_qr_code("https://example.com", outfile)
    assert outfile.exists() and outfile.stat().st_size > 0


def test_create_directory_failure(monkeypatch, tmp_path):
    """Force Path.mkdir to raise so the except-branch is executed."""
    bad_path = tmp_path / "no-perm"

    def boom(self, parents=False, exist_ok=False):  # noqa: D401
        raise PermissionError("no permission")      # triggers the except

    monkeypatch.setattr(Path, "mkdir", boom, raising=True)

    with pytest.raises(SystemExit):
        qr.create_directory(bad_path)


def test_module_entry_point(monkeypatch, tmp_path):
    """
    Execute `python -m app.qr` so the __main__ guard runs
    without argparse choking on pytest args.
    """
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    monkeypatch.setattr(sys, "argv", ["app.qr", "--url", "https://example.com"])
    sys.modules.pop("app.qr", None)

    runpy.run_module("app.qr", run_name="__main__")

    generated = list((tmp_path / qr.QR_DIRECTORY).glob("QRCode_*.png"))
    assert generated and generated[0].stat().st_size > 0

