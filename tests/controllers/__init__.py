from unittest import TestCase

from bs4 import BeautifulSoup
from flask import Response

import config
from app import create_app
from app.models import Journey, Stage


class BaseCase(TestCase):
    def setUp(self):
        self.app = create_app(config.TestConfig)
        self.test_client = self.app.test_client()

    def make_request(self, **kwargs) -> Response:
        """Make a request based on self.valid_request (overwrite any values with **kwargs) and return the response."""
        request = {**self.valid_request, **kwargs}
        response = self.test_client.open(**request)
        return response

    @staticmethod
    def make_journey(**kwargs) -> Journey:
        base_vals = {
            'id': 123,
            'name': 'random journey name',
            'distance_meters': 12345,
            'start_lat': 2.3,
            'start_lng': 3.4,
            'finish_lat': 4.5,
            'finish_lng': 5.6
        }
        vals = {**base_vals, **kwargs}
        return Journey(**vals)

    @staticmethod
    def make_stage(**kwargs) -> Stage:
        base_vals = {
            'id': 123,
            'distance_meters': 12345
        }
        vals = {**base_vals, **kwargs}
        return Stage(**vals)

    @staticmethod
    def response_html(response: Response) -> BeautifulSoup:
        """Return response body as parsed html (i.e. BeautifulSoup object)."""
        return BeautifulSoup(response.get_data(as_text=True), 'html.parser')
