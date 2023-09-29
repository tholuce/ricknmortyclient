from ricknmorty.clients import AbstractClient
from ricknmorty.mixins import (PaginationMixin, JsonFileMixin)
from datetime import datetime


class BaseService(JsonFileMixin, PaginationMixin):
    def __init__(self, client: AbstractClient, endpoint) -> None:
        self._client = client
        self._endpoint = endpoint

    def __get_results(self, response):
        if not response:
            return None
        return response.get('results') or []

    async def get_all(self):
        response = await self._client.aconnect(self._endpoint)
        results = self.__get_results(response)
        for page_number in range(2, self.get_page_count(response)):
            results += self.__get_results(await self._client.aconnect(f'{self._endpoint}?page={page_number}'))
        return results

    async def get_by_link(self, link):
        return await self._client.aconnect(link)


class EpisodeService(BaseService):
    def __init__(self, client: AbstractClient) -> None:
        super().__init__(client, 'episode')

    async def get_episodes_by_airred_date(self, start_date, end_date):
        filtered_episodes = []
        episodes = await self.get_all()
        for episode in episodes:
            characters = episode.get('characters')
            if not characters or len(characters) <= 3:
                continue
            air_date = episode.get('air_date')
            if not air_date:
                continue
            parsed_air_date = datetime.strptime(air_date, '%B %d, %Y')
            if parsed_air_date > start_date and parsed_air_date < end_date:
                filtered_episodes.append(episode['name'])
        return filtered_episodes


class LocationService(BaseService):
    def __init__(self, client: AbstractClient) -> None:
        super().__init__(client, 'location')

    async def __is_odd_episodes(self, location_data):
        for character_link in location_data.get('residents'):
            character_data = await self.get_by_link(character_link)
            for episode_link in character_data.get('episode'):
                episode = await self.get_by_link(episode_link)
                episode_number = int(episode.get('episode').split('E')[-1])
                if episode_number % 2 == 0:
                    return False
        return True

    async def get_by_odd_episode_number(self):
        return [location['name'] for location in await self.get_all() if await self.__is_odd_episodes(location)]


class CharacterService(BaseService):
    def __init__(self, client: AbstractClient) -> None:
        super().__init__(client, 'character')
