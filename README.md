# sqlalchemy-challenge

# Step 1 - Climate Analysis and Exploration
Use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database

## Precipitation Analysis

→ Start by finding the most recent date in the data set.
→ Using this date, retrieve the last 12 months of precipitation data by querying the 12 preceding months of data. Note you do not pass in the date as a variable to your query.
→ Select only the date and prcp values.
→ Load the query results into a Pandas DataFrame and set the index to the date column.
→ Sort the DataFrame values by date.
→ Plot the results using the DataFrame plot method.

Results:
![image](https://github.com/rls1316/sqlalchemy-challenge/blob/DataBootCamp/Output/Precipitation.png)

## Station Analysis

→ Design a query to calculate the total number of stations in the dataset.
→ Design a query to find the most active stations (i.e. which stations have the most rows?).
→ → List the stations and observation counts in descending order.
→ → Which station id has the highest number of observations?
→ → Using the most active station id, calculate the lowest, highest, and average temperature.

→ Design a query to retrieve the last 12 months of temperature observation data (TOBS).
→ → Filter by the station with the highest number of observations.
→ → Query the last 12 months of temperature observation data for this station.
→ → Plot the results as a histogram with bins=12.

Results: 
![image](https://github.com/rls1316/sqlalchemy-challenge/blob/DataBootCamp/Output/Temperature_by_Frequency.png)

# Step 2 - Climate App

→ Design a Flask API based on the queries developed above
→ Use Flask jsonify to convert the API data into a valid JSON response object.

Results:
(See [app.py](app.py))
