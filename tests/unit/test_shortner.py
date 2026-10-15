import pytest_asyncio
import pytest
from url_shortner.model.url import MinifiedUrl
from url_shortner.store.base import URLStore
from url_shortner.logic.shortner import UrlShortner


class MockedStore(URLStore):

    def  __init__(self):
        self._data = {}

    async def get(self, slug: str) -> MinifiedUrl|None:
        return self._data.get(slug, None)

    async def store(self, url: MinifiedUrl):
        self._data[url.minified_slug] = url

    async def delete(self, url: MinifiedUrl):
        if url.minified_slug in self._data[url.minified_slug]:
            del self._data[url.minified_slug]

@pytest.fixture()
def url_store() -> MockedStore:
    return MockedStore()

@pytest.mark.asyncio
async def test_shortner_store_url_when_short_code_is_created(url_store: MockedStore):
    shortner = UrlShortner(url_store)
    res = await shortner.shorten("https://www.test.com")
    assert res.minified_slug in url_store._data 
