import time
from datetime import datetime
from unittest import TestCase

from app.templates.utils.filters import format_date


class TestFormatDate(TestCase):
    def test_not_datetime(self):
        """Return the original input argument if the input is not of type `datetime`."""
        invalid_args = ["random string", "06 March 2017", str(datetime.now()), 1234, time.localtime()]
        for arg in invalid_args:
            assert format_date(arg) is arg

    def test_correct_format(self):
        """Return a human-friendly date string when given a `datetime`."""
        arg = datetime(2017, 3, 6)
        assert format_date(arg) == '06 March 2017'
