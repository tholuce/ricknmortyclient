from typing import List
from ricknmorty.dtos import JsonItem
from uuid import uuid4


def json_results_formatter(results: List) -> List:
    '''
        Formats result into other json schema
        :param results: list of results to be formatted
        :return: list of results with desired schema
    '''
    return [JsonItem(id=str(uuid4()), metadata=result_item['name'],
                     raw=result_item).__dict__ for result_item in results]
