from datetime import datetime
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class Color:

    def __init__(self, red, green, blue, name=None):
        """
        Creates a Color instance that represents a single RGB color. The
        original color values and brightness are stored to allow referencing
        when modifying the color values.

        :param red: int, the amount of red on a scale 0-255.
        :param green: int, the amount of green on a scale 0-255.
        :param blue: int, the amount of blue on a scale 0-255.
        :param name: str, the name of the color.
        """

        self.__red = red
        self.__green = green
        self.__blue = blue
        self.__name = name

        self.__original_red = red
        self.__original_green = green
        self.__original_blue = blue
        self.__original_brightness = self.get_brightness()

    def __str__(self):
        """
        Converts the Color instance to a string.

        :return: str, the Color instance.
        """

        return f'{self.__name}: {self.hex()}'

    def hex(self):
        """
        Converts a color from RGB to a HEX color code string.

        :return: str, the color as hex color code.
        """

        return f'#{self.__red:02x}{self.__green:02x}{self.__blue:02x}'.upper()

    def name(self):
        """
        Fetches the color's name.

        :return: str, the name of the color.
        """

        return self.__name

    def values(self):
        """
        Separates the RGB values into an array.

        :return: array, the red, green and blue values in an array.
        """

        return [self.__red, self.__green, self.__blue]

    def get_minmidmax(self):
        """
        Arranges the RGB integer values into order from low to high.

        :return: tuple, the RGB values in ascending order.
        """

        rgb_array = self.values()
        min_value = sorted(rgb_array)[0]
        mid_value = sorted(rgb_array)[1]
        max_value = sorted(rgb_array)[2]

        minmidmax_rgb_values = (min_value, mid_value, max_value)

        return minmidmax_rgb_values

    def get_lightness(self):
        """
        Determines the lightness of the color as in ratio of white and black
        of the color. Value 0 represents pure black and 1 pure white.

        :return: float, the lightness of the color as value between 0-1.
        """

        rgb_minmidmax_values = self.get_minmidmax()
        lowest_rgb_value = rgb_minmidmax_values[0]
        highest_rgb_value = rgb_minmidmax_values[2]

        return (lowest_rgb_value + highest_rgb_value) / 2 / 255

    def get_brightness(self):
        """
        Calculates the relative luminance of the color.
        https://en.wikipedia.org/wiki/Relative_luminance

        :return: float, the brightness of the color.
        """
        return (
            0.2126 * self.__red + 0.7152 * self.__green + 0.0722 * self.__blue
        )

    def clamp_rgb_value(self, rgb_value):
        """
        Clamps the RGB value to valid range 0-255. Converts the value to an int
        if a float is provided.

        :param rgb_value: float, the value to clamp.
        :return: int, the RGB value in 0-255.
        """

        if (
                not isinstance(rgb_value, float)
                and not isinstance(rgb_value, int)
        ):
            show_error('Invalid RGB value to clamp received!')
            return

        if rgb_value < 0:
            return 0
        elif rgb_value > 255:
            return 255
        else:
            return round(rgb_value)

    def brightness(self, brightness_amount):
        """
        Modify the luminance of the color in relation to the colors original
        luminance amount. Maintains the colors original hue.

        :param brightness_amount: float, the amount of brightness 0.0-255.0
        """

        if (
            not isinstance(brightness_amount, float)
        ):
            show_error('Invalid brightness value received!')
            return

        brightness_change = brightness_amount - self.__original_brightness

        new_red_rgb_value = self.__original_red + brightness_change
        new_green_rgb_value = self.__original_green + brightness_change
        new_blue_rgb_value = self.__original_blue + brightness_change

        self.__red = self.clamp_rgb_value(new_red_rgb_value)
        self.__green = self.clamp_rgb_value(new_green_rgb_value)
        self.__blue = self.clamp_rgb_value(new_blue_rgb_value)

    def tint(self, tint_percentage):
        """
        Modifies the tint of the color as in adds white to it.

        :param tint_percentage: int, the percentage of tinting to apply.
        :return: Color, the tinted color.
        """

        if (
                not isinstance(tint_percentage, int)
                or 0 > tint_percentage > 100
        ):
            show_error('Invalid tint parameter received!')
            return

        tint_fraction = tint_percentage / 100
        self.__red = self.clamp_rgb_value(self.__red + (255 - self.__red)
                                          * tint_fraction)
        self.__green = self.clamp_rgb_value(self.__green + (255 - self.__green)
                                            * tint_fraction)
        self.__blue = self.clamp_rgb_value(self.__blue + (255 - self.__blue)
                                           * tint_fraction)

        return self

    def shade(self, shade_percentage):
        """
        Modifies the shade of the color as in adds black to it.

        :param shade_percentage: int, the percentage of shading to apply.
        :return: Color, the shaded color.
        """

        if (
                not isinstance(shade_percentage, int)
                or 0 > shade_percentage > 100
        ):
            show_error('Invalid shade parameter received!')
            return

        shade_fraction = shade_percentage / 100
        self.__red = self.clamp_rgb_value(self.__red * (1 - shade_fraction))
        self.__green = self.clamp_rgb_value(
            self.__green * (1 - shade_fraction))
        self.__blue = self.clamp_rgb_value(self.__blue * (1 - shade_fraction))

        return self

    def tone(self, tone_percentage):
        """
        Modifies the saturation aka tone of the color as in adds gray to it.

        :param tone_percentage: int, the percentage  of shading to apply.
        :return: Color, the toned color.
        """

        if (
                not isinstance(tone_percentage, int)
                or 0 > tone_percentage > 100
        ):
            show_error('Invalid tone parameter received!')
            return

        minmidmax_rgb_values = self.get_minmidmax()
        gray_rgb_value = self.get_lightness() * 255

        saturation_range = round(min(255 - gray_rgb_value, gray_rgb_value))
        max_shift = min((255 - minmidmax_rgb_values[2]),
                        minmidmax_rgb_values[0])
        shift_amount = min(saturation_range / tone_percentage, max_shift)

        mid_difference = gray_rgb_value - minmidmax_rgb_values[1]
        max_difference = gray_rgb_value - minmidmax_rgb_values[2]
        mid_ratio = mid_difference / max_difference

        max_value = 0
        toned_rgb_values = [0] * 3
        rgb_values = self.values()
        for idx, rgb_value in enumerate(rgb_values):
            if rgb_value == minmidmax_rgb_values[0]:
                toned_rgb_values[idx] = \
                    self.clamp_rgb_value(
                        minmidmax_rgb_values[0] - shift_amount)
            elif rgb_value == minmidmax_rgb_values[2]:
                toned_rgb_values[idx] = \
                    self.clamp_rgb_value(
                        minmidmax_rgb_values[2] + shift_amount)
                max_value = rgb_values[idx]
            elif rgb_value == minmidmax_rgb_values[1]:
                toned_rgb_values[idx] = self.clamp_rgb_value(
                    gray_rgb_value + (max_value - gray_rgb_value) * mid_ratio)

        self.__red = toned_rgb_values[0]
        self.__green = toned_rgb_values[1]
        self.__blue = toned_rgb_values[2]

        return self


