from typing import MutableMapping, Mapping, Optional, Any
import requests
import logging
import os

from ..data import Region, Platform
from ..datastores.riotapi import RiotAPI

import json


LOGGER = logging.getLogger("looserupdatev2.core")
RIOT = RiotAPI()

ddragon = {"version": "", "cache": {}}

def get_latest_version() -> str:
    try:
        latest_version = requests.get("http://ddragon.leagueoflegends.com/api/versions.json").json()[0]
        LOGGER.info(f"Latest version from Data Dragon API: {latest_version}")
    except requests.exceptions.RequestException as error:
        latest_version = ""
        LOGGER.error(f"Unable to retrieve the latest version from Data Dragon API: {error}")

    return latest_version

def get_data_dragon(file: str) -> Mapping[str, Any]:
    url = "http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/{file}".format(
        version=ddragon["version"], file=file,
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        ddragon["cache"][file] = response.json()
        LOGGER.info(f"Data Dragon cache updated for {file}")
    except requests.exceptions.RequestException as error:
        LOGGER.error(f"Unable to update Data Dragon cache for {file}: {error}")

    return ddragon["cache"][file]

# only use for arena augment
def get_data_cdragon(file: str) -> Mapping[str, Any]:
    url = "https://raw.communitydragon.org/latest/cdragon/arena/en_us.json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        ddragon["cache"][file] = response.json()
        LOGGER.info(f"Data Dragon cache updated for {file}")
    except requests.exceptions.RequestException as error:
        LOGGER.error(f"Unable to update Data Dragon cache for {file}: {error}")

    return ddragon["cache"][file]

class CoreData(object):
    @property
    def _renamed(cls) -> Mapping[str, str]:
        pass

    def __init__(self, **kwargs):
        self(**kwargs)

    def __call__(self, **kwargs):
        for key, value in kwargs.items():
            new_key = self._renamed.get(key, key)
            setattr(self, new_key, value)
        return self

class LolObject(object):
    _renamed = {}
    
    def __init__(self, **kwargs):
        self._data = {_type: None for _type in self._data_types}
        results = {_type: {} for _type in self._data_types}

        for _type in self._data_types:
            if issubclass(_type, CoreData):
                if hasattr(_type, "_api"):
                    results[_type] = self.request_api(_type._api, _type._dto_type, kwargs)
                elif hasattr(_type, "_file"):
                    results[_type] = self.from_json(_type._file)
                else:
                    results[_type] = kwargs
                

        for _type, insert_this in results.items():
            if self._data[_type] is not None:
                self._data[_type] = self._data[_type](**insert_this)
            else:
                self._data[_type] = _type(**insert_this)

    def __str__(self) -> str:
        result = {}
        for _type, data in self._data.items():
            result[str(_type)] = str(data)
        return str(result)

    def request_api(
        self, api_name: str = None, dto: Mapping[str, Any] = None, query: MutableMapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        from ..dto.championmastery import ChampionMasteryListDto
        from ..dto.match import MatchListDto
        
        if api_name is None:
            return query

        if "region" in query:
            query["platform"] = Platform.from_region(Region(query["region"]))

        api = RIOT.services.get(api_name)

        if not api:
            raise ValueError(f"API for {api_name} not found")

        api_methods = {
            "AccountAPI": lambda kwargs: api.get_account(kwargs),
            "SummonerAPI": lambda kwargs: api.get_summoner(kwargs),
            "LeagueAPI": lambda kwargs: api.get_league_entries_by_summoner(kwargs),
            "ChampionMasteryAPI": lambda kwargs: (
                api.get_champion_mastery_list(kwargs) if issubclass(ChampionMasteryListDto, dto) else api.get_champion_mastery_score(kwargs)
            ),
            "ChallengesAPI": lambda kwargs: api.get_player_data(kwargs),
            "MatchAPI": lambda kwargs: (
                api.get_match_list(kwargs) if issubclass(MatchListDto, dto) else api.get_match(kwargs)
            ),
        }

        api_method = api_methods.get(api_name, None)

        if api_method:
            try:
                response = api_method(query)
            except Exception as error:
                raise Exception(f"{api_name}: {error}") from error
        else:
            raise ValueError(f"Method for {api_name} not defined")

        # response = self._clear(response, dto._dict)

        return response

    def _clear(
        self, data: MutableMapping[str, Any] = None, dto: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        if data is None:
            return {}

        if not isinstance(data, (dict, list)):
            if not isinstance(dto, (dict, list)):
                return data if isinstance(data, dto) else None
            elif isinstance(dto, dict):
                return {key: data for key, value_type in dto.items() if isinstance(data, value_type)}

        if isinstance(data, dict):
            return {
                key: (
                    self._clear(data.get(key), value_type) if isinstance(value_type, dict)
                    else [self._clear(item, value_type[0]) for item in data[key]] if isinstance(value_type, list) and key in data and isinstance(value_type[0], dict)
                    else [item for item in data[key] if isinstance(item, value_type[0])] if isinstance(value_type, list) and key in data
                    else data[key] if key in data and isinstance(data[key], value_type)
                    else None
                )
                for key, value_type in dto.items()
            }
        elif isinstance(data, list):
            return {key: [self._clear(item, value_type[0]) for item in data] for key, value_type in dto.items()}

        return {}

    def to_json(
        self, file: Optional[str] = None, data: Mapping[str, Any] = None,
    ) -> None:
        assert data
        if file is None:
            for _type in self._data_types: file = _type._file
        file_name = os.path.join(os.path.dirname(__file__), "../datastores/data", file)
        with open(file_name, "w") as json_file:
            json.dump(data, json_file)
    
    def from_json(
        self, file: Optional[str] = None,
    ) -> Mapping[str, Any]:
        if file is None:
            for _type in self._data_types: file = _type._file
        file_name = os.path.join(os.path.dirname(__file__), "../datastores/data", file)
        with open(file_name, "r") as json_file:
            data = json.load(json_file)
            return data
