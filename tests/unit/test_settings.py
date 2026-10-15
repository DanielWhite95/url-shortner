from url_shortner.config import AppSettings
import os
import unittest
from unittest.mock import patch


class TestAppSettings(unittest.TestCase):

    @patch.dict(os.environ, {
               "MONGODB_URI":"mongodb://127.0.0.1:32768/?directConnection=true",
               "APP_DOMAIN":"myurlshortner",
               "URL_EXPIRATION_TIME":"3000",
    })
    def test_app_settings_read_info_from_env(self):
        AppSettings._instance = None
        settings = AppSettings.instance()
        self.assertEqual(settings.app_domain, "myurlshortner")
        self.assertEqual(settings.mongo_uri, "mongodb://127.0.0.1:32768/?directConnection=true")
        self.assertEqual(settings.url_exp_time, 3000)

    @patch.dict(os.environ, {
               "MONGODB_URI":"mongodb://127.0.0.1:32768/?directConnection=true",
               "APP_DOMAIN":"myurlshortner",
    }, clear=True)
    def test_app_settings_use_default_expiration_on_missing_env(self):
        AppSettings._instance = None
        settings = AppSettings.instance()
        self.assertEqual(settings.app_domain, "myurlshortner")
        self.assertEqual(settings.mongo_uri, "mongodb://127.0.0.1:32768/?directConnection=true")
        self.assertEqual(settings.url_exp_time, 5000)
