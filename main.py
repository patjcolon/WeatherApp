"""Creating a weather app using APIs"""
from flask import Flask, request, redirect, url_for, render_template
from weather_api import get_weather, get_weather_details, Weather

def main(user_city:str = 'tokyo'):
    
    # Get city that weather forecast will be on
    #user_city: str = input('Enter a city: ')
    #user_city = 'tokyo'

    # Get the current weather details
    current_weather: dict = get_weather(user_city, False) #change to false in order to get real data
    weather_details: list[Weather] = get_weather_details(current_weather)

    # Get the current days
    date_format: str = '%m/%d/%y'
    days: list[str] = sorted(set(f'{date.date:{date_format}}' for date in weather_details))
    
    
    city_banner = f'{user_city.title()}\'s 5 Day Forecast'

    # creating a massive string for entire 5 day forecast
    full_forecast: str = ''

    for day in days:
        day_title = f'{day} Report:|'
        day_forecast = day_title

        grouped: list[Weather] = [current for current in weather_details if f'{current.date:{date_format}}' == day]
        for report in grouped:
            report = report.get_formatted_data()
            day_forecast += report
        day_forecast = day_forecast[:-1]
        full_forecast += day_forecast + ';'
    full_forecast = full_forecast[:-1]
    return city_banner, full_forecast


# if __name__ == '__main__':
#     forecast = main()
#     print(forecast[1])


app = Flask(__name__, static_url_path='/static')

city = 'tokyo'

@app.route('/', methods =['GET', 'POST'])
def index():
    global city
    if request.method == 'GET':
        return render_template("index.html")
    if request.method == 'POST':
        city = request.form.get('city_name')
        return redirect(url_for('forecast'))

@app.route('/forecast')
def forecast():
    city_banner, forecast_list = main(city)
    return render_template("forecast.html", city_banner=city_banner, forecast_list=forecast_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)