from pymongo.errors import CollectionInvalid
from url_shortner.config import AppSettings
from pymongo import AsyncMongoClient
from typing import override
import asyncio
import datetime
from url_shortner.model.url import MinifiedUrl
from url_shortner.store.base import URLStore

settings = AppSettings.instance()

class MongoStore(URLStore):
    def __init__(self, db_uri: str):
        self._db_uri = db_uri
        self._db_client = AsyncMongoClient(self._db_uri) 
        self._db_collection = self._db_client.get_database("skokka")['minifiedUrls']
    
    async def connect(self, db_uri: str):
        """
        Preferred method to connect to MongoDB.
        It instantiate the class and create the required MongoDB collection to be used
        """
        try:
            await self._db_client.get_database("skokka").create_collection("minifiedUrls", timeseries={"timeField": "submissionDate"}, expireAfterSeconds=settings.url_exp_time)
        except CollectionInvalid as coll_err:
            if coll_err._message == "collection minifiedUrls already exists":
                return
            raise coll_err



    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        await self._db_client.close()

    @override
    async def get(self, slug:str) -> MinifiedUrl|None:
        res  = await self._db_collection.find_one({"slug": slug})
        if res is None:
            return None
        return MinifiedUrl(
            original_url=res['originalUrl'],
            minified_slug=res['slug'],
            submission_time=res['submissionDate']
        )


    async def store(self, url: MinifiedUrl):
        await self._db_collection.insert_one(
            {
                "originalUrl": url.original_url,
                "submissionDate": url.submission_time,
                "slug": url.minified_slug
            }
        )

    async def delete(self, url: MinifiedUrl):
        await self._db_collection.delete_one(
            { "slug": url.minified_slug }
        )

    async def close(self):
        await self._db_client.close()
