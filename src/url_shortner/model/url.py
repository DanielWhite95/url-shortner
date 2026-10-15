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
    submission_time: datetime.datetime
