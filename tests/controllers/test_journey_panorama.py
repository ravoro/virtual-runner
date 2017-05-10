from unittest.mock import patch, Mock

from app.repositories import JourneyRepo, StageRepo
from . import BaseCase, common_test_require_auth


class Test(BaseCase):
    def setUp(self):
        super().setUp()

        self.valid_request = {
            'method': 'GET',
            'path': '/journeys/123/panorama'
        }

        self.journey = self.make_journey(id=543, name="random journey name")

        self.html_stages_selector = '#journey-details-modal table tbody tr'

    @common_test_require_auth
    def test_auth(self):
        pass

    @patch.object(JourneyRepo, 'get')
    def test_not_found(self, mock_get: Mock):
        """Return 404 status and show error page when no journey matches the given id."""
        mock_get.return_value = None

        response = self.make_request_with_auth()
        html = self.response_html(response)

        assert response.status_code == 404
        assert "Not Found" in html.select_one('h1').text

    @patch.object(StageRepo, 'all_ordered')
    @patch.object(JourneyRepo, 'get')
    def test_panorama(self, mock_get: Mock, mock_all_ordered: Mock):
        """Return 200 status and show page with journey panorama."""
        mock_get.return_value = self.journey
        mock_all_ordered.return_value = []

        response = self.make_request_with_auth()
        html = self.response_html(response)

        assert response.status_code == 200
        assert 'page-journey-panorama' == html.select_one('body').attrs['id']
