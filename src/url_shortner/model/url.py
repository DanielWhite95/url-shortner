import secrets
import base64
from url_shortner.config import AppSettings
from typing import Self
import datetime
from dataclasses import dataclass
import hashlib

@dataclass
class MinifiedUrl:
    original_url: str
    minified_slug: str
    expiration_time: datetime.datetime

    def is_expired(self) -> bool:
        now = datetime.datetime.now(datetime.UTC)
        print("Now: ", now)
        print("Expiration Time: ", self.expiration_time)
        return now >= self.expiration_time

