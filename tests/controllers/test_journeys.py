from unittest.mock import patch, Mock
from urllib.parse import urlparse

from app.repositories import JourneyRepo, StageRepo
from . import BaseCase


class Test(BaseCase):
    def setUp(self):
        super().setUp()

        self.valid_request = {
            'method': 'GET',
            'path': '/journeys'
        }

        self.html_journeys_selector = '#content #journeys-table tbody tr'

    def test_unauthed(self):
        """Return 302 status and redirect to /login when user is not logged in."""
        response = self.make_request()
        assert response.status_code == 302
        assert urlparse(response.headers['location']).path == '/login'

    @patch.object(StageRepo, 'total_distance')
    @patch.object(JourneyRepo, 'all_ordered')
    def test_no_journeys(self, mock_all_ordered: Mock, mock_total_distance: Mock):
        """Return 200 status and show text that there are no journeys."""
        mock_all_ordered.return_value = []
        mock_total_distance.return_value = 0

        response = self.make_request_with_auth()
        html = self.response_html(response)
        html_journeys = html.select(self.html_journeys_selector)

        assert response.status_code == 200
        assert len(html_journeys) == 0
        assert "No journeys created." in html.select_one('#content').text

    @patch.object(StageRepo, 'total_distance')
    @patch.object(JourneyRepo, 'all_ordered')
    def test_list_journeys(self, mock_all_ordered: Mock, mock_total_distance: Mock):
        """Return 200 status and show list of journeys."""
        journey1 = self.make_journey(id=1)
        journey2 = self.make_journey(id=2)
        mock_all_ordered.return_value = [journey1, journey2]
        mock_total_distance.return_value = 0

        response = self.make_request_with_auth()
        html = self.response_html(response)
        html_journeys = html.select(self.html_journeys_selector)

        assert response.status_code == 200
        assert len(html_journeys) == 2

    @patch.object(StageRepo, 'total_distance')
    @patch.object(JourneyRepo, 'all_ordered')
    def test_list_journeys(self, mock_all_ordered: Mock, mock_total_distance: Mock):
        """Display total distance stats."""
        mock_distance = 567.89
        mock_all_ordered.return_value = [self.make_journey()]
        mock_total_distance.return_value = mock_distance

        response = self.make_request_with_auth()
        html = self.response_html(response)

        assert str(mock_distance) in html.select_one('#content').text
