from datetime import datetime
import tkinter as tk
from tkinter import ttk

from main import show_error, resource_path
from palette import Palette


class ColorianUI:

    def __init__(self):
        """
        Creates Colorian UI initializing the color palettes and starts running
        it in a new window.
        """

        self.__color_picker_palette = Palette()
        random_color = self.__color_picker_palette.random_color()
        self.__color_picker_palette.set_picked_color(random_color)

        self.__color_wheel_hue_palette = Palette()
        picked_hue_color = self.__color_wheel_hue_palette.find_by_name(
            random_color.name())
        self.__color_wheel_hue_palette.set_picked_color(picked_hue_color)

        self.__color_wheel_tint_palette = Palette().to_tint(25)
        picked_hue_color = self.__color_wheel_tint_palette.find_by_name(
            random_color.name())
        self.__color_wheel_tint_palette.set_picked_color(picked_hue_color)

        self.__color_wheel_shade_palette = Palette().to_shade(25)
        picked_hue_color = self.__color_wheel_shade_palette.find_by_name(
            random_color.name())
        self.__color_wheel_shade_palette.set_picked_color(picked_hue_color)

        self.__color_wheel_tone_palette = Palette().to_tone(50)
        picked_hue_color = self.__color_wheel_tone_palette.find_by_name(
            random_color.name())
        self.__color_wheel_tone_palette.set_picked_color(picked_hue_color)

        self.__selected_color_wheel_palette = self.__color_wheel_hue_palette

        self.__color_wheels = {
            'RYB (Web)': 'RYB',
            'RGB (Screen)': 'RGB',
            'CMYK (Print)': 'CMYK'
        }
        self.__hue_variants = {
            'Hue': 'HUE',
            'Tint': 'TINT',
            'Shade': 'SHADE',
            'Tone': 'TONE'
        }
        self.__color_schemes = [
            'Analogous',
            'Complementary',
            'Triadic',
            'Tetradic',
            'Square',
            'Split-complementary',
            'Double split-complementary',
            'Clash',
            'Intermediate'
        ]

        # Create custom widget theme
        self.__default_ui_dark_color = '#000000'
        self.__default_ui_frame_color = '#313131'
        self.__default_ui_bg_color = '#4B4B4C'
        self.__default_ui_fg_color = '#B0AFB0'
        self.__default_ui_focus_color = '#B0AFB0'
        self.__default_ui_highlight_color = '#696969'

        self.__main_window = tk.Tk()

        widget_style = ttk.Style()
        widget_style.theme_settings('alt', {
            'TButton': {
                'configure': {
                    'anchor': tk.E,
                    'background': self.__default_ui_highlight_color,
                    'foreground': self.__default_ui_dark_color,
                    'highlightthickness': 4,
                    'font': ('Helvetica', 16),
                    'bordercolor': self.__default_ui_fg_color,
                    'padding': 5,
                    'shiftrelief': 0
                },
                'map': {
                    'background': [
                        ('selected', False)
                    ],
                    'bordercolor': [
                        ('active', self.__default_ui_focus_color),
                        ('focus', self.__default_ui_focus_color)
                    ]
                }
            },
            'TCanvas': {
                'configure': {
                    'background': self.__default_ui_frame_color
                }
            },
            'TCombobox': {
                'configure': {
                    'arrowcolor': self.__default_ui_bg_color,
                    'arrowsize': 26,
                    'foreground': self.__default_ui_fg_color,
                    'padding': '5'
                },
                'map': {
                    'background': [
                        ('readonly', self.__default_ui_highlight_color)],
                    'bordercolor': [
                        ('readonly', self.__default_ui_highlight_color)],
                    'fieldbackground': [
                        ('readonly', self.__default_ui_bg_color)]
                }
            },
            'TFrame': {
                'configure': {
                    'background': self.__default_ui_frame_color
                }
            },
            'TLabel': {
                'configure': {
                    'background': self.__default_ui_frame_color,
                    'foreground': self.__default_ui_fg_color
                }
            },
            'TScale': {
                'configure': {
                    'background': self.__default_ui_frame_color,
                    'borderwidth': 10,
                    'groovewidth': 10,
                    'troughcolor': self.__default_ui_highlight_color,
                    'troughrelief': tk.SOLID
                },
                'map': {
                    'background': [
                        ('selected', False)
                    ]
                }
            }
        })
        widget_style.theme_use('alt')

        # Initialize Main window and images
        self.__main_window.title('Colorian')
        self.__main_window.configure(bg=self.__default_ui_frame_color)

        self.__copy_icon_image = tk.PhotoImage(
            master=self.__main_window,
            file=resource_path('noun_copy_964433.png'))
        self.__save_icon_image = tk.PhotoImage(
            master=self.__main_window,
            file=resource_path('noun_sticker_964404.png'))

        # Initialize Color wheel dropdown
        color_wheels_list = list(self.__color_wheels.keys())
        self.__color_wheel_value = tk.StringVar(self.__main_window,
                                                color_wheels_list[0])

        self.__color_wheel_combobox = ttk.Combobox(
            self.__main_window,
            state='readonly',
            textvariable=self.__color_wheel_value,
            values=color_wheels_list,
            width=12
        )
        self.__color_wheel_combobox.bind('<<ComboboxSelected>>',
                                         self.set_color_wheel)
        self.__color_wheel_combobox.grid(row=0, column=0, padx=(20, 10))

        # Initialize Color picker
        self.__color_picker_frame = ttk.Frame(self.__main_window)
        self.__color_picker_frame.grid(row=0, column=1, columnspan=12)

        self.update_color_picker()

        # Initialize Hue wheel
        self.__pie_canvas = tk.Canvas(
            self.__main_window,
            bg=self.__default_ui_frame_color,
            height=400,
            highlightbackground=self.__default_ui_frame_color,
            width=480)
        self.__pie_canvas.grid(row=1, column=0, columnspan=7)

        # Initialize Color scheme panel
        self.__color_scheme_settings_frame = ttk.Frame(self.__main_window)
        self.__color_scheme_settings_frame.grid(row=1, column=7, columnspan=6)

        # Initialize Hue variation selector
        self.__hue_variant_selector_frame = ttk.Frame(
            self.__color_scheme_settings_frame)
        self.__hue_variant_selector_frame.grid(row=0, column=0, pady=10)

        hue_variant_list = list(self.__hue_variants.keys())
        self.__hue_variant_value = tk.StringVar(self.__main_window,
                                                hue_variant_list[0])

        for idx, title in enumerate(hue_variant_list):
            # Note! Uses tk to allow more customization over ttk
            hue_variant_radiobutton = tk.Radiobutton(
                self.__hue_variant_selector_frame,
                foreground=self.__default_ui_fg_color,
                background=self.__default_ui_frame_color,
                selectcolor=self.__default_ui_highlight_color,
                command=self.set_hue_variant,
                indicator=0,
                pady=10,
                relief=tk.SOLID,
                text=title,
                value=hue_variant_list[idx],
                variable=self.__hue_variant_value,
                width=30)
            hue_variant_radiobutton.grid(row=idx, column=0, sticky=tk.W)

        # Initialize Color scheme dropdown
        self.__color_scheme_value = tk.StringVar(
            self.__main_window,
            self.__selected_color_wheel_palette.get_color_scheme())

        self.__color_scheme_combobox = ttk.Combobox(
            self.__color_scheme_settings_frame,
            state='readonly',
            textvariable=self.__color_scheme_value,
            values=self.__color_schemes,
            width=25
        )

        self.__color_scheme_combobox.bind('<<ComboboxSelected>>',
                                          self.set_color_scheme)
        self.__color_scheme_combobox.grid(row=1, column=0, pady=(0, 5))

        # Initialize Hue brightness slider and preview panel
        self.__hue_brightness_label = ttk.Label(
            self.__color_scheme_settings_frame, text='Brightness')
        self.__hue_brightness_label.grid(row=2, column=0, pady=(2, 2))

        self.__hue_brightness_value = tk.DoubleVar(
            self.__main_window, random_color.get_brightness())
        hue_brightness_min_value = 0.0
        hue_brightness_max_value = 255.0

        self.__hue_brightness_scale = ttk.Scale(
            self.__color_scheme_settings_frame,
            command=self.set_hue_brightness,
            from_=hue_brightness_min_value,
            length=270,
            orient=tk.HORIZONTAL,
            to=hue_brightness_max_value,
            variable=self.__hue_brightness_value)

        self.__hue_brightness_scale.grid(row=3, column=0)

        self.__hue_preview_frame = tk.Frame(
            self.__color_scheme_settings_frame,
            background=random_color.hex(),
            height=140,
            width=270)

        self.__hue_preview_frame.grid(row=4, column=0)

        # Initialize Palette view
        self.__palette_view_frame = ttk.Frame(self.__main_window)
        self.__palette_view_frame.grid(row=2, column=0, columnspan=7)
        self.__palette_view_frame.grid_propagate(0)
        self.__palette_view_swatches_frame = ttk.Frame(
            self.__palette_view_frame, height=80, width=480)
        self.__palette_view_swatches_frame.pack()

        # Initialize Message display and Palette export to file button
        self.__palette_export_frame = ttk.Frame(self.__main_window)
        self.__palette_export_frame.grid(row=2, column=8, columnspan=6)

        self.__palette_display_label = ttk.Label(
            self.__palette_export_frame)
        self.__palette_display_label.grid(row=0, column=0, pady=(5, 5))

        self.__palette_export_button = ttk.Button(
            self.__palette_export_frame,
            command=self.export_palette_to_file,
            compound=tk.LEFT,
            image=self.__save_icon_image,
            state='readonly',
            text='Export to file',
            padding=(0, 10, 25, 10),
            width=12)

        self.__palette_export_button.grid(row=1, column=0, sticky=tk.NE,
                                          padx=(53, 0), pady=(0, 20))

        # Start UI graphics and event loop
        self.update_all_color_previews()
        self.__main_window.mainloop()

    def display_message(self, message):
        """
        Shows a temporary message that is removed after the time expires.

        :param message: str, the message to display.
        """

        if not isinstance(message, str):
            show_error('Invalid message text received!')
            return

        self.__palette_display_label.config(text=message)
        self.__main_window.after(2000,
                                 lambda: self.__palette_display_label
                                 .config(text=''))

    def set_color_wheel(self, event):
        """
        Update what color wheel is being used and picks a random color from it.
        Clears text highlighting in the Combobox after selection has been made.

        :param event: tkinter.Event, the event triggered by user.
        """

        self.__color_wheel_combobox.selection_clear()

        color_wheel_key = self.__color_wheels[self.__color_wheel_value.get()]
        self.__color_picker_palette.set_color_wheel(color_wheel_key)

        random_color = self.__color_picker_palette.random_color()
        self.__color_picker_palette.set_picked_color(random_color)

        self.update_color_picker()

    def update_color_picker(self):
        """
        Populates the color picker buttons in order defined in the
        palette. Implements the selection of color for updating it as the
        picked color and all the color previews.
        """

        for widget in self.__color_picker_frame.winfo_children():
            widget.destroy()

        for idx, color in enumerate(self.__color_picker_palette.values()):

            color_swatch_frame = ttk.Frame(self.__color_picker_frame,
                                           height=50,
                                           width=50)
            color_swatch_frame.rowconfigure(0, weight=1)
            color_swatch_frame.columnconfigure(0, weight=1)
            color_swatch_frame.grid_propagate(0)
            color_swatch_frame.grid(row=0, column=idx)

            def set_picked_color(color_value=color):
                self.__color_picker_palette \
                    .set_picked_color(color_value)

                picked_color_wheel_key = self.__color_picker_palette \
                    .get_color_wheel()
                color_scheme_key = self.__color_scheme_value.get()

                self.__color_wheel_hue_palette = Palette()
                self.__color_wheel_hue_palette \
                    .set_color_wheel(picked_color_wheel_key)
                root_color = self.__color_wheel_hue_palette \
                    .find_by_name(color_value.name())
                self.__color_wheel_hue_palette.set_picked_color(root_color)
                self.__color_wheel_hue_palette \
                    .sort_color_wheel(root_color)
                self.__color_wheel_hue_palette.set_color_scheme(
                    color_scheme_key)

                self.__color_wheel_tint_palette = Palette()
                self.__color_wheel_tint_palette \
                    .set_color_wheel(picked_color_wheel_key)
                root_color = self.__color_wheel_tint_palette \
                    .find_by_name(color_value.name())
                self.__color_wheel_tint_palette.set_picked_color(root_color)
                self.__color_wheel_tint_palette \
                    .sort_color_wheel(root_color)
                self.__color_wheel_tint_palette.to_tint(25)
                self.__color_wheel_tint_palette.set_color_scheme(
                    color_scheme_key)

                self.__color_wheel_shade_palette = Palette()
                self.__color_wheel_shade_palette \
                    .set_color_wheel(picked_color_wheel_key)
                root_color = self.__color_wheel_shade_palette \
                    .find_by_name(color_value.name())
                self.__color_wheel_shade_palette.set_picked_color(root_color)
                self.__color_wheel_shade_palette \
                    .sort_color_wheel(root_color)
                self.__color_wheel_shade_palette.to_shade(25)
                self.__color_wheel_shade_palette.set_color_scheme(
                    color_scheme_key)

                self.__color_wheel_tone_palette = Palette()
                self.__color_wheel_tone_palette \
                    .set_color_wheel(picked_color_wheel_key)
                root_color = self.__color_wheel_tone_palette \
                    .find_by_name(color_value.name())
                self.__color_wheel_tone_palette.set_picked_color(root_color)
                self.__color_wheel_tone_palette \
                    .sort_color_wheel(root_color)
                self.__color_wheel_tone_palette.to_tone(10)
                self.__color_wheel_tone_palette.set_color_scheme(
                    color_scheme_key)

                color_scheme = \
                    self.__selected_color_wheel_palette.get_color_scheme()

                hue_variant_key = self.__hue_variants[
                    self.__hue_variant_value.get()]

                if hue_variant_key == 'HUE':
                    self.__selected_color_wheel_palette = \
                        self.__color_wheel_hue_palette
                elif hue_variant_key == 'TINT':
                    self.__selected_color_wheel_palette = \
                        self.__color_wheel_tint_palette
                elif hue_variant_key == 'SHADE':
                    self.__selected_color_wheel_palette = \
                        self.__color_wheel_shade_palette
                elif hue_variant_key == 'TONE':
                    self.__selected_color_wheel_palette = \
                        self.__color_wheel_tone_palette

                self.__selected_color_wheel_palette.set_color_scheme(
                    color_scheme)

                self.update_hue_brightness_slider()
                self.update_all_color_previews()

            swatch_button_style = ttk.Style()
            swatch_button_style.configure(
                f'SwatchStyle{idx}.TButton',
                background=color.hex(),
                relief=tk.FLAT)

            color_swatch_button = ttk.Button(
                color_swatch_frame,
                command=set_picked_color,
                state='readonly',
                style=f'SwatchStyle{idx}.TButton')

            color_swatch_button.grid(sticky=tk.NSEW)

    def draw_hue_wheel(self):
        """
        Updates the hue wheel and implements the selection of hue and updates
        all color previews.
        """

        color_slices = self.__selected_color_wheel_palette.values()
        scheme_color_slices = \
            self.__selected_color_wheel_palette.get_scheme_colors()
        extend_degrees = 360.0 / len(color_slices)
        start_degrees = extend_degrees * 2.5

        for idx, color in enumerate(color_slices):
            def select_hue(event, selected_hue=color):
                self.__selected_color_wheel_palette \
                    .set_picked_color(selected_hue)
                self.update_hue_brightness_slider()
                self.update_all_color_previews()

            start_angle = extend_degrees * idx + start_degrees
            tag_id = f'slice-{idx}'

            self.__pie_canvas.create_arc((50, 10, 440, 400),
                                         extent=extend_degrees,
                                         fill=color.hex(),
                                         outline=color.hex(),
                                         start=start_angle,
                                         tags=(tag_id,))

            self.__pie_canvas.tag_bind(tag_id, '<1>', select_hue)

        for idx, color in enumerate(color_slices):

            start_angle = extend_degrees * idx + start_degrees

            if color in scheme_color_slices:
                self.__pie_canvas.create_arc((50, 10, 440, 400),
                                             extent=extend_degrees,
                                             outline='black',
                                             start=start_angle,
                                             width=3)

    def update_all_color_previews(self):
        """
        Aggregates all the functions to call when a color changes or gets
        modified and the UI widget states need to be updated.
        """

        self.draw_hue_wheel()
        self.update_hue_preview()
        self.update_palette_view()

    def set_hue_variant(self):
        """
        Updates the hue variant to the selected value and updates color
        previews.
        """

        hue_variant_key = self.__hue_variants[self.__hue_variant_value.get()]

        if hue_variant_key == 'HUE':
            self.__selected_color_wheel_palette = \
                self.__color_wheel_hue_palette
        elif hue_variant_key == 'TINT':
            self.__selected_color_wheel_palette = \
                self.__color_wheel_tint_palette
        elif hue_variant_key == 'SHADE':
            self.__selected_color_wheel_palette = \
                self.__color_wheel_shade_palette
        elif hue_variant_key == 'TONE':
            self.__selected_color_wheel_palette = \
                self.__color_wheel_tone_palette

        self.update_all_color_previews()

    def set_color_scheme(self, event):
        """
        Updates the color scheme to the selected value. Clears text
        highlighting in the Combobox after selection has been made.

        :param event: tkinter.Event, the event triggered by user.
        """

        self.__color_scheme_combobox.selection_clear()
        color_scheme_key = self.__color_scheme_value.get()

        self.__color_wheel_hue_palette.set_color_scheme(color_scheme_key)
        self.__color_wheel_tint_palette.set_color_scheme(color_scheme_key)
        self.__color_wheel_shade_palette.set_color_scheme(color_scheme_key)
        self.__color_wheel_tone_palette.set_color_scheme(color_scheme_key)

        self.update_all_color_previews()

    def set_hue_brightness(self, event):
        """
        Modifies the selected color's brightness according to the fetched
        slider's value.

        :param event: tkinter.Event, the event triggered by user.
        """

        selected_hue_color = self.__selected_color_wheel_palette \
            .get_picked_color()

        selected_hue_color.brightness(self.__hue_brightness_value.get())

        self.update_all_color_previews()

    def update_hue_brightness_slider(self):
        """
        Updates the hue brightness slider position according to selected color.
        """

        selected_hue_color = self.__selected_color_wheel_palette \
            .get_picked_color()

        self.__hue_brightness_value.set(
            selected_hue_color.get_brightness())

    def update_hue_preview(self):
        """
        Updates the hue preview to the selected color.
        """

        selected_hue_color = self.__selected_color_wheel_palette \
            .get_picked_color()

        self.__hue_preview_frame.config(
            bg=selected_hue_color.hex())

    def update_palette_view(self):
        """
        Generates the palette view buttons and implements the click to copy
        color code feature for the buttons.
        """

        for widget in self.__palette_view_swatches_frame.winfo_children():
            widget.destroy()

        for idx, color in enumerate(
                self.__selected_color_wheel_palette.get_scheme_colors()
        ):
            palette_swatch_frame = ttk.Frame(
                self.__palette_view_swatches_frame,
                height=80,
                width=80)

            palette_swatch_frame.rowconfigure(0, weight=1)
            palette_swatch_frame.columnconfigure(0, weight=1)
            palette_swatch_frame.grid_propagate(0)
            palette_swatch_frame.grid(row=0, column=idx)

            def copy_color_to_clipboard(color_value=color):
                self.__main_window.clipboard_clear()
                self.__main_window.clipboard_append(color_value.hex())
                self.display_message('Copied to clipboard!')

            palette_button_style = ttk.Style()
            palette_button_style.configure(f'PaletteStyle{idx}.TButton',
                                           background=color.hex(),
                                           padding=(24, 40, 24, 0),
                                           relief=tk.FLAT)

            palette_swatch_button = ttk.Button(palette_swatch_frame,
                                               command=copy_color_to_clipboard,
                                               image=self.__copy_icon_image)

            palette_swatch_button.config(style=f'PaletteStyle{idx}.TButton')
            palette_swatch_button.grid(sticky=tk.NSEW)

    def export_palette_to_file(self):
        """
        Creates a file and converts the current palette to a string
        representation to write it to the file.
        """

        date_and_time = str(datetime.now()).split('.')[0]
        filename = f'Palette {date_and_time}.txt'

        try:
            file = open(filename, mode='w')
            content = 'Colorian Palette\n' + \
                      '================\n\n'

            color_scheme = \
                self.__selected_color_wheel_palette.get_color_scheme()

            content += \
                color_scheme + ' color scheme\n' + \
                ('-' * (len(color_scheme) + 13)) + '\n'

            for color in (
                    self.__selected_color_wheel_palette.get_scheme_colors()
            ):
                content += str(color) + '\n'

            content += '\n'

            content += 'Color wheel\n' + \
                       '-----------\n'

            for color in self.__selected_color_wheel_palette.values():
                content += str(color) + '\n'

            print(content, file=file)

            file.close()
        except OSError:
            show_error('Exporting to file ran into trouble!')
            return

        self.display_message('Palette exported!')
