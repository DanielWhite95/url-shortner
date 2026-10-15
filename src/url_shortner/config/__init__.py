import os
from typing import ClassVar, Self
import dataclasses

@dataclasses.dataclass(frozen=True)
class AppSettings:
    """
    Simple Wrapper around application settings read from environment variables

    ```python
        settings = AppSettings.instance()
        ...
    ```
    """
    _instance: ClassVar[Self|None] = None
    app_domain: str
    mongo_uri: str
    url_exp_time: int

    @classmethod
    def instance(cls) -> Self:
        """
        Access singleton class instance. It should be the only way to instantiate this class
        """
        if cls._instance:
            return cls._instance


        app_domain = os.getenv('APP_DOMAIN') or "myurlshortner"
        mongo_uri = os.getenv('MONGODB_URI')
        if mongo_uri is None:
            raise RuntimeError("Missing Mongo URI connection")
        url_exp_time = int(os.getenv('URL_EXPIRATION_TIME') or "5000")
        cls._instance = cls(app_domain, mongo_uri, url_exp_time)
        return cls._instance
