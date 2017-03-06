from . import BaseCase


class TestJourneysAddPresent(BaseCase):
    def setUp(self):
        super().setUp()

        self.valid_request = {
            'method': 'GET',
            'path': '/journeys/add'
        }

    def test_empty_form(self):
        """Return 200 status and present an empty JourneysAddForm."""
        response = self.make_request()
        html = self.response_html(response)

        assert response.status_code == 200
        assert html.select_one("#content form input[name=name]").attrs['value'] is ''
        assert html.select_one("#content form input[name=start_lat]").attrs['value'] is ''
        assert html.select_one("#content form input[name=start_lng]").attrs['value'] is ''
        assert html.select_one("#content form input[name=finish_lat]").attrs['value'] is ''
        assert html.select_one("#content form input[name=finish_lng]").attrs['value'] is ''
