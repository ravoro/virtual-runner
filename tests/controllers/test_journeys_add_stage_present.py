from unittest.mock import patch, Mock
from urllib.parse import urlparse

from app.repositories import JourneyRepo
from . import BaseCase


class TestJourneysAddStagePresent(BaseCase):
    def setUp(self):
        super().setUp()

        self.valid_request = {
            'method': 'GET',
            'path': '/journeys/123/add-run'
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
    def test_completed(self, mock_get: Mock):
        """Return 302 status and redirect to the journey page when the journey is complete."""
        journey = self.make_journey()
        stage = self.make_stage(distance_meters=journey.distance_meters)
        journey.stages = [stage]
        mock_get.return_value = journey

        response = self.make_request()

        assert response.status_code == 302
        assert urlparse(response.headers['location']).path == '/journeys/{}'.format(journey.id)

    @patch.object(JourneyRepo, 'get')
    def test_empty_form(self, mock_get: Mock):
        """Return 200 status and present an empty JourneysAddStageForm when given invalid data."""
        mock_get.return_value = self.make_journey()

        response = self.make_request()
        html = self.response_html(response)

        assert response.status_code == 200
        assert html.select_one("#content form input[name=distance_meters]").attrs['value'] is ''
