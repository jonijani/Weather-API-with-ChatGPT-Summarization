
import requests
from bs4 import BeautifulSoup
import json
import datetime
from dotenv import load_dotenv
import os
import openai
#from django.conf.global_settings import OPENAI_API_KEY
#load_dotenv()



#BASE_URL = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/londonoup=metric&key=?unitGrYS5LCHDN6WNKKRUCEYTCGDY3K&contentType=json'


key = 'YS5LCHDN6WNKKRUCEYTCGDY3K'
BASE_URL = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'


def get_req(url):
    res = requests.get(url)
    if res.status_code == 200:
        print(url)
        return True
    else:
        raise Exception('URL is not successful')
    
def create_search_url_from_city_name(city):
    #city = input('Enter any city name in world :')
    key = 'YS5LCHDN6WNKKRUCEYTCGDY3K'
    get_key = f'?unitGroup=metric&key={key}'
    res_url = '&contentType=json'
    url = f'{BASE_URL}{city}{get_key}{res_url}'
    return url

def get_date(numbers): # 20230727
    current_date = datetime.date.today()
    # current_year = current_date[0:4]
    # current_month = current_date[4:6]
    # curent_day = current_date[6:8]

    year = numbers[0:4]
    month = numbers[4:6]
    day = numbers[6:8]
    date = f'{year}-{month}-{day}'
    return date


def get_weather_data_in_string(url,date):
    result = requests.get(url)
    json_data = requests.Response.json(result)
    location = json_data['resolvedAddress']

    days_data = json_data['days']
    data = ''
    for day in days_data:
        if day['datetime'] == date:
            break
    date = day['datetime']
    sunrise = day['sunrise']
    sunset = day['sunset']
    temp = day['temp']
    conditions = day['conditions']
    humidity = day['humidity']
    windspeed = day['windspeed']
    description = day['description']
    data = data + f'location : {location}, date: {date}, Sunrise: {sunrise}, sunset: {sunset}, temp: {temp}, conditions: {conditions}, humidity :{humidity, } windspeed:{windspeed},description:{description}\n '
    return data

    '''location = json_data['resolvedAddress']
    print(location)
    data = ''
    len_days_data = len(days_data)
    count = 0
    for day in days_data:
        date = day['datetime']
        sunrise = day['sunrise']
        sunset = day['sunset']
        temp = day['temp']
        conditions = day['conditions']
        humidity = day['humidity']
        windspeed = day['windspeed']
        description = day['description']
        data = data + f'location : {location}, date: {date}, Sunrise: {sunrise}, sunset: {sunset}, temp: {temp}, conditions: {conditions}, humidity :{humidity, } windspeed:{windspeed},description:{description}\n '
        count += 1
        if count == 1:
            break
    return data'''

    
def get_city_weather_update(city,date):
   url  = create_search_url_from_city_name(city)
   string_data = get_weather_data_in_string(url,get_date(date))
   return string_data


def get_summary_from_openAI(data,api_key):
    #openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key


    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="[INSTRUCTION] Consider yourself a weather forcasting expert .On the basis of following data you have to give us short and simple summary for average human to understand and provide  that this information may vary .The data is as follows " + data,
    temperature=0.5,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    return response

if __name__ == "__main__":


    #print(create_search_url_from_keyword('london'))
    #print(get_city_weather_update('mansehra',get_date('20230720')))

    # weather_data = get_city_weather_update('london','20230720')
    # print(weather_data)

    #print(generate_weather_summary(weather_data))
    api = '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'
    data = 'Sunrise: 05:06:48, sunset: 21:06:14, temp: 16.8, conditions: Partially cloudy, humidity :(62.6,) windspeed:10.8.'
    print(get_summary_from_openAI(data,api))

