
import requests
from bs4 import BeautifulSoup
import json
import datetime
from dotenv import load_dotenv
import os


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


def get_weather_data_in_string(url):
    result = requests.get(url)
    json_data = requests.Response.json(result)
    #print(json_data)
    days_data = json_data['days']
    location = json_data['resolvedAddress']
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
        if count == 7:
            break
    return data

    
def get_city_weather_update(city):
   url  = create_search_url_from_city_name(city)
   string_data = get_weather_data_in_string(url)
   return string_data



def generate_weather_summary(weather_data):
    load_dotenv()
    api_key = os.getenv('API_KEY')
    api_endpoint = 'https://api.openai.com/v1/chat/completions'
    prompt = f"Weather update: {weather_data}"
    params = {
    'model': 'gpt-3.5-turbo',
    'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content': prompt}],
    'max_tokens': 1,
    'temperature': 0.3,
    'n': 1,
    'stop': None,
    }
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}',
    }
    response = requests.post(api_endpoint, json=params, headers=headers)
    data = response.json()
    #summary = data['choices'][0]['message']['content']
    return data


if __name__ == "__main__":


    #print(create_search_url_from_keyword('london'))
    #print(get_city_weather_update('mansehra'))
    weather_data = get_city_weather_update('london')
    #print(weather_data)

    print(generate_weather_summary(weather_data))

        


    







        

        


  




    

    
    
  
 

    







