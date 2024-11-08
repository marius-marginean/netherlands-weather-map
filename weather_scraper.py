from bs4 import BeautifulSoup
import requests
import folium
import re

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

def marker_colour(temperature):
  '''
  This function decides the colour of a marker on the weather map based on the temperature in degrees Celsius at that specific location. The marker will be blue for temperatures under 10 degrees, green for temperatures between 10 and 20 degrees and red for any temperature larger than that. 
  Input:temperature(int)
  Output:marker colour(string)
  Example:
  Input: 30
  Output: 'red'
 '''
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
  '''
  Function that uses folium to create a map of The Netherlands where all of the cities are assigned their corresponding temperature and weather descriptions. Displays the temperature in the correct location on the map. Colours number blue for temperature below 10 degrees Celsius, green for  under 20 degrees Celsius, and red for anything more, using the marker_colour() function. Clicking on the pop up provides information on weather conditions. Uses as an input the output of weather_array_stacker().

  Input: 
  A matrix of the form [[City1(str), temp_max1(int), weather1(str), latitude1(float), longitute1(float)],[City2(str), temp_max2(int), weather2(str), latitude2(float), longitute2(float)]]
  Output: 
  creates an html file named 'netherlands_weather_map.html' that can be opened in a separate web browser
  '''
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
