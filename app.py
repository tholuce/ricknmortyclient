import asyncio
from ricknmorty.clients import GetClient
from ricknmorty.services import (
    EpisodeService, CharacterService, LocationService)
from ricknmorty.formatters import json_results_formatter
from datetime import datetime


client = GetClient('https://rickandmortyapi.com/api/')
episode_service = EpisodeService(client)
character_service = CharacterService(client)
location_service = LocationService(client)


async def aget_all_data_to_json():
    '''
        Gets all characters, episodes and locations to josn files respectively
    '''
    print('Generating files for all episodes, characters and locations...')
    await episode_service.to_json_file('episodes.json', json_results_formatter)
    await character_service.to_json_file('characters.json', json_results_formatter)
    await location_service.to_json_file('locations.json', json_results_formatter)
    print('Done generating json files')


async def aget_episodes_by_air_date():
    print('Getting episodes by air dates between 2017 and 2021 and more than 3 characters')
    start_date = datetime(2017, 1, 1)
    end_date = datetime(2021, 1, 1)
    print('Episodes from 2017 to 2021 with more than 3 characters are: ' + ', '.join(await episode_service.get_episodes_by_airred_date(start_date, end_date)))


async def aget_locations_by_odd_episodes():
    print('Getting locations by odd episodes')
    print('Locations with odd episdeos are: ' + ', '.join(await location_service.get_by_odd_episode_number()))


async def main():
    print('Start')
    await asyncio.gather(aget_all_data_to_json(), aget_episodes_by_air_date(),
                         aget_locations_by_odd_episodes())
    print('Done')

if __name__ == '__main__':
    asyncio.run(main())
