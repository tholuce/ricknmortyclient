import json
from typing import AnyStr, Callable, Union, Dict, List


class PaginationMixin:
    '''
        Mixin for endpoints with pagination
    '''

    def __get_page_info(self, response, key: AnyStr) -> Union[Dict, List, AnyStr, None]:
        '''
            gets page info
            :param response: response data to search for page info
            :param key: grabs specific data from page info
            :return: value if has such under key, otherwise - None
        '''
        page_info = response.get('info')
        if not page_info:
            return None
        return page_info.get(key)

    def get_page_count(self, response) -> int:
        '''
            gets page count
            :param response: response to get page count
            :return: page count. default: 0
        '''
        return (self.__get_page_info(response, 'pages') + 1) or 0


class JsonFileMixin:
    '''
        Mixin for data to write in json file
    '''
    async def to_json_file(self, filename: AnyStr, formatter: Union[Callable, None] = None) -> None:
        '''
            converts data to json file
            :param self: Object to be mixined
            :param formatter: formats results into desired schema
        '''
        response = await self.get_all()
        if formatter:
            response = formatter(response)
        with open(filename, 'w') as out_file:
            json.dump(response, out_file)
