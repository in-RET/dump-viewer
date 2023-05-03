import argparse
import os

from gui import PYQT


if __name__ == '__main__':
    if PYQT:
        from gui import StartGui
        StartGui()
    else:
        parser = argparse.ArgumentParser(
            prog = 'main.py',
            description='Tool to inspect dump-files from oemof simulations.',
            epilog = 'In.RET - Institut für regenerative Energietechnik'
        )

        print("Please install PySide6 -- pip install pyside6")