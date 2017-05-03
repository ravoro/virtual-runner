from unittest.mock import patch, Mock
from urllib.parse import urlparse

from app.repositories import JourneyRepo, StageRepo
from . import BaseCase


class Test(BaseCase):
    def setUp(self):
        super().setUp()

        self.valid_data = {
            'distance_meters': 1234
        }

        self.valid_request = {
            'method': 'POST',
            'path': '/journeys/123/add-run',
            'content_type': 'application/x-www-form-urlencoded',
            'data': self.valid_data
        }

    @patch.object(JourneyRepo, 'get')
    def test_not_found(self, mock_get: Mock):
        """Return 404 status and show error page when no journey matches the given id."""
        mock_get.return_value = None

        response = self.make_request()
        html = self.response_html(response)

        assert response.status_code == 404
        assert "Not Found" in html.select_one('h1').text

    @patch.object(StageRepo, 'all_ordered')
    @patch.object(JourneyRepo, 'get')
    def test_completed(self, mock_get: Mock, mock_all_ordered: Mock):
        """Return 302 status and redirect to the journey page when the journey is complete."""
        journey = self.make_journey()
        final_stage = self.make_stage(distance_meters=journey.distance_meters)
        journey.stages = [final_stage]
        mock_get.return_value = journey
        mock_all_ordered.return_value = [final_stage]

        response = self.make_request()

        assert response.status_code == 302
        assert urlparse(response.headers['location']).path == '/journeys/{}'.format(journey.id)

    @patch.object(StageRepo, 'all_ordered')
    @patch.object(JourneyRepo, 'get')
    def test_invalid_submission(self, mock_get: Mock, mock_all_ordered: Mock):
        """Return 400 status and re-present the page with JourneysAddStageForm errors when given invalid data."""
        journey = self.make_journey()
        mock_get.return_value = journey
        mock_all_ordered.return_value = None

        invalid_data = self.valid_data.copy()
        invalid_data['distance_meters'] = ''
        response = self.make_request(data=invalid_data)
        html = self.response_html(response)

        assert response.status_code == 400
        assert "Please fix any errors below and try again" in html.select_one("#content form .alert").text

    @patch.object(StageRepo, 'create')
    @patch.object(StageRepo, 'all_ordered')
    @patch.object(JourneyRepo, 'get')
    def test_non_final_stage(self, mock_get: Mock, mock_all_ordered: Mock, mock_create: Mock):
        """Return 302 status, save stage to db, and redirect to journey's page when adding a non-final stage."""
        journey = self.make_journey()
        mock_get.return_value = journey
        mock_all_ordered.return_value = None

        response = self.make_request()

        assert mock_create.call_count is 1
        with self.test_client.session_transaction() as session:
            assert session['_flashes'][0][1] == 'Successfully added new run.'
        assert response.status_code == 302
        assert urlparse(response.headers['location']).path == '/journeys/{}/panorama'.format(journey.id)

    @patch.object(StageRepo, 'create')
    @patch.object(StageRepo, 'all_ordered')
    @patch.object(JourneyRepo, 'get')
    def test_final_stage_message(self, mock_get: Mock, mock_all_ordered: Mock, mock_create: Mock):
        """Display custom flash message when submitting the final stage."""
        journey = self.make_journey()
        mock_get.return_value = journey
        mock_all_ordered.return_value = None

        final_stage = self.valid_data.copy()
        final_stage['distance_meters'] = journey.distance_meters
        response = self.make_request(data=final_stage)

        with self.test_client.session_transaction() as session:
            assert 'You\'ve completed the journey' in session['_flashes'][0][1]
            assert '</iframe>' in session['_flashes'][0][1]
