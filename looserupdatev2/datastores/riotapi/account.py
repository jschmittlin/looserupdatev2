from typing import MutableMapping, Any

from .common import RiotAPIService, APIError, APINotFoundError
from ...dto.account import AccountDto


class AccountApi(RiotAPIService):
    """
    ACCOUNT-V1
    League of Legends
    """
    def get_account(
        self, query: MutableMapping[str, Any]
    ) -> AccountDto:
        """
        Get account.

        :param dict query:  Query parameters for the request:
                            - region:        Region
                            - puuid:         Encrypted summoner ID. Max length 63 characters.
                            - (or) gameName: This field may be excluded from the response if the account doesn't have a gameName.
                            - (and) tagLine: This field may be excluded from the response if the account doesn't have a tagLine.

        :return: AccountDTO:
        """
        region = query["region"]
        continent: Continent = region.continent
        if "puuid" in query:
            url = "https://{continent}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}".format(
                continent=continent.value.lower(), puuid=query["puuid"],
            )
        if "gameName" in query and "tagLine" in query:
            url = "https://{continent}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}".format(
                continent=continent.value.lower(), gameName=query["gameName"], tagLine=query["tagLine"],
            )

        try:
            data = self._get(url, {})
        except APINotFoundError as error:
            raise APINotFoundError(str(error)) from error

        data["region"] = query["region"].value
        return AccountDto(data)
