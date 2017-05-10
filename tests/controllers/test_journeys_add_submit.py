from unittest.mock import patch, Mock
from urllib.parse import urlparse

from app.repositories import JourneyRepo
from . import BaseCase, common_test_require_auth


class Test(BaseCase):
    def setUp(self):
        super().setUp()

        self.valid_data = {
            'name': 'random journey name',
            'start_lat': 0,
            'start_lng': 0,
            'finish_lat': 1,
            'finish_lng': 1,
            'distance_meters': 900
        }

        self.valid_request = {
            'method': 'POST',
            'path': '/journeys/add',
            'content_type': 'application/x-www-form-urlencoded',
            'data': self.valid_data
        }

    @common_test_require_auth
    def test_auth(self):
        pass

    def test_invalid_submission(self):
        """Return 400 status and re-present the page with JourneysAddForm errors."""
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = ''
        response = self.make_request_with_auth(data=invalid_data)
        html = self.response_html(response)

        assert response.status_code == 400
        assert "Please fix any errors below and try again" in html.select_one("#content form .alert").text

    @patch.object(JourneyRepo, 'add')
    def test_valid_submission(self, mock_add: Mock):
        """Return 302 status, add journey to db, and redirect to created journey's page when given valid submission."""
        journey = self.make_journey(**self.valid_data)
        mock_add.return_value = journey

        response = self.make_request_with_auth()

        assert mock_add.call_count is 1
        with self.test_client.session_transaction() as session:
            assert session['_flashes'][0][1] == 'Successfully created new journey.'
        assert response.status_code == 302
        assert urlparse(response.headers['location']).path == '/journeys/{}'.format(journey.id)
