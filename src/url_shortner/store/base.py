import abc
from url_shortner.model.url import MinifiedUrl


class URLStore(abc.ABC):

    @abc.abstractmethod
    async def get(self, slug: str) -> MinifiedUrl|None:
        pass

    @abc.abstractmethod
    async def store(self, url: MinifiedUrl):
        pass


    @abc.abstractmethod
    async def delete(self, url: MinifiedUrl):
        pass
