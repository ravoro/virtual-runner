from unittest import TestCase

import config
from app import create_app
from app.templates.utils.filters import asset_release_version


class TestAssetReleaseVersion(TestCase):
    def setUp(self):
        self.app = create_app(config.TestConfig)

    def test_no_config(self):
        """Return the original unchanged url when the "RELEASE_VERSION" config is not set."""
        with self.app.app_context():
            url = 'random-url'
            self.app.config['RELEASE_VERSION'] = None
            assert asset_release_version(url) == url

    def test_asset_version_in_url(self):
        """Return the url with the "RELEASE_VERSION" value added as url query parameter."""
        with self.app.app_context():
            url = 'random-url'
            version = 'random-version'
            self.app.config['RELEASE_VERSION'] = version
            assert asset_release_version(url) == '{}?v={}'.format(url, version)
