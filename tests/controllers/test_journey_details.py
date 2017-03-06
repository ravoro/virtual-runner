from unittest.mock import patch, Mock

from app.repositories import JourneyRepo
from . import BaseCase


class TestJourneyDetails(BaseCase):
    def setUp(self):
        super().setUp()

        self.valid_request = {
            'method': 'GET',
            'path': '/journeys/123'
        }

    @patch.object(JourneyRepo, 'get')
    def test_not_found(self, mock_get: Mock):
        """Return 404 status and show error page when no journey matches the given id."""
        mock_get.return_value = None

        response = self.make_request()
        html = self.response_html(response)

        assert response.status_code == 404
        assert "Not Found" in html.select_one('h1').text

    @patch.object(JourneyRepo, 'get')
    def test_journey_details(self, mock_get: Mock):
        """Return 200 status and show page with journey details."""
        journey = self.make_journey()
        mock_get.return_value = journey

        response = self.make_request()
        html = self.response_html(response)

        assert response.status_code == 200
        assert journey.name in html.select_one('title').text
