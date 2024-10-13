Student: Marginean Marius-Andrei 6031331

This program creates a weather map of the netherlands that shows the current temperature for a series of large cities while also providing a short description of the local weather conditions. The weather data is scraped form a series of links to the bbc weather website for every city using the beautiful soup python library. A separate function is used to determine the decimal coordinates of all of the cities, by scraping the "https://www.geodatos.net/en/coordinates/netherlands/" website. All the data is processed, formated and arranged in a matrix. The map itself is constructed from the matrix using the folium library and saved as an html file that the user can interact with. 

The input to the entire program is an array of "https://www.bbc.com/weather/xxxxxxx" urls corresponding to cities in The Netherlands and the output is an html file that contains an interactive map with the current temperature and weather conditions in each city. 
