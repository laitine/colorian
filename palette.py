import random

from color import Color
from main import show_error


class Palette:

    def __init__(self, color_wheel='RYB'):
        """
        Creates a Palette instance that represents a group of Color instances.
        the palette has colors from a specific color wheel, a color scheme and
        a picked color.
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
            Color(68, 36, 214, 'Blue-purple'),
            Color(134, 1, 175, 'Purple'),
            Color(194, 20, 96, 'Red-purple')
        ]
        self.__RGB_COLORS = [
            Color(255, 0, 0, 'Red'),
            Color(255, 128, 0, 'Orange'),
            Color(255, 255, 0, 'Yellow'),
            Color(128, 255, 0, 'Chartreuse Green'),
            Color(0, 255, 0, 'Green'),
            Color(0, 255, 128, 'Spring Green'),
            Color(0, 255, 255, 'Cyan'),
            Color(0, 128, 255, 'Azure'),
            Color(0, 0, 255, 'Blue'),
            Color(128, 0, 255, 'Violet'),
            Color(255, 0, 255, 'Magenta'),
            Color(255, 0, 128, 'Rose')
        ]
        self.__CMYK_COLORS = [
            Color(0, 255, 255, 'Cyan'),
            Color(0, 128, 255, 'Azure'),
            Color(0, 0, 255, 'Blue'),
            Color(128, 0, 255, 'Violet'),
            Color(255, 0, 255, 'Magenta'),
            Color(255, 0, 128, 'Rose'),
            Color(255, 0, 0, 'Red'),
            Color(255, 128, 0, 'Orange'),
            Color(255, 255, 0, 'Yellow'),
            Color(128, 255, 0, 'Chartreuse Green'),
            Color(0, 255, 0, 'Green'),
            Color(0, 255, 128, 'Spring Green')
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
        Fetches all the colors currently in the palette as a list.

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

        if not isinstance(name, str):
            show_error('Invalid color name to search for received!')
            return

        for color_in_palette in self.values():
            if name == color_in_palette.name():
                return color_in_palette

        show_error('The searched color couldn\'t be found!')
        return

    def get_color_wheel(self):
        """
        Fetches the color wheel key of the palette.

        :return: str, the color wheel value of the palette.
        """

        return self.__color_wheel

    def get_color_scheme(self):
        """
        Fetches the color scheme key of the palette.

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
        Fetches a random color from the palette.

        :return: Color, the randomly picked color.
        """

        return self.__color_palette[
            random.randint(0, len(self.__color_palette) - 1)]

    def get_scheme_colors(self):
        """
        Fetches colors from the palette that are included in the current color
        scheme.

        :return: list, the colors in the current color scheme.
        """

        color_scheme_colors = []
        for idx in self.__COLOR_SCHEMES[self.__color_scheme]:
            color_scheme_colors.append(self.__color_palette[idx])

        return color_scheme_colors

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
            show_error(f'Invalid color wheel key provided!')
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
                not isinstance(picked_color, Color) or
                picked_color not in self.__color_palette
        ):
            show_error('Tried to set invalid picked color!')
            return

        self.__picked_color = picked_color

        return self

    def sort_color_wheel(self, first_color):
        """
        Organizes the palette to color wheel order starting with provided root
        color.

        :param first_color: Color, the root color to be arranged as first.
        :return: Palette, the sorted palette.
        """

        if (
                not isinstance(first_color, Color) or
                first_color not in self.__color_palette
        ):
            show_error('Invalid color to sort by provided!')
            return

        self.__color_palette = \
            self.__color_palette[self.__color_palette.index(first_color):] + \
            self.__color_palette[:self.__color_palette.index(first_color)]

        return self

    def to_tint(self, tint_percentage):
        """
        Tints (lightens) the palette colors according to provided tint amount.

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
        Shades (darkens) the palette colors according to provided shade amount.

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
        Tones (saturates) the palette colors according to provided tone amount.

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
