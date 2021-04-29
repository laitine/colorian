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


def main():
    colorian_ui.ColorianUI()


if __name__ == '__main__':
    main()