class Palette:

    def __init__(self, color_wheel='RYB'):
        """
        Creates a Palette instance that represents a group of Color instances.
        """

        self.__RYB_COLORS = [
            Color(254, 39, 18, 'Red'),
            Color(252, 96, 10, 'Red-orange'),
            Color(251, 153, 2, 'Orange'),
            Color(252, 204, 26, 'Yellow-orange'),
            Color(254, 254, 51, 'Yellow'),
            Color(178, 215, 50, 'Yellow-green'),
            Color(102, 176, 50, 'Green'),
            Color(52, 124, 152, 'Blue-green'),
            Color(2, 71, 254, 'Blue'),
            Color(68, 36, 214, 'Blue-violet'),
            Color(134, 1, 175, 'Violet'),
            Color(194, 20, 96, 'Red-violet')
        ]
        self.__RGB_COLORS = [
            Color(255, 0, 0, 'Red'),
            Color(255, 128, 0, 'Orange'),
            Color(255, 255, 0, 'Yellow'),
            Color(128, 255, 0, 'Chartreuse'),
            Color(0, 255, 0, 'Green'),
            Color(0, 255, 128, 'Mint'),
            Color(0, 255, 255, 'Cyan'),
            Color(0, 128, 255, 'Azure'),
            Color(0, 0, 255, 'Blue'),
            Color(128, 0, 255, 'Purple'),
            Color(255, 0, 255, 'Magenta'),
            Color(255, 0, 128, 'Rose')
        ]
        self.__CMYK_COLORS = [
            Color(0, 255, 255, 'Cyan'),
            Color(0, 128, 255, 'Azure'),
            Color(0, 0, 255, 'Blue'),
            Color(128, 0, 255, 'Purple'),
            Color(255, 0, 255, 'Magenta'),
            Color(255, 0, 128, 'Rose'),
            Color(255, 0, 0, 'Red'),
            Color(255, 128, 0, 'Orange'),
            Color(255, 255, 0, 'Yellow'),
            Color(128, 255, 0, 'Chartreuse'),
            Color(0, 255, 0, 'Green'),
            Color(0, 255, 128, 'Mint')
        ]
        self.__color_wheels = {
            'RYB': self.__RYB_COLORS,
            'RGB': self.__RGB_COLORS,
            'CMYK': self.__CMYK_COLORS
        }
        """
        Color schemes are presented as arrays with each 12 hue in the color
        wheel representing index values 0-11 with root color being value 0.
        """
        self.__COLOR_SCHEMES = {
            'Analogous': [0, 1, 11],
            'Complementary': [0, 6],
            'Triadic': [0, 4, 8],
            'Tetradic': [0, 2, 6, 8],
            'Square': [0, 3, 6, 9],
            'Split-complementary': [0, 5, 7],
            'Double split-complementary': [0, 1, 5, 7, 11],
            'Clash': [0, 2, 8],
            'Intermediate': [0, 2, 4, 6, 8, 10]
        }

        if (
                not isinstance(color_wheel, str)
                or color_wheel.upper() not in self.__color_wheels
        ):
            show_error(f'Value {color_wheel} is not a valid color wheel!')
            return

        self.__color_palette = self.__color_wheels[color_wheel.upper()]
        self.__color_wheel = color_wheel.upper()
        self.__color_scheme = list(self.__COLOR_SCHEMES.keys())[0]
        self.__picked_color = self.__color_palette[0]

    def values(self):
        """
        Gets all the colors currently in the palette as an array.

        :return: list, the colors in the palette.
        """

        return self.__color_palette

    def get(self, index):
        """
        Fetches a color from the palette based on index value.

        :param index: int, the index of the color to fetch.
        :return: Color, the color at the specified index.
        """

        if (
                not isinstance(index, int)
                or 0 > index >= len(self.__color_palette)
        ):
            show_error('Tried getting an index that\'s not in the palette!')
            return

        return self.__color_palette[index]

    def find_by_name(self, name):
        """
        Fetches a color from the palette by name.

        :name: str, the name of the color to search for.
        :return: Color, the color with the searched name.
        """

        for color_in_palette in self.values():
            if name == color_in_palette.name():
                return color_in_palette

        show_error('The searched color couldn\'t be found!')
        return

    def get_color_wheel(self):
        """
        Fetches the color wheel of the palette.

        :return: str, the color wheel value of the palette.
        """

        return self.__color_wheel

    def get_color_scheme(self):
        """
        Fetches the color scheme of the palette.

        :return: str, the color scheme value of the palette.
        """

        return self.__color_scheme

    def get_picked_color(self):
        """
        Fetches the color that is set as the picked color in the palette.

        :return: Color, the color currently picked.
        """

        return self.__picked_color

    def random_color(self):
        """
        Fetches a random color from the current palette.

        :return: Color, the randomly picked color.
        """

        return self.__color_palette[
            random.randint(0, len(self.__color_palette) - 1)]

    def set_color_wheel(self, color_wheel_key):
        """
        Sets the colors of the palette according to provided color wheel key.

        :param color_wheel_key: str, the color wheel to set.
        :return: Palette, the palette with set color wheel.
        """

        if (
                not isinstance(color_wheel_key, str)
                or color_wheel_key not in self.__color_wheels
        ):
            show_error(f'Invalid color wheel key {color_wheel_key} provided!')
            return

        self.__color_palette = self.__color_wheels[color_wheel_key]
        self.__color_wheel = color_wheel_key

        return self

    def set_color_scheme(self, color_scheme_key):
        """
        Sets the color scheme for the palette according to provided color
        scheme key.

        :param color_scheme_key: str, the color scheme to set.
        :return: Palette, the palette with set color scheme.
        """

        if (
                not isinstance(color_scheme_key, str)
                or color_scheme_key not in self.__COLOR_SCHEMES
        ):
            show_error(f'Invalid color scheme {color_scheme_key} provided!')
            return

        self.__color_scheme = color_scheme_key

        return self

    def set_picked_color(self, picked_color):
        """
        Sets the provided color as the picked color in the palette.

        :return: Palette, the palette with currently picked color.
        """

        if (
                # Note! Remove comment from line below when classes are split
                # to separate files
                # not isinstance(picked_color, Color) or
                picked_color not in self.__color_palette
        ):
            show_error('Tried to set invalid picked color!')
            return

        self.__picked_color = picked_color

        return self

    def sort_color_wheel(self, first_color):
        """
        Organizes the palette to color wheel order according to provided root
        color.

        :param first_color: Color, the root color to be arranged as first.
        :return: Palette, the sorted palette.
        """

        if (
                # Note! Remove comment from line below when splitting class to
                # separate file
                # not isinstance(first_color, Color) or
                first_color not in self.__color_palette
        ):
            show_error('Invalid color to sort by provided!')
            return

        self.__color_palette = \
            self.__color_palette[self.__color_palette.index(first_color):] + \
            self.__color_palette[:self.__color_palette.index(first_color)]

        return self

    def get_scheme_colors(self):
        """
        Fetches colors from the polette that are included in the current color
        scheme.

        :return: list, the colors in the current color scheme.
        """

        color_scheme_colors = []
        for idx in self.__COLOR_SCHEMES[self.__color_scheme]:
            color_scheme_colors.append(self.__color_palette[idx])

        return color_scheme_colors

    def to_tint(self, tint_percentage):
        """
        Tints (lighten) the palette colors according to provided tint amount.

        :param tint_percentage: int, the percentage of tint to apply.
        :return: Palette, the tinted color palette.
        """

        if (
                not isinstance(tint_percentage, int)
                or 0 > tint_percentage > 100
        ):
            show_error('Invalid tint percentage received!')
            return

        for color in self.values():
            color.tint(tint_percentage)

        return self

    def to_shade(self, shade_percentage):
        """
        Shades (darken) the palette colors according to provided shade amount.

        :param shade_percentage: int, the percentage of shade to apply.
        :return: Palette, the shaded color palette.
        """

        if (
                not isinstance(shade_percentage, int)
                or 0 > shade_percentage > 100
        ):
            show_error('Invalid shade percentage received!')
            return

        for color in self.values():
            color.shade(shade_percentage)

        return self

    def to_tone(self, tone_percentage):
        """
        Tones (saturate) the palette colors according to provided tone amount.

        :param tone_percentage: int, the percentage of tone to apply.
        :return: Palette, the toned color palette.
        """

        if (
                not isinstance(tone_percentage, int)
                or 0 > tone_percentage > 100
        ):
            show_error('Invalid tone percentage received!')
            return

        for color in self.values():
            color.tone(tone_percentage)

        return self


