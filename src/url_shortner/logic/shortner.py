import datetime
from url_shortner.model.url import MinifiedUrl
from url_shortner.store.base import URLStore
import hashlib

class UrlShortner:
    """
    This class contains the logic to convert a standard URL into a short code to store in the app DB.
    To improve the User Experience, the short code is 6-chars long.
    To reduce the collision, a predefined value may be appended to the original string to produce the short-code, but it will not be exposed to the user
        """

    def __init__(self, db: URLStore, exp_time: int = 5000):
        self._url_store  = db
        self._salt = "myurlshortner_123"
        self._code_length = 6
        self._exp_time = datetime.timedelta(milliseconds=exp_time)

    async def shorten(self, url: str) -> MinifiedUrl:
        """
        Generates a short code from a user url using SHA256 hash function and the predefined salt to avoid collisions.

        It uses the DB to check for collisions and store the new code when generated
        """
        attempt = 0
        while True:
            url_to_hash = url + (self._salt * attempt if attempt > 0 else "")
            hash = hashlib.sha256(url_to_hash.encode())
            short_code = hash.hexdigest()[:self._code_length]
            # Check for collision
            collision = await self._url_store.get(short_code)
            if collision is None:
                now = datetime.datetime.now(datetime.UTC)
                minified_url = MinifiedUrl(
                    original_url=url,
                    minified_slug=short_code,
                    expiration_time=now + self._exp_time
    )
                await self._url_store.store(minified_url)
                return minified_url  # Return the generated short URL
            else:
                attempt += 1



