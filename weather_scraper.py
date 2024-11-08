from bs4 import BeautifulSoup
import requests
import folium
import re

def bbc_weather_scraper(url):
  """
  This function is a web scraper that obtains the current weather data in a specific city from a provided BBC Weather URL. 
  Args:
    url (str): URL of the form 'https://www.bbc.com/weather/xxxxxxx'.
  Returns:
      list: A list containing:
        - City (str): The name of the city.
        - max_temp (int): Maximum temperature in Celsius.
        - description (str): Description of current conditions. 

  Example:
        >>> bbc_weather('https://www.bbc.com/weather/2988507')
        ['Paris', 14, 'Sunny and light winds']  # Values may vary depending on current conditions.
  """
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
  """
  Determines the geographic coordinates of a specified Dutch city using a web scraper.

  The function takes the name of a city in the Netherlands, is case-insensitive, and can handle names with multiple words.

  Args:
      city (str): The name of a Dutch city.

  Returns:
      list of float: A list containing the coordinates of the city in decimal degree format:
        - Latitude (float): The latitude of the city.
        - Longitude (float): The longitude of the city.

  Example:
      >>> dutch_coordinates('The Hague')
      [52.07667, 4.29861]
  """
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
  """
  Generates a matrix with city names, maximum temperatures, weather conditions, and coordinates using a list of BBC Weather URLs.

  This function uses `bbc_weather_scraper()` to obtain weather data and `dutch_coordinates()` to retrieve geographic coordinates.
  Note: The URLs must correspond to cities in the Netherlands for the `dutch_coordinates()` function to work correctly.

  Args:
     url_list (list of str): A list of BBC Weather URLs in the format 
        ["https://www.bbc.com/weather/xxxxxxx", "https://www.bbc.com/weather/yyyyyyy"], where each URL is specific to a Dutch city.

  Returns:
     list of list: A matrix where each inner list contains:
        - City (str): The name of the city.
        - temp_max (int): The maximum temperature in Celsius.
        - weather (str): Description of current weather conditions.
        - latitude (float): The latitude of the city in decimal degree format.
        - longitude (float): The longitude of the city in decimal degree format.

  Example:
      >>> weather_array_stacker(["https://www.bbc.com/weather/2988507", "https://www.bbc.com/weather/2759794"])
      [['Paris', 14, 'Sunny and light winds', 52.07667, 4.29861],
      ['Amsterdam', 10, 'Partly cloudy', 52.3676, 4.9041]]
  """
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

def marker_colour(temperature):
  """
 Determines the color of a marker on the weather map based on the temperature in degrees Celsius.

 The function assigns:
    - 'blue' for temperatures below 10 degrees,
    - 'green' for temperatures between 10 and 20 degrees,
    - 'red' for temperatures above 20 degrees.

  Args:
    temperature (int): The temperature in degrees Celsius.

  Returns:
    colour (str): The color of the marker ('blue', 'green', or 'red').

  Example:
    >>> marker_colour(30)
    'red'
  """
  if type(temperature) is not int:
    raise ValueError("Invalid input data type")
  if temperature<10:
      colour = 'blue'
  else:
      if temperature<20:
       colour='green'
      else:
       colour ='red'
  return colour

def map_generator(url_list):
  """
  Creates an interactive weather map of The Netherlands using Folium, where each city is marked with its corresponding temperature and weather description.

  This function uses `weather_array_stacker()` to gather weather data and `marker_colour()` to determine the color of the marker based on the temperature. The map displays:
    - A color-coded marker (blue for temperatures below 10°C, green for temperatures between 10-20°C, red for temperatures above 20°C).
    - A popup with weather conditions that appear when clicking on a marker.

  Args:
      url_list (list of str): A list of BBC Weather URLs in the form 
        ["https://www.bbc.com/weather/xxxxxxx", "https://www.bbc.com/weather/yyyyyyy"], where each URL corresponds to a Dutch city.

  Returns:
      None: The function generates an HTML map and saves it as 'netherlands_weather_map.html' for viewing in a web browser.

  Example:
      >>> map_generator(["https://www.bbc.com/weather/2988507", "https://www.bbc.com/weather/2759794"])
      # Creates 'netherlands_weather_map.html' with markers showing weather data for cities in the URLs.
   """
  matrix = weather_array_stacker (url_list)
  netherlands_map = folium.Map(location=[52.3784, 4.9009], zoom_start=7)#location of the map
  index = len(matrix)#number of markers
  for i in range(index):#creates a marker for each point
    #determines the colour of marker based on temperature
    colour=marker_colour(int(matrix[i][1]))
    folium.Marker(
        location=[matrix[i][3],matrix[i][4]],#places marker on coordinates
        popup=f"{matrix[i][0]} - {matrix[i][1]} - {matrix[i][2]}",  # Weather description is added to the pop up
        icon=folium.DivIcon(html=f'<div style="font-size: 16pt; color: {colour};">{matrix[i][1]}</div>')#uses temperature as number icon of the correct colour
    ).add_to(netherlands_map)
  netherlands_map.save("netherlands_weather_map.html")#saves complete map
  return

url_list = ["https://www.bbc.com/weather/2759794","https://www.bbc.com/weather/2755003","https://www.bbc.com/weather/2747373","https://www.bbc.com/weather/2745912",'https://www.bbc.com/weather/2743477','https://www.bbc.com/weather/2755420','https://www.bbc.com/weather/2759706','https://www.bbc.com/weather/2755251','https://www.bbc.com/weather/2751738','https://www.bbc.com/weather/2757220','https://www.bbc.com/weather/2756136']

map_generator(url_list)

