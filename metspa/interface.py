from metspa.utils import read_environment_variable
import requests
from requests.exceptions import HTTPError
import logging
import urllib
import time

aemet_api_key_name = "AEMET_API_KEY"


class AEMETInterface:
    ROUTE = "https://opendata.aemet.es/opendata/"
    API_KEY = read_environment_variable(aemet_api_key_name)
    
    # TODO Note to me
    # make a generic api call function and add as args the desired endpoint and message
    
    def _call_api(self, endpoint, query_params=None) -> dict:
        
        query_endpoint = urllib.parse.urljoin(self.ROUTE, endpoint)

        headers = {
            'no-cache': False
        }
        
        if query_params is None:
            query_params = {}
        query_params["api_key"] = self.API_KEY

        try:
            logging.info(
                f"Calling AEMET OPENDATA"
            )
            response = requests.get(
                query_endpoint, params=query_params, timeout=360
            )
            logging.info("Successfully read API")
            response.raise_for_status()
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
        http_msg = urllib.request.urlopen(api_msg["datos"])
        
        return http_msg.read()
        