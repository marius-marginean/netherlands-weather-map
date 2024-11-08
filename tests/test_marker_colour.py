import pytest
def marker_colour(temperature):
  '''
  This function decides the colour of a marker on the weather map based on the temperature in degrees Celsius at that specific location. The marker will be blue for temperatures under 10 degrees, green for temperatures between 10 and 20 degrees and red for any temperature larger than that. 
  Input:temperature(int)
  Output:colour(string)
  Example:
  Input: 30
  Output: red
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

def test_marker_colour():
 #testing normal functions
 assert marker_colour(5) == 'blue'
 assert marker_colour(15) == 'green'
 assert marker_colour(30) == 'red'
 assert marker_colour(-20) == 'blue'
 #testing errors being raised correctly in edge cases
 with pytest.raises(ValueError, match="Invalid input data type"):
    marker_colour([])
 with pytest.raises(ValueError, match="Invalid input data type"):
    marker_colour('cat')