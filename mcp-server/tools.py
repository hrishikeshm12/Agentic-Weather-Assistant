"""
Weather API Tools for MCP Server
Wraps OpenWeather API with clear interfaces
"""

import os
import requests
from typing import Dict, List, Any, Optional

class WeatherAPIClient:
    """Client for OpenWeather API"""

    BASE_URL = "https://api.openweathermap.org"

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OPENWEATHER_API_KEY environment variable not set")
        self.api_key = api_key

    def _make_request(self, endpoint: str, params: Dict) -> Dict[str, Any]:
        """Make HTTP request to OpenWeather API"""
        params['appid'] = self.api_key
        try:
            response = requests.get(f"{self.BASE_URL}{endpoint}", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")

    def get_current_weather(self, city: str, country: Optional[str] = None) -> Dict[str, Any]:
        """
        Get current weather for a city.

        Args:
            city: City name
            country: Optional country code (e.g., 'US', 'GB')

        Returns:
            Weather data including temperature, conditions, humidity, wind speed
        """
        query = city
        if country:
            query = f"{city},{country}"

        try:
            data = self._make_request("/data/2.5/weather", {
                'q': query,
                'units': 'metric'  # Use Celsius
            })

            return {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'temp_max': data['main']['temp_max'],
                'temp_min': data['main']['temp_min'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'condition': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'cloudiness': data['clouds']['all'],
                'sunrise': data['sys']['sunrise'],
                'sunset': data['sys']['sunset']
            }
        except KeyError as e:
            raise Exception(f"Unexpected API response format: {str(e)}")

    def get_forecast(self, city: str, country: Optional[str] = None, days: int = 5) -> Dict[str, Any]:
        """
        Get weather forecast for a city.

        Args:
            city: City name
            country: Optional country code
            days: Number of days to forecast (default 5)

        Returns:
            Forecast data with daily weather predictions
        """
        query = city
        if country:
            query = f"{city},{country}"

        try:
            data = self._make_request("/data/2.5/forecast", {
                'q': query,
                'units': 'metric',
                'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
            })

            # Group by day
            daily_forecasts = {}
            for forecast in data['list']:
                date = forecast['dt_txt'].split()[0]  # YYYY-MM-DD
                if date not in daily_forecasts:
                    daily_forecasts[date] = []
                daily_forecasts[date].append(forecast)

            # Process daily data
            forecasts = []
            for date, items in sorted(daily_forecasts.items()):
                temps = [item['main']['temp'] for item in items]
                conditions = [item['weather'][0]['main'] for item in items]

                forecasts.append({
                    'date': date,
                    'temp_max': max(temps),
                    'temp_min': min(temps),
                    'temp_avg': sum(temps) / len(temps),
                    'condition': conditions[0],  # Most common condition
                    'description': items[0]['weather'][0]['description']
                })

            return {
                'city': data['city']['name'],
                'country': data['city']['country'],
                'forecasts': forecasts
            }
        except KeyError as e:
            raise Exception(f"Unexpected API response format: {str(e)}")

    def search_cities(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Search for cities by name.

        Args:
            query: City name to search for
            limit: Maximum number of results

        Returns:
            List of matching cities with coordinates
        """
        try:
            # Use Geocoding API for city search
            response = requests.get(f"{self.BASE_URL}/geo/1.0/direct", params={
                'q': query,
                'appid': self.api_key,
                'limit': limit
            }, timeout=10)
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data:
                results.append({
                    'name': item['name'],
                    'country': item.get('country', 'N/A'),
                    'state': item.get('state', ''),
                    'latitude': item['lat'],
                    'longitude': item['lon']
                })

            return {
                'query': query,
                'results': results
            }
        except requests.exceptions.RequestException as e:
            raise Exception(f"City search failed: {str(e)}")


def create_tools(api_key: str) -> Dict[str, Any]:
    """
    Create MCP tool definitions for LangChain integration.

    These tool definitions follow the LangChain format for function calling.
    """
    client = WeatherAPIClient(api_key)

    return {
        'get_current_weather': {
            'description': 'Get current weather conditions for a city',
            'parameters': {
                'type': 'object',
                'properties': {
                    'city': {
                        'type': 'string',
                        'description': 'Name of the city'
                    },
                    'country': {
                        'type': 'string',
                        'description': 'Optional ISO 3166-1 alpha-2 country code (e.g., "US", "GB")'
                    }
                },
                'required': ['city']
            },
            'function': client.get_current_weather
        },
        'get_forecast': {
            'description': 'Get 5-day weather forecast for a city',
            'parameters': {
                'type': 'object',
                'properties': {
                    'city': {
                        'type': 'string',
                        'description': 'Name of the city'
                    },
                    'country': {
                        'type': 'string',
                        'description': 'Optional ISO 3166-1 alpha-2 country code'
                    },
                    'days': {
                        'type': 'integer',
                        'description': 'Number of days to forecast (default 5)',
                        'default': 5
                    }
                },
                'required': ['city']
            },
            'function': client.get_forecast
        },
        'search_cities': {
            'description': 'Search for cities by name to get their coordinates and details',
            'parameters': {
                'type': 'object',
                'properties': {
                    'query': {
                        'type': 'string',
                        'description': 'City name to search for'
                    },
                    'limit': {
                        'type': 'integer',
                        'description': 'Maximum number of results (default 5)',
                        'default': 5
                    }
                },
                'required': ['query']
            },
            'function': client.search_cities
        }
    }
