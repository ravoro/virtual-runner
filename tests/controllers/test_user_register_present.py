from . import BaseCase, common_test_require_anonymous


class Test(BaseCase):
    def setUp(self):
        super().setUp()

        self.valid_request = {
            'method': 'GET',
            'path': '/register'
        }

    @common_test_require_anonymous
    def test_auth(self):
        pass

    def test_empty_form(self):
        """Return 200 status and present an empty UserRegisterForm."""
        response = self.make_request()
        html = self.response_html(response)

        assert response.status_code == 200
        assert html.select_one("#content form input[name=email_or_username]").attrs['value'] is ''
        assert html.select_one("#content form input[name=password]").attrs['value'] is ''
