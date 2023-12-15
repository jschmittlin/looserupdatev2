from typing import MutableMapping, Any, Union

from ..common import HTTPClient, HTTPError

class APIRequestError(HTTPError):
    pass

class APIError(HTTPError):
    pass

class APINotFoundError(HTTPError):
    pass

class APIForbiddenError(APINotFoundError):
    pass

_ERROR_CODES = {
    400: APIRequestError,
    401: APIRequestError,
    403: APIForbiddenError,
    404: APINotFoundError,
    405: APIRequestError,
    415: RuntimeError,
    429: RuntimeError,
    500: APIError,
    502: APIError,
    503: APIError,
    504: APIError,
}


class RiotAPIService():
    def __init__(
        self,
        api_key: str,
        http_client: HTTPClient = None,
    ):
        if http_client is None:
            self._client = HTTPClient()
        else:
            self._client = http_client

        self._headers = {"X-Riot-Token": api_key}

    def _get(
        self,
        url: str,
        parameters: MutableMapping[str, Any] = None,
    ) -> Union[dict, list, Any]:
        request = RiotAPIRequest(
            servise=self,
            url=url,
            parameters=parameters,
        )
        try:
            return request()
        except HTTPError as error:
            error_type = _ERROR_CODES[error.code]
            if error_type is RuntimeError:
                new_error = RuntimeError(
                    "Encountered HTTP error {code} with message {message}".format(
                        code=error.code, message=str(error)
                    )
                )
            elif error_type is APIError:
                new_error = APIError(
                    "Riot API is currently unavailable. Please try again later. The received error code was {code}: {message}".format(
                        code=error.code, message=str(error)
                    ),
                    error.code,
                )
            elif error_type is APINotFoundError:
                new_error = APINotFoundError(
                    "Riot API returned a NOT FOUND error. The received error code was {code}: {message}".format(
                        code=error.code, message=str(error)
                    ),
                    error.code,
                )
            elif error_type is APIRequestError:
                new_error = APIRequestError(
                    "Riot API returned a BAD REQUEST error. The received error code was {code}: {message}".format(
                        code=error.code, message=str(error)
                    ),
                    error.code,
                )
            elif error_type is APIForbiddenError:
                new_error = APIForbiddenError(
                    "Riot API returned a FORBIDDEN error. The received error code was {code}: {message}".format(
                        code=error.code, message=str(error)
                    ),
                    error.code,
                )
            else:
                new_error = error_type(str(error))

            raise new_error from error

class RiotAPIRequest(object):
    def __init__(
        self,
        servise: RiotAPIService,
        url: str,
        parameters: MutableMapping[str, Any],
    ):
        self.servise = servise
        self.url = url
        self.parameters = parameters

    def __call__(self):
        try:
            body, response_headers = self.servise._client.get(
                url=self.url,
                parameters=self.parameters,
                headers=self.servise._headers,
            )
            return body
        except HTTPError as error:
            raise error
