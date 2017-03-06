from unittest import TestCase

from app.templates.utils.filters import meters_to_km


class TestMetersToKm(TestCase):
    def test_not_int(self):
        """Return the original input argument if the input is not of type `int`."""
        invalid_args = ["random string", "123", 123.5]
        for arg in invalid_args:
            assert meters_to_km(arg) is arg

    def test_convert_to_km(self):
        """Return a km representation (with 2 decimal points) of a distance in meters."""
        assert meters_to_km(100) == "0.10"
        assert meters_to_km(494) == "0.49"
        assert meters_to_km(495) == "0.49"
        assert meters_to_km(496) == "0.50"
        assert meters_to_km(10000) == "10.00"
        assert meters_to_km(10200) == "10.20"
