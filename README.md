# FinalProject

I used Niche.com to scrape data about national universities. There is not an API key or Client secret. 

In order to use the program with plotly you will need to have a browser window open at the time the program is run. 

If running the program without information saved in the database, please uncomment line 524.

One of the main functions is get_colleges_for_state. This takes the state name and returns the information for the universities in that state in the form of a list of dictionaries called list_of_dictionaries. This list is then saved into a json file called data.json. Another large function used is the insert_data function. This inserts data from the json file into the database. Another large function is the plotting function which takes the user input, gets the data for that state’s universities and plots the information accordingly. 

To run the program, enter a state abbreviation and the type of data you want to see in a graph:
rank = the national ranking of the university
	students = the number of students who attend the university
	tuition = in state and out of state tuition
	acceptance = the acceptance rate for the university

For example: ca tuition
