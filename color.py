import colorsys

from main import show_error


class Color:

    def __init__(self, red, green, blue, name=None):
        """
        Creates a Color instance that represents a single RGB color. The
        initial color values and brightness are stored to allow referencing
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

        :return: str, the Color instance as a string.
        """

        return f'{self.__name}: {self.hex()}'

    def hex(self):
        """
        Converts a color from RGB to a hex color code.

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
        Separates the Red, Green and Blue values into an array.

        :return: array, the red, green and blue values in an array.
        """

        return [self.__red, self.__green, self.__blue]

    def get_minmidmax(self):
        """
        Arranges the RGB integer values into order from low to high.

        :return: tuple, the RGB values in ascending order.
        """

        rgb_array = sorted(self.values())
        min_value = rgb_array[0]
        mid_value = rgb_array[1]
        max_value = rgb_array[2]

        minmidmax_rgb_values = (min_value, mid_value, max_value)

        return minmidmax_rgb_values

    def get_lightness(self):
        """
        Determines the lightness of the color as a ratio between white and
        black. Value 0 represents pure black and 1 pure white.

        :return: float, the lightness of the color as value between 0.0-1.0.
        """

        rgb_minmidmax_values = self.get_minmidmax()
        lowest_rgb_value = rgb_minmidmax_values[0]
        highest_rgb_value = rgb_minmidmax_values[2]

        return (lowest_rgb_value + highest_rgb_value) / 2 / 255

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

    def clamp_fraction_value(self, color_value):
        """
        Clamps the provided fraction value to valid range 0.0-1.0. Converts the
        value to a float if int is provided.

        :param color_value: float, the value to clamp.
        :return: float, the value in 0.0-1.0.
        """

        if (
                not isinstance(color_value, float)
                and not isinstance(color_value, int)
        ):
            show_error('Invalid fraction value to clamp received!')
            return

        if color_value < 0.0:
            return 0.0
        elif color_value > 1.0:
            return 1.0
        else:
            return float(color_value)

    def get_brightness(self):
        """
        Calculates the relative luminance of the color.
        https://en.wikipedia.org/wiki/Relative_luminance

        :return: float, the brightness of the color about 0.0-254.9.
        """

        return (
            0.2126 * self.__red + 0.7152 * self.__green + 0.0722 * self.__blue
        )

    def brightness(self, brightness_amount):
        """
        Modify the luminance aka brightness of the color in relation to the
        colors original luminance amount. Maintains the colors original hue.

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

        :param tone_percentage: int, the percentage of toning to apply.
        :return: Color, the toned color.
        """

        if (
                not isinstance(tone_percentage, int)
                or 0 > tone_percentage > 100
        ):
            show_error('Invalid tone parameter received!')
            return

        tone_amount = tone_percentage / 100

        red_amount = self.__red / 255
        green_amount = self.__green / 255
        blue_amount = self.__blue / 255

        color_hsv = colorsys.rgb_to_hsv(red_amount, green_amount, blue_amount)
        saturation_amount = self.clamp_fraction_value(
            color_hsv[1] + (color_hsv[1] * tone_amount))

        toned_color_hsv = (color_hsv[0], saturation_amount, color_hsv[2])
        toned_rgb_color = colorsys.hsv_to_rgb(
            toned_color_hsv[0],
            toned_color_hsv[1],
            toned_color_hsv[2])

        toned_rgb_values = (
            self.clamp_rgb_value(toned_rgb_color[0] * 255),
            self.clamp_rgb_value(toned_rgb_color[1] * 255),
            self.clamp_rgb_value(toned_rgb_color[2] * 255)
        )

        self.__red = toned_rgb_values[0]
        self.__green = toned_rgb_values[1]
        self.__blue = toned_rgb_values[2]

        return self
