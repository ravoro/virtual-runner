from unittest.mock import patch, Mock

from app.repositories import JourneyRepo, StageRepo
from . import BaseCase


class Test(BaseCase):
    def setUp(self):
        super().setUp()

        self.valid_request = {
            'method': 'GET',
            'path': '/journeys/123'
        }

        self.journey = self.make_journey(id=543, name="random journey name")

        self.html_stages_selector = '#journey-details-modal table tbody tr'

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
    def test_journey_details(self, mock_get: Mock, mock_all_ordered: Mock):
        """Return 200 status and show page with journey details."""
        mock_get.return_value = self.journey
        mock_all_ordered.return_value = []

        response = self.make_request()
        html = self.response_html(response)

        assert response.status_code == 200
        assert self.journey.name in html.select_one('title').text

    @patch.object(StageRepo, 'all_ordered')
    @patch.object(JourneyRepo, 'get')
    def test_no_stages(self, mock_get: Mock, mock_all_ordered: Mock):
        """Return 200 status and show journey details with no stages."""
        mock_get.return_value = self.journey
        mock_all_ordered.return_value = []

        response = self.make_request()
        html = self.response_html(response)
        html_stages = html.select(self.html_stages_selector)

        assert len(html_stages) == 0
        assert "You have not added any runs." in html.select_one('#journey-details-modal').text

    @patch.object(StageRepo, 'all_ordered')
    @patch.object(JourneyRepo, 'get')
    def test_with_stages(self, mock_get: Mock, mock_all_ordered: Mock):
        """Return 200 status and show journey details page with stages."""
        mock_get.return_value = self.journey
        stage1 = self.make_stage(id=1)
        stage2 = self.make_stage(id=2)
        mock_all_ordered.return_value = [stage1, stage2]

        response = self.make_request()
        html = self.response_html(response)
        html_stages = html.select(self.html_stages_selector)

        assert len(html_stages) == 2
