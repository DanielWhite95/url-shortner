from unittest.mock import patch, MagicMock
import pytest
from url_shortner.model.url import MinifiedUrl
import datetime

@patch(
    "url_shortner.model.url.datetime"
)
def test_minified_url_compute_correct_expiration_time(datetime_mock: MagicMock):
    now = datetime.datetime.now(datetime.UTC)
    datetime_mock.datetime.now.return_value = now

    expired_url = MinifiedUrl("https://www.expired.com", "expired123", now - datetime.timedelta(hours=1))
    assert expired_url.is_expired() == True

    not_expired_url = MinifiedUrl("https://www.expired.com", "expired123", now + datetime.timedelta(hours=1))
    assert not_expired_url.is_expired() == False

    just_expired_url = MinifiedUrl("https://www.expired.com", "expired123", now)
    assert just_expired_url.is_expired() == True

