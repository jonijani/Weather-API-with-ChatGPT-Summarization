
from distutils import config
import requests
from bs4 import BeautifulSoup
import json
import datetime
from dotenv import load_dotenv
import os
import openai
from django.conf import settings

load_dotenv()



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
    year = numbers[0:4]
    month = numbers[4:6]
    day = numbers[6:8]
    date = f'{year}-{month}-{day}'
    return date


def get_weather_data_in_string(url):
    result = requests.get(url)
    json_data = requests.Response.json(result)
    #location = json_data['resolvedAddress']

    days_data = json_data['days']
    data = ''
    for day in days_data:
    #     if day['datetime'] == date:
    #         break
        #date = day['datetime']
        sunrise = day['sunrise']
        sunset = day['sunset']
        temp = day['temp']
        conditions = day['conditions']
        humidity = day['humidity']
        windspeed = day['windspeed']
        #description = day['description']
        data = data + f' Sunrise: {sunrise}, sunset: {sunset}, temp: {temp}, conditions: {conditions}, humidity :{humidity, } windspeed:{windspeed} '
        break
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



def get_response_from_openAI(string_data):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="[INSTRUCTION] Consider yourself a weather forcasting expert .On the basis of following data you have to give us short and simple summary for average human to understand and provide  that as follow  " + string_data,
    temperature=0.5,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    return response

def get_summary_of_weather(response):
    summary = response['choices'][0]['text']
    return summary

def get_city_weather_update(city):
   url  = create_search_url_from_city_name(city)
   string_data = get_weather_data_in_string(url)
   response = get_response_from_openAI(string_data)
   summary = get_summary_of_weather(response)

   return summary






if __name__ == "__main__":


    #print(create_search_url_from_keyword('london'))
    #print(get_city_weather_update('mansehra',get_date('20230720')))

    print(get_city_weather_update('london'))
   



