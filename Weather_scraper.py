from bs4 import BeautifulSoup
import requests
import numpy as np
import folium
import re

def bbc_weather_scraper(url):
  '''
  This function is a web scraper that obtains the current weather data in a specific city from a provided bbc weather url. The expected output is a list containing the city name, maximum temperature and description of current conditions. All values are returned as strings.

  Input: 
  url(str) of the form : "https://www.bbc.com/weather/xxxxxxx".
  Output: 
  array of the fomr: [City(str), max_temp (int), description (str)] 
  
  Example functionality:
  input:'https://www.bbc.com/weather/2988507'
  output: ['Paris', 14, ['Sunny and light winds']]
  '''
  #reading of the url
  # A url was chosen as an input instead of a city name because weather websites do not index their results by city name and this makes them much more difficult to scrape.
  results =requests.get(url).text
  doc= BeautifulSoup(results, "html.parser")
  #selecting the relevant location for today's weather
  clasa= doc.find(class_='wr-day__details')
  #finding the city 
  location=doc.find(class_='wr-c-location__name gel-paragon')
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
  Function that uses a webscraper to determine the coordinates of a Dutch city from its name. 
  Input: Name of a city in the netherlands
  Output: Float array of coordinates in the decimal degree format : [Latitude,Longitude]
  '''
  city=city.lower() #the url only works for lowercase city names
  city =city.replace(" ", "-") #for composite names like "the hague"
  #determining coordinates
  url=f'https://www.geodatos.net/en/coordinates/netherlands/{city}'
  results =requests.get(url).text
  doc= BeautifulSoup(results, "html.parser")
  unprocessed_coordinates=doc.find('p', class_='font-bold text-blue-500 mt-3 lg:text-lg')
  #processing coordinates into usable float array format
  list_coordinates=unprocessed_coordinates.contents[0].split(",")
  processed_cooridnates = [float(a) for a in list_coordinates]
  return processed_cooridnates

def weather_array_stacker(url_list):
  '''
  
  '''
  index=len(url_list)#determining number of possible results
  stacked_results=np.empty((0,5))#initialising final result
  for i in range(index):
    current=bbc_weather_scraper(url_list[i])#determining values for each url
    coordinates=dutch_coordinates(current[0])
    current=np.append(current, coordinates)
    stacked_results=np.vstack([stacked_results,current])#creating a matrix with weather data for all cities
  return stacked_results

def map_generator(matrix):
  '''
  Function that creates a map of The Netherlands where all of the cities are assigned their corresponding temperature and weather descriptions. 


  '''
  netherlands_map = folium.Map(location=[52.3784, 4.9009], zoom_start=7)
  index = len(matrix)
  for i in range(index):
    if(int(matrix[i][1])<10):
      colour = 'blue'
    else:
      if (int(matrix[i][1])<20):
        colour='green'
      else:
       colour ='red'
    folium.Marker(
        location=[matrix[i][3],matrix[i][4]],
        popup=f"{matrix[i][0]} - {matrix[i][1]} - {matrix[i][2]}",  # Number is added to the popup
        icon=folium.DivIcon(html=f'<div style="font-size: 16pt; color: {colour};">{matrix[i][1]}</div>')
    ).add_to(netherlands_map)
  netherlands_map.save("netherlands_map_with_numbers.html")
  return
  
url_list= ["https://www.bbc.com/weather/2759794","https://www.bbc.com/weather/2755003","https://www.bbc.com/weather/2747373","https://www.bbc.com/weather/2745912",'https://www.bbc.com/weather/2743477','https://www.bbc.com/weather/2755420','https://www.bbc.com/weather/2759706','https://www.bbc.com/weather/2755251','https://www.bbc.com/weather/2751738','https://www.bbc.com/weather/2757220','https://www.bbc.com/weather/2756136']
weather_matrix = weather_array_stacker(url_list)
print(weather_matrix)
map_generator(weather_matrix)
