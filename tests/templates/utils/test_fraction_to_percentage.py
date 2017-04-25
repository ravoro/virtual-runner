from unittest import TestCase

from app.templates.utils.filters import fraction_to_percentage


class Test(TestCase):
    def test_not_number(self):
        """Return the original input argument if the input is not of type `int` or `float`."""
        invalid_args = ["random string", "123", "123.5"]
        for arg in invalid_args:
            assert fraction_to_percentage(arg) is arg

    def test_convert_to_percentage(self):
        """Return a percentage representation (with 2 decimal points) of a fraction."""
        assert fraction_to_percentage(.1) == "10.00"
        assert fraction_to_percentage(.49994) == "49.99"
        assert fraction_to_percentage(.49995) == "49.99"
        assert fraction_to_percentage(.49996) == "50.00"
        assert fraction_to_percentage(1) == "100.00"
        assert fraction_to_percentage(1.23) == "100.00"

