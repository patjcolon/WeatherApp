"""api data handling for weather app"""

from typing import Final
import json
import requests
from model import Weather, dt

API_KEY: Final[str] = 'insert api key here from api.openweathermap.org'
BASE_URL: Final[str] = 'https://api.openweathermap.org/data/2.5/forecast'
GEO_URL: Final[str] = 'https://api.openweathermap.org/geo/1.0/direct'
'https://api.openweathermap.org/geo/1.0/direct?q=tokyo&appid=02f1aa107378f96a7dfaf5baba998934'


def get_lat_lon(city_name: str) -> tuple:
        """returns (lat, lon) of city name"""
        payload: dict = {'q': city_name, 'appid': API_KEY}
        response = requests.get(url=GEO_URL, params=payload)
        geo_data: dict = response.json()[0]
        
        lat: str = geo_data['lat']
        lon: str = geo_data['lon']
        return lat, lon


def get_weather(city_name: str, mock: bool = True) -> dict:
    if mock:
        with open('dummy_data.json') as file:
            print("dummy data from dummy_data.json loaded")
            return json.load(file)
        
    # Converting city name into lat long coordinates to feed weather api
    lat, lon = get_lat_lon(city_name)

    # Request live data
    payload: dict = {'lat': lat, 'lon': lon, 'appid': API_KEY, 'units': 'imperial'}
    response = requests.get(url=BASE_URL, params=payload)
    data: dict = response.json()

    return data


def degrees_to_compass(degrees:float) -> str:
    """Converts degrees into cardinal direction"""
    index = int((degrees/22.5)+0.5)
    directions: list = ['N', 'NNE', 'NE','ENE',
                        'E','ESE', 'SE', 'SSE',
                        'S','SSW','SW','WSW',
                        'W','WNW','NW','NNW']
    cardinal_direction = directions[(index % 16)]
    return cardinal_direction


def mph_to_knots(mph: float, decimals: int=1) -> float:
    knots = round((mph / 1.151), decimals)
    return knots


def get_weather_details(weather:dict) -> list[Weather]:
    days: list[dict] = weather.get('list')

    if not days:
        raise Exception(f'Problem with json: {weather}')
    
    list_of_weather: list[Weather] = []
    for day in days:
        w: Weather = Weather(date=dt.fromtimestamp(day.get('dt')),
                             details=(details := day.get('main')),
                             temperature=details.get('temp'),
                             humidity=details.get('humidity'),
                             weather=(weather := day.get('weather')),
                             description=weather[0].get('description'),
                             clouds=(clouds := day.get('clouds')),
                             cloud_coverage=clouds.get('all'),
                             winds=(winds := day.get('wind')),
                             wind_speed=(wind_speed := winds.get('speed')),
                             wind_knots=mph_to_knots(wind_speed),
                             wind_degrees=(wind_degrees := winds.get('deg')),
                             wind_direction=degrees_to_compass(wind_degrees)
                             )
        list_of_weather.append(w)
    return list_of_weather



if __name__ == '__main__':
    current_weather = get_weather('San Pedro', mock=True)
    weather: list[Weather] = get_weather_details(current_weather)
    for w in weather:
        w.test_printing()

