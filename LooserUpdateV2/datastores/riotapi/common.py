from typing import MutableMapping, Any
import logging

from riotwatcher import LolWatcher, ApiError


class HTTPError(RuntimeError):
    def __init__(self, message, code = 400):
        super().__init__(message)
        self.code = code

class APIError(HTTPError):
    pass

class APIRequestError(ApiError):
    def __init__(self, message):
        self.code = int(message[:3])
        self.message = _ERROR_CODES.get(self.code, message)
        LOGGER.error(f"{self.code} {self.message}")
        super().__init__(f"{self.code} {self.message}")

class APINotFoundError(HTTPError):
    pass


_ERROR_CODES = {
    400: "Bad request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Data not found",
    405: "Method not allowed",
    415: "Unsupported media type",
    429: "Rate limit exceeded",
    500: "Internal server error",
    502: "Bad gateway",
    503: "Service unavailable",
    504: "Gateway timeout",
}

_RENAMED = {
    "platform": "region",
    "encryptedAccountId": "encrypted_account_id",
    "encryptedPUUID1": "encrypted_puuid",
    "encryptedPUUID2": "puuid",
    "encryptedSummonerId": "encrypted_summoner_id",
    "summonerName": "summoner_name",
    "matchId": "match_id",
}

LOGGER = logging.getLogger("riotapi")


class RiotAPIService():
    def __init__(
        self,
        api_key: str,
        client: LolWatcher = None,
    ):
        if client is None:
            self._client = LolWatcher(api_key)
        else:
            self._client = client

    def _get(
        self,
        baseapi: str,
        endpoint: str,
        parameters: MutableMapping[str, Any] = None,
    ):
        request = RiotAPIRequest(
            servise = self,
            baseapi = baseapi,
            endpoint = endpoint,
            parameters = parameters,
        )
        try:
            return request()
        except APIRequestError as error:
            raise APIError(str(error)) from error

class RiotAPIRequest(object):
    def __init__(
        self,
        servise: RiotAPIService,
        baseapi: str,
        endpoint: str,
        parameters: MutableMapping[str, Any] = None,
    ):
        self.servise = servise
        self.baseapi = baseapi
        self.endpoint = endpoint
        self.parameters = self._renamed(parameters)

    @staticmethod
    def _renamed(to_rename: MutableMapping[str, Any]):
        return {_RENAMED.get(k, k): v for k, v in to_rename.items()}

    def __call__(self):
        try:
            request = getattr(getattr(self.servise._client, self.baseapi), self.endpoint)
            return request(**self.parameters)
        except ApiError as error:
            raise APIRequestError(str(error)) from error
