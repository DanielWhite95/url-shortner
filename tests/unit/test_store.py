import datetime
from url_shortner.config import AppSettings
from pymongo import MongoClient
import pytest
import pytest_asyncio
from url_shortner.model.url import MinifiedUrl
from url_shortner.store.base import URLStore
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from url_shortner.store.mongo import MongoStore

class MockedMongoDB:

    def __init__(self):
        self._stored_elements = {}

    async def find_one(self, query: dict):
        return self._stored_elements.get(query['slug'], None)

    async def insert_one(self, obj: dict) -> MinifiedUrl|None:
        self._stored_elements[obj['slug']] = obj

    async def delete_one(self,query: dict):
        if self._stored_elements.get(query['slug'], None):
            del self._stored_elements[query['slug']]

@patch(
    "url_shortner.store.mongo.AsyncMongoClient"
)
@pytest.mark.asyncio
async def test_mongo_store_uses_righ_db_collection(mock_mongo: AsyncMock):
    settings = AppSettings.instance()
    _ = MongoStore(settings.mongo_uri)
    mock_mongo.assert_called_once_with(settings.mongo_uri)
    mock_mongo.return_value.get_database.assert_called_once_with("skokka")
    mock_mongo.return_value.get_database.return_value.__getitem__.assert_called_once_with("minifiedUrls")

@patch(
    "url_shortner.store.mongo.AsyncMongoClient"
)
@pytest.mark.asyncio
async def test_mongo_store_use_right_query_for_existing_items(mock_mongo: AsyncMock):
    settings = AppSettings.instance()
    store = MongoStore(settings.mongo_uri)
    store._db_collection = AsyncMock()
    await store.get("slug123")
    store._db_collection.find_one.assert_called_once_with({"slug": "slug123"})


@patch(
    "url_shortner.store.mongo.AsyncMongoClient"
)
@pytest.mark.asyncio
async def test_mongo_store_extract_data_in_correct_form(mock_mongo: AsyncMock):
    settings = AppSettings.instance()
    store = MongoStore(settings.mongo_uri)
    store._db_collection = AsyncMock()
    now = datetime.datetime.now(datetime.UTC)
    mocked_value = {
        "originalUrl": "https://www.test.com",
            "slug": "slug123",
        "submissionDate": now.timestamp()
    }
    store._db_collection.find_one.return_value = mocked_value
    res = await store.get("slug123")
    assert res is not None
    assert type(res) == MinifiedUrl
    assert res.minified_slug == "slug123"
    assert res.original_url == "https://www.test.com"
    assert res.submission_time == now

@patch(
    "url_shortner.store.mongo.AsyncMongoClient"
)
@pytest.mark.asyncio
async def test_mongo_store_return_none_if_missing_data(mock_mongo: AsyncMock):
    settings = AppSettings.instance()
    store = MongoStore(settings.mongo_uri)
    store._db_collection = AsyncMock()
    now = datetime.datetime.now(datetime.UTC)
    store._db_collection.find_one.return_value = None
    res = await store.get("slug123")
    assert res is None


@patch(
    "url_shortner.store.mongo.AsyncMongoClient"
)
@pytest.mark.asyncio
async def test_mongo_store_store_data_in_the_right_format(mock_mongo: AsyncMock):
    settings = AppSettings.instance()
    store = MongoStore(settings.mongo_uri)
    store._db_collection = AsyncMock()
    submission_time = datetime.datetime.now()
    await store.store(MinifiedUrl(original_url="https://www.test.com", minified_slug="slug123", submission_time=submission_time))
    store._db_collection.insert_one.assert_called_once_with({"originalUrl": "https://www.test.com", "slug": "slug123", "submissionDate": submission_time.isoformat()})

@patch(
    "url_shortner.store.mongo.AsyncMongoClient"
)
@pytest.mark.asyncio
async def test_mongo_store_delete_the_right_data(mock_mongo: AsyncMock):
    settings = AppSettings.instance()
    store = MongoStore(settings.mongo_uri)
    store._db_collection = AsyncMock()
    exp_time = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp() + 5000)
    await store.delete(MinifiedUrl(original_url="https://www.test.com", minified_slug="slug123", submission_time=exp_time))
    store._db_collection.delete_one.assert_called_once_with({"slug": "slug123"})
