from unittest.mock import patch

from app.repositories import JourneyRepo
from . import BaseCase


class TestJourneys(BaseCase):
    def setUp(self):
        super().setUp()

        self.valid_request = {
            'method': 'GET',
            'path': '/journeys'
        }

        self.html_journeys_selector = '#content table tbody tr'

    @patch.object(JourneyRepo, 'all_ordered')
    def test_no_journeys(self, mock_all_ordered):
        """Return 200 status and show text that there are no journeys."""
        mock_all_ordered.return_value = []

        response = self.make_request()
        html = self.response_html(response)
        html_journeys = html.select(self.html_journeys_selector)

        assert response.status_code == 200
        assert len(html_journeys) == 0
        assert "No journeys created." in html.select_one('#content').text

    @patch.object(JourneyRepo, 'all_ordered')
    def test_list_journeys(self, mock_all_ordered):
        """Return 200 status and show list of journeys."""
        journey1 = self.make_journey(id=1)
        journey2 = self.make_journey(id=2)
        mock_all_ordered.return_value = [journey1, journey2]

        response = self.make_request()
        html = self.response_html(response)
        html_journeys = html.select(self.html_journeys_selector)

        assert response.status_code == 200
        assert len(html_journeys) == 2
