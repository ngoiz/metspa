import logging
import urllib

import requests
from requests.exceptions import HTTPError

from metspa.utils import read_environment_variable

aemet_api_key_name = "AEMET_API_KEY"


class AEMETInterface:
    ROUTE = "https://opendata.aemet.es/opendata/"
    API_KEY = read_environment_variable(aemet_api_key_name)

    def __init__(self) -> None:
        self.logger = logging.getLogger("interface")

    # TODO Note to me
    # make a generic api call function and add as args the desired endpoint and message

    def _call_api(self, endpoint, query_params=None) -> dict:

        query_endpoint = urllib.parse.urljoin(self.ROUTE, endpoint)

        if query_params is None:
            query_params = {}
        query_params["api_key"] = self.API_KEY

        try:
            self.logger.info("Calling AEMET OPENDATA")
            response = requests.get(query_endpoint, params=query_params, timeout=360)
            self.logger.info(f"Successfully read API - STATUS {response.status_code}")
        except HTTPError as http_err:
            logging.exception(http_err)
            print(f"HTTP error occurred: {http_err}")
            raise

        return response.json()

    def get_api_msg(self, endpoint, query_params=None) -> str:
        """

        Returns:
            str: HTTP response data
        """
        api_msg = self._call_api(endpoint, query_params)

        try:
            api_data = api_msg["datos"]
        except KeyError:
            error_msg = f'Error - STATUS {api_msg["estado"]} - {api_msg["descripcion"]}'
            self.logger.error(error_msg)
            raise HTTPError
        else:
            http_msg = urllib.request.urlopen(api_data)

        return http_msg.read().decode("UTF-8")
