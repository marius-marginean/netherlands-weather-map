from bs4 import BeautifulSoup
import requests

def bbc_weather_scraper(url):
  '''
  This function is a web scraper that obtains the current weather data in a specific city from a provided bbc weather url. The expected output is a list containing the city name, maximum temperature, minimum temperature and description of current conditions. All values are returned as strings.

  Input: 
  url(str) of the form : "https://www.bbc.com/weather/xxxxxxx".
  Output: 
  str array of the fomr: [City, max_temp, min_temp, description] 
  
  Example functionality:
  input:'https://www.bbc.com/weather/2988507'
  output: ['Paris', ['14°'], ['9°'], ['Sunny and light winds']]
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
  description= clasa.find(class_="wr-day__details__weather-type-description")
  temperature= clasa.find_all(class_="wr-value--temperature--c")
  #constructing the final results vector
  results = [city,temperature[0].contents,temperature[1].contents,description.contents]
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



url_list=['https://www.bbc.com/weather/2653743','https://www.bbc.com/weather/3117735','https://www.bbc.com/weather/2988507']

current_conditions = bbc_weather_scraper(url_list[2])
print (current_conditions)

