from . import BaseCase, common_test_require_anonymous


class Test(BaseCase):
    def setUp(self):
        super().setUp()

        self.valid_request = {
            'method': 'GET',
            'path': '/'
        }

    @common_test_require_anonymous
    def test_auth(self):
        pass

    def test_ok(self):
        """Return 200 status and display the home page."""
        response = self.make_request()
        html = self.response_html(response)
        assert response.status_code == 200
        assert 'page-home' == html.select_one("body").attrs['id']
