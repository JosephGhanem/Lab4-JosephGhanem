"""Choose one GUI event loop per process; both use the same backend."""
import argparse
from pathlib import Path
from backend import DEFAULT_DB


def main():
    parser = argparse.ArgumentParser(description='Lab 4 solo task manager')
    parser.add_argument('--ui', choices=['tkinter', 'pyqt'], default='tkinter')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB, help='Shared SQLite database path')
    args = parser.parse_args()
    if args.ui == 'tkinter':
        from tkinter_ui import run
    else:
        from pyqt_ui import run
    run(args.db)


if __name__ == '__main__':
    main()
