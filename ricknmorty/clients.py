from aiohttp.client import ClientSession
from urllib.parse import urljoin
from typing import AnyStr
from abc import ABC, abstractmethod


class AbstractClient(ABC):

    @abstractmethod
    async def aconnect(self, endpoint: AnyStr, **kargs):
        ...


class GetClient(AbstractClient):
    def __init__(self, base_url: AnyStr) -> None:
        self._base_url: AnyStr = base_url

    def __get_absolute_url(self, endpoint) -> AnyStr:
        '''
            get absolute url
            :param endpoint: relative or absolute endpoint url. If absolute endpoint then it will not concatenete
            :return: absolute url for endpoint
        '''
        return urljoin(self._base_url, endpoint)

    async def aconnect(self, endpoint, **kargs):
        '''
            sends http requests and gets reponse in json format
            :param endpoint: specific endpoint to reuqest for
            :param kargs: payload data to request
            :return: http responss in json format
        '''
        async with ClientSession() as session:
            async with session.get(self.__get_absolute_url(endpoint), **kargs) as response:
                return await response.json()
