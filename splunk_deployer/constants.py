"""Defines constants"""

# Standard libraries
import sys
from pathlib import Path

main_file_path = getattr(sys.modules["__main__"], "__file__", None) or sys.argv[0]
PARENT_DIRECTORY = Path(main_file_path).resolve().parents[1]

VERSION = (PARENT_DIRECTORY / "VERSION.txt").read_text().strip()
