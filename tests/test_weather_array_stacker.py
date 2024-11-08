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

def dutch_coordinates(city):
  '''
  Function that uses a webscraper to determine the coordinates of a Dutch city from its name. The function is not case sensitive and can deal with names composed of multiple words. 
  Input: Name of a city in The Netherlands as a string
  Output: Float array of coordinates in the decimal degree format : [Latitude,Longitude]
  Example:
  Input: 'The Hague'
  Output: [52.07667, 4.29861]
  '''
  if type(city) is not str:
    raise ValueError(f"Invalid input data type")
  city=city.lower() #the url only works for lowercase city names
  city =city.replace(" ", "-") #for composite names like "the hague"
  #determining coordinates
  url=f'https://www.geodatos.net/en/coordinates/netherlands/{city}'
  results =requests.get(url).text
  doc= BeautifulSoup(results, "html.parser")
  unprocessed_coordinates=doc.find('p', class_='font-bold text-blue-500 mt-3 lg:text-lg')
  #processing coordinates into usable float array format
  if(unprocessed_coordinates) == None:
    raise ValueError(f"Error: Coordinates not found for {city}")
  list_coordinates=unprocessed_coordinates.contents[0].split(",")
  processed_cooridnates = [float(a) for a in list_coordinates]
  return processed_cooridnates

def weather_array_stacker(url_list):
  '''
  Uses the bbc_weather_scraper() and dutch_coordinates() functions to generate a matrix with cities, maximum temperature, weather conditions and coordinates from an array of bbc weather urls. The urls have to correspond to dutch cities in order for the dutch_coordinates() function to work. 
  
  Input: Array of urls of the form ["https://www.bbc.com/weather/xxxxxxx","https://www.bbc.com/weather/yyyyyyy"]
  Output: [[City1(str), temp_max1(int), weather1(str), latitude1(float), longitute1(float)],[City2(str), temp_max2(int), weather2(str), latitude2(float), longitute2(float)]]
  '''
  index=len(url_list)#determining number of rows in the matrix
  stacked_results=[]#initialising stack of results
  if index == 0 or type(url_list) is not list:
    raise ValueError('Invalid input')
  for i in range(index):
    #determining weather conditions for each url
    current=bbc_weather_scraper(url_list[i])
    coordinates=dutch_coordinates(current[0]) #calculating coordiantes
    current=current+coordinates #adding coordinates to the city row
    stacked_results.append(current) #stacking matrix
  return stacked_results

def test_weather_array_stacker():
  #test if function runs under normal conditions
  url_list1= ["https://www.bbc.com/weather/2759794","https://www.bbc.com/weather/2755003"] 
  result1 =weather_array_stacker(url_list1)
  #testing shape
  assert len(result1) == 2
  assert len(result1[0][:]) == 5
  #testing datatype
  assert type(result1[1][0]) is str and type(result1[0][0]) is str
  assert type(result1[1][1]) is int and type(result1[0][1]) is int
  assert type(result1[1][2]) is str and type(result1[0][2]) is str
  assert type(result1[1][3]) is float and type(result1[0][3]) is float
  assert type(result1[1][4]) is float and type(result1[0][4]) is float
  #testing if format remains consistent with docs for only one link as input
  url_list2= ["https://www.bbc.com/weather/2759794"]
  result2 = weather_array_stacker(url_list2)
  assert type(result2) is list
  assert result1[0] == result2[0]
  #testing if errors in called functions are raised correctly in edge cases
  url_list3=["https://www.cern.home"]
  with pytest.raises(ValueError, match='Invalid website'):
    weather_array_stacker(url_list3)  
  with pytest.raises(ValueError, match='Invalid input'):
    weather_array_stacker([])
test_weather_array_stacker()