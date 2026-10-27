import configparser
from pathlib import Path
import requests
import os
from utils.logger import get_logger
logger = get_logger(__name__)

class ApiClient:
    def __init__(self,authenticated=True):
        config_path = Path(__file__).resolve().parent.parent / "config" / "config.ini"

        config = configparser.ConfigParser()
        config.read(config_path)

        self.base_url = config.get("api", "base_url").rstrip("/")
        self.timeout = config.getint("api", "timeout")
        self.session = requests.Session()

        if authenticated:
            cookie = os.getenv("API_COOKIE")
            if cookie:
                self.session.headers.update({"Cookie": cookie})

    def get_endpoint(self, endpoint_name):
        config_path = (
                Path(__file__).resolve().parent.parent
                / "config"
                / "config.ini"
        )
        config = configparser.ConfigParser()
        config.read(config_path)

        return config.get("endpoints", endpoint_name)

    # def get(self, endpoint, params=None, headers=None):
    #     url = f"{self.base_url}/{endpoint.lstrip('/')}"
    #     return self.session.get(
    #         url,
    #         params=params,
    #         headers=headers,
    #         timeout=self.timeout
    #     )
    def get(self, endpoint, params=None, headers=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        logger.info("GET request: endpoint=%s, params=%s", endpoint, params)

        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )

            logger.info(
                "GET response: endpoint=%s, status_code=%s",
                endpoint,
                response.status_code
            )

            return response

        except requests.exceptions.RequestException:
            logger.exception("GET request failed: endpoint=%s", endpoint)
            raise

    # def post(self, endpoint, json=None, params=None, headers=None):
    #     url = f"{self.base_url}/{endpoint.lstrip('/')}"
    #     return self.session.post(
    #         url,
    #         json=json,
    #         params=params,
    #         headers=headers,
    #         timeout=self.timeout
    #     )
    def post(self, endpoint, json=None, params=None, headers=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        logger.info("POST request: endpoint=%s, params=%s", endpoint, params)

        try:
            response = self.session.post(
                url,
                json=json,
                params=params,
                headers=headers,
                timeout=self.timeout
            )

            logger.info(
                "POST response: endpoint=%s, status_code=%s",
                endpoint,
                response.status_code
            )

            return response

        except requests.exceptions.RequestException:
            logger.exception("POST request failed: endpoint=%s", endpoint)
            raise

    # def delete(self, endpoint, params=None, json=None, headers=None):
    #     url = f"{self.base_url}/{endpoint.lstrip('/')}"
    #     return self.session.delete(
    #         url,
    #         params=params,
    #         json=json,
    #         headers=headers,
    #         timeout=self.timeout
    #     )
    def delete(self, endpoint, params=None, json=None, headers=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        logger.info("DELETE request: endpoint=%s, params=%s", endpoint, params)

        try:
            response = self.session.delete(
                url,
                params=params,
                json=json,
                headers=headers,
                timeout=self.timeout
            )

            logger.info(
                "DELETE response: endpoint=%s, status_code=%s",
                endpoint,
                response.status_code
            )

            return response

        except requests.exceptions.RequestException:
            logger.exception("DELETE request failed: endpoint=%s", endpoint)
            raise

