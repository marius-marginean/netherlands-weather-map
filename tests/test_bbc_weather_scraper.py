from bs4 import BeautifulSoup
import requests
import re
import pytest

def bbc_weather_scraper(url):
  '''
  This function is a web scraper that obtains the current weather data in a specific city from a provided bbc weather url. The expected output is a list containing the city name, maximum temperature and description of current conditions. All values are returned as strings.

  Input: 
  url(str) of the form : 'https://www.bbc.com/weather/xxxxxxx'.
  Output: 
  array of the fomr: [City(str), max_temp (int), description (str)] 
  
  Example functionality:
  input:'https://www.bbc.com/weather/2988507'
  output: ['Paris', 14, 'Sunny and light winds'] //values may change depending on current conditions
  '''
  #reading of the url
  # A url was chosen as an input instead of a city name because weather websites do not index their results by city name and this makes them much more difficult to scrape.
  if url[0:28] != 'https://www.bbc.com/weather/':
    raise ValueError('Invalid website')
  results =requests.get(url).text
  doc= BeautifulSoup(results, "html.parser")
  #selecting the relevant location for today's weather
  clasa= doc.find(class_='wr-day__details')
  #finding the city 
  location=doc.find(class_='wr-c-location__name gel-paragon')
  if location is None:
    raise ValueError('Location not found')
  city=location.contents[0].strip()
  #finding description and temperature values
  desc= clasa.find(class_="wr-day__details__weather-type-description")
  temperature= clasa.find(class_="wr-value--temperature--c")
  #selecting the temperature as an integer from a string
  description=desc.contents[0].strip()
  num_temp = re.search(r'\d+', str(temperature.contents))
  if num_temp:
    temp=int(num_temp.group())
  #constructing the final results vector
  results = [city,temp,description]
  return results

def test_bbc_weather_scraper():
  #testing normal operation
  result = bbc_weather_scraper('https://www.bbc.com/weather/2988507')
  assert result[0] == 'Paris'
  assert type(result[1]) is int and result[1]>-100 and result[1]<70
  assert type(result[2]) is str
  #testing if errors are raised correctly in edge cases
  with pytest.raises(ValueError, match='Invalid website'):
    bbc_weather_scraper('https://www.amazon.com/')
  with pytest.raises(ValueError, match='Invalid website'):
    bbc_weather_scraper([])
  with pytest.raises(ValueError, match='Location not found'):
    bbc_weather_scraper('https://www.bbc.com/weather/0488508')
test_bbc_weather_scraper()#running the testing function so the file can be run as a standalone


 
