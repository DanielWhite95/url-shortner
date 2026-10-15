from url_shortner.logic.shortner import UrlShortner
import url_shortner
import time
import datetime
from url_shortner.model.url import MinifiedUrl
import asyncio
from url_shortner.config import AppSettings
from url_shortner.store.mongo import MongoStore
from cmath import exp
import sys
import os
from typing import ClassVar, Self
import dataclasses
import pymongo
import json
import hashlib
import argparse
import base64
from urllib.parse import urlparse

settings = AppSettings.instance()

async def expand_url(url_to_expand: str, db: MongoStore):
    if not url_to_expand.strip().startswith(f"https://{settings.app_domain}"):
        print("Invalid Url provided!")
        return

    url = urlparse(url_to_expand.strip())
    print("Parsed URL: ", url)

    if url.netloc != settings.app_domain:
        print("Url not found!")
        return

    short_code = (url.path or "").lstrip("/")
    orig_url = await db.get(short_code)
    if orig_url is None:
        print("Url not found!")
        return

    if orig_url.is_expired():
        print("Url expired! Will be deleted. Please create it again")
        await db.delete(orig_url)
        return


    print("Expanded url: ")
    print(f"https://{settings.app_domain}/{orig_url.minified_slug}")

async def minify_url(url_to_minify: str, db: MongoStore):
    url_shortner = UrlShortner(db, settings.url_exp_time)
    minified_url = await url_shortner.shorten(url_to_minify)
    await db.store(minified_url)
    print("Url stored. Minfied url:")
    print(f"https://{settings.app_domain}/{minified_url.minified_slug}")

async def main():
    arg_parser = argparse.ArgumentParser("url-shortner",)
    arg_parser.add_argument("--minify", type=str)
    arg_parser.add_argument("--expand", type=str)
    args = arg_parser.parse_args()
    url_to_minify = args.minify
    url_to_expand = args.expand
    if url_to_expand is None and url_to_minify is None:
        print("At least one between minify and expand parameters must be specified")
        sys.exit(1)
    if url_to_expand is not None and url_to_minify is not None:
        print("Only one between minify and expand parameters can be specified")
        sys.exit(1)
    async with MongoStore(settings.mongo_uri) as db:
        if url_to_expand is not None:
            await expand_url(url_to_expand, db)
        else:
            await minify_url(url_to_minify, db)
        return


if __name__ == "__main__":
    asyncio.run(main())
