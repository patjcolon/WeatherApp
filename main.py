"""Creating a weather app using APIs"""
from flask import Flask, request, redirect, render_template
from weather_api import get_weather, get_weather_details, Weather

def main(user_city:str = 'tokyo'):
    
    # Get city that weather forecast will be on
    #user_city: str = input('Enter a city: ')
    #user_city = 'tokyo'

    # Get the current weather details
    current_weather: dict = get_weather(user_city, True) #change to false in order to get real data
    weather_details: list[Weather] = get_weather_details(current_weather)

    # Get the current days
    date_format: str = '%m/%d/%y'
    days: list[str] = sorted(set(f'{date.date:{date_format}}' for date in weather_details))
    
    
    city_banner_name = f'{user_city}\'s 5 Day Forecast'
    city_banner = '='*40 + '\n'
    city_banner +='||' + city_banner_name.center(36) + '||' + '\n'
    city_banner += '='*40 + '\n'

    # creating a massive string for entire 5 day forecast
    full_forecast: list[str] = []
    full_forecast.append(city_banner)

    for day in days:
        day_title = f'  {day}   Daily Report: \n'
        day_title += '  ' + '='*24
        day_forecast = day_title + '\n'

        grouped: list[Weather] = [current for current in weather_details if f'{current.date:{date_format}}' == day]
        for report in grouped:
            report = report.test_printing()
            day_forecast += report + '\n'
        full_forecast.append(day_forecast)
    return full_forecast


# if __name__ == '__main__':
#     forecast = main()
#     print(forecast[1])


app = Flask(__name__)

city = 'tokyo'

@app.route('/', methods =['GET', 'POST'])
def index():
    global city
    if request.method == 'POST':
        city = request.form.get('city_name')
        return redirect('/forecast')
    return render_template("index.html")

@app.route('/forecast')
def forecast():
    forecast_list = main(city)
    title, today, tomorrow, two_days, three_days, four_days, five_days = forecast_list[::]
    return render_template("forecast_display.html",
                        title=title, today=today, tomorrow=tomorrow, two_days=two_days,
                        three_days=three_days, four_days=four_days, five_days=five_days)

if __name__ == '__main__':
    app.run()