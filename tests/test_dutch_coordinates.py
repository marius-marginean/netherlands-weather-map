from bs4 import BeautifulSoup
import requests
import pytest

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

def test_dutch_coordinates():
  #testing case independence 
  assert dutch_coordinates('the-hague') == [52.07667, 4.29861]
  assert dutch_coordinates('The-Hague') == [52.07667, 4.29861]
  assert dutch_coordinates('the hague') == [52.07667, 4.29861]
  assert dutch_coordinates('The Hague') == [52.07667, 4.29861]
  #testing if errors are raised correctly
  with pytest.raises(ValueError, match="Error: Coordinates not found for astremdam"):
    dutch_coordinates("astremdam")
  with pytest.raises(ValueError, match="Invalid input data type"):
    dutch_coordinates([])
  with pytest.raises(ValueError, match="Invalid input data type"):
    dutch_coordinates(901)
test_dutch_coordinates()#running the testing function so the file can be run as a standalone

  