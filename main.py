import os
import sys
from tkinter import messagebox

import colorian_ui


def show_error(error_message):
    """
    Display an error message in a new popup window.

    :param error_message: str, the message to display.
    """

    if not isinstance(error_message, str):
        return

    messagebox.showerror('Colorian', error_message)


def resource_path(relative_path):
    """
    Fetch the absolute path to the resource. For both local and PyInstaller.

    :param relative_path: str, the relative file path to transform.
    """
    base_path = getattr(sys, '_MEIPASS',
                        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def main():
    colorian_ui.ColorianUI()


if __name__ == '__main__':
    main()