class ColorPaletterUI:

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

        self.__copy_icon_image = tk.PhotoImage(master=self.__main_window,
                                               file='noun_copy_964433.png')
        self.__save_icon_image = tk.PhotoImage(master=self.__main_window,
                                               file='noun_sticker_964404.png')

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
        self.__color_wheel_combobox.grid(row=0, column=0)

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
            width=400)
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
        self.__color_scheme_combobox.grid(row=1, column=0, pady=(0, 10))

        # Initialize Hue brightness slider and preview panel
        self.__hue_brightness_label = ttk.Label(
            self.__color_scheme_settings_frame, text='Brightness')
        self.__hue_brightness_label.grid(row=2, column=0, pady=(5, 2))

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
            borderwidth=2,
            height=140,
            width=270)

        self.__hue_preview_frame.grid(row=4, column=0)

        # Initialize Palette view
        self.__palette_view_frame = ttk.Frame(self.__main_window)
        self.__palette_view_frame.grid(row=2, column=0, columnspan=7)

        # Initialize Message display and Palette export to file button
        self.__palette_export_frame = ttk.Frame(self.__main_window)
        self.__palette_export_frame.grid(row=2, column=7, columnspan=6)

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
            padding=(0, 5, 25, 5),
            width=12)

        self.__palette_export_button.grid(row=1, column=0, padx=(100, 0),
                                          pady=(0, 10))

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

                picked_color_wheel = self.__color_picker_palette\
                    .get_color_wheel()

                self.__color_wheel_hue_palette = Palette()
                self.__color_wheel_hue_palette\
                    .set_color_wheel(picked_color_wheel)
                root_color = self.__color_wheel_hue_palette \
                    .find_by_name(color_value.name())
                self.__color_wheel_hue_palette.set_picked_color(root_color)
                self.__color_wheel_hue_palette \
                    .sort_color_wheel(root_color)

                self.__color_wheel_tint_palette = Palette()
                self.__color_wheel_tint_palette \
                    .set_color_wheel(picked_color_wheel)
                root_color = self.__color_wheel_tint_palette \
                    .find_by_name(color_value.name())
                self.__color_wheel_tint_palette.set_picked_color(root_color)
                self.__color_wheel_tint_palette \
                    .sort_color_wheel(root_color)
                self.__color_wheel_tint_palette.to_tint(25)

                self.__color_wheel_shade_palette = Palette()
                self.__color_wheel_shade_palette \
                    .set_color_wheel(picked_color_wheel)
                root_color = self.__color_wheel_shade_palette \
                    .find_by_name(color_value.name())
                self.__color_wheel_shade_palette.set_picked_color(root_color)
                self.__color_wheel_shade_palette \
                    .sort_color_wheel(root_color)
                self.__color_wheel_shade_palette.to_shade(25)

                self.__color_wheel_tone_palette = Palette()
                self.__color_wheel_tone_palette \
                    .set_color_wheel(picked_color_wheel)
                root_color = self.__color_wheel_tone_palette \
                    .find_by_name(color_value.name())
                self.__color_wheel_tone_palette.set_picked_color(root_color)
                self.__color_wheel_tone_palette \
                    .sort_color_wheel(root_color)
                self.__color_wheel_tone_palette.to_tone(10)

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
        slice_degrees = 360.0 / len(color_slices)

        for idx, color in enumerate(color_slices):

            def select_hue(event, selected_hue=color):
                self.__selected_color_wheel_palette \
                    .set_picked_color(selected_hue)
                self.update_hue_brightness_slider()
                self.update_all_color_previews()

            angle = slice_degrees * idx + 76.0
            tag_id = f'slice-{idx}'

            self.__pie_canvas.create_arc(10, 10, 400, 400,
                                         extent=slice_degrees,
                                         fill=color.hex(),
                                         outline=color.hex(),
                                         start=angle,
                                         tags=(tag_id,))

            self.__pie_canvas.tag_bind(tag_id, '<1>', select_hue)

            if color in scheme_color_slices:
                tag_id = f'slice-selected-{idx}'

                self.__pie_canvas.create_arc(10, 10, 400, 400,
                                             extent=slice_degrees,
                                             outline='black',
                                             start=angle,
                                             tags=(tag_id,),
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

        for widget in self.__palette_view_frame.winfo_children():
            widget.destroy()

        for idx, color in enumerate(
                self.__selected_color_wheel_palette.get_scheme_colors()
        ):
            palette_swatch_frame = ttk.Frame(self.__palette_view_frame,
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


def show_error(error_message):
    """
    Display an error message in a new popup window.

    :param error_message: str, the message to display.
    """

    if not isinstance(error_message, str):
        return

    messagebox.showerror('Colorian', error_message)


def main():
    ColorPaletterUI()


if __name__ == '__main__':
    main()
