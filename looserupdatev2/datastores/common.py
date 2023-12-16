from typing import MutableMapping, Mapping, Union, Any, Dict, List
from urllib.parse import urlencode
import re
import logging
import requests

try:
    import ujson as json
except ImportError:
    import json

LOGGER = logging.getLogger("looserupdatev2.datastores")


class HTTPError(RuntimeError):
    def __init__(self, message, code, response_headers: Dict[str, str] = None):
        super().__init__(message)
        self.code = code
        self.response_headers = response_headers or {}

class HTTPClient(object):
    @staticmethod
    def _get(
        url: str,
        headers: Mapping[str, str] = None,
    ) -> (int, bytes, dict):
        if not headers:
            request_headers = {"Accept-Encoding": "gzip"}
        else:
            if not headers:
                request_headers = {"Accept-Encoding": "gzip"}
            else:
                request_headers = {k: v for k, v in headers.items()}
                if "Accept-Encoding" not in headers:
                    request_headers["Accept-Encoding"] = "gzip"

            LOGGER.info(f"Request: {url}")
            return requests.get(url=url, headers=request_headers)

    def get(
        self,
        url: str,
        parameters: MutableMapping[str, Any] = None,
        headers: Mapping[str, str] = None,
        encode_parameters: bool = True,
    ) -> (Union[dict, list, str, bytes], dict):
        if parameters:
            if encode_parameters:
                parameters = {
                    k: str(v).lower() if isinstance(v, bool) else v 
                    for k, v in parameters.items()
                }
                parameters = urlencode(parameters, doseq=True)
            url = "{url}?{parameters}".format(url=url, parameters=parameters)

        response = HTTPClient._get(url, headers)
        response_headers = response.headers

        if response.status_code >= 400:
            raise HTTPError(
                response.reason, response.status_code,  response_headers,
            )

        content_type = response_headers.get(
            "Content-Type", None
        ).upper()

        match = re.search("CHARSET=(\S+)", content_type)
        if match:
            if "APPLICATION/JSON" in content_type:
                body = response.json()
            else:
                body = response.content.decode("utf-8")
        elif "IMAGE/" in content_type:
            body = response.content
        else:
            body = response.content.decode("utf-8")

        return body, response_headers
