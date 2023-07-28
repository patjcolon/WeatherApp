"""creating a model class for use with weather app and api data"""

from dataclasses import dataclass
from datetime import datetime as dt


@dataclass
class Weather:
    date: dt
    
    # main
    details: dict
    temperature: str #main, temp
    humidity: float #main, humidity

    # weather
    weather: list[dict]
    description: str #weather, 0, description
    
    # clouds
    clouds: dict
    cloud_coverage: float #clouds, all

    # wind
    winds: dict
    wind_speed: float #wind, speed
    wind_knots: float
    wind_degrees: float #wind, deg
    wind_direction: str



    
    def __str__(self):
        return f'[{self.date:%H:%M}] {self.temperature}°F ({self.description})'
    

    def test_printing(self):
        description_underline = '-' * len(self.description) +'--'
        return f"""  {self.date:%I:%M %p}:         [{self.description.title()}]
  ---------         {description_underline}
  - Temperature: ({self.temperature}°F)   - Humidity: ({self.humidity}%) 
  - Wind Speed: ({self.wind_knots} Knots {self.wind_direction})
  - Cloud Coverage: ({self.cloud_coverage}%)


    """

    def get_formatted_data(self):
        return f"""{self.date:%I:%M %p} - {self.description.title()},
        Temperature: {self.temperature}°F,
        Humidity: {self.humidity}%,
        Winds: {self.wind_knots} knots {self.wind_direction},
        Cloud coverage: {self.cloud_coverage}%|"""




# retired weather formatting. replaced by model
def format_weather_details(data: dict):
    def degrees_to_compass(degrees:float) -> str:
        """Converts degrees into cardinal direction"""
        index = int((degrees/22.5)+0.5)
        directions: list = ['N', 'NNE', 'NE','ENE',
                            'E','ESE', 'SE', 'SSE',
                            'S','SSW','SW','WSW',
                            'W','WNW','NW','NNW']
        cardinal_direction = directions[(index % 16)]
        return cardinal_direction

    reports = data['list']
    for report in reports:
        time = report['dt_txt'][:-3]

        temperature = report['main']['temp']
        humidity = report['main']['humidity']

        sky_description = report['weather'][0]['description']

        cloud_coverage = report['clouds']['all']
        
        wind_knots = round((report['wind']['speed'] / 1.151), 1)
        wind_degrees = report['wind']['deg']
        wind_direction = degrees_to_compass(wind_degrees)

        print(f"""
    {time}    Weather Report:
    Temperature: {temperature}°F   -   Humidity: {humidity}%   -   Cloud Coverage: {cloud_coverage}%
    Weather Description: {sky_description.title()}
    Wind Speed: {wind_knots} Knots {wind_direction}
    """)