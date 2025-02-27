import sys
sys.path.append("..")
import requests
import pandas as pd
from datetime import datetime
from config.settings import API_BASE_URL, API_KEY
from flatten_json import flatten

class AirQualityAPI:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.api_key = API_KEY

    def fetch_city_weather_data(self):
        """Fetch air quality data from the API"""
        headers = {
            "Accept": "application/json",
            "api-key": self.api_key
        }
        
        try:
            response = requests.get(
                f"{self.base_url}&appid={self.api_key}",
                headers=headers
            )
            response.raise_for_status()
            print(flatten(response.json()))
            return flatten(response.json())
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")