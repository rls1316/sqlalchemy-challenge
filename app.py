# Import Flask
from flask import Flask,jsonify

# Python SQL Toolkit and ORM
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import datetime as dt

###################################################################
# Database Setup
###################################################################
# create engine to sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#map engine
Base = automap_base()
Base.prepare(engine, reflect = True)

#table references
Station = Base.classes.station
Measurement = Base.classes.measurement

###################################################################
# Flask Setup
###################################################################
app = Flask(__name__)

###################################################################
# Flask Routes
###################################################################
# Home Route
@app.route("/")
def home():
    return (
        "Welcome to the Climate App API<br>\
    Available routes are<br>\
    Precipitation: /api/v1.0/precipitation<br>\
    Stations: /api/v1.0/stations<br>\
    TOBS: /api/v1.0/tobs<br>\
    Start Date*: /api/v1.0/'start'<br>\
    *replace 'start' with date value prior to 2017-08-24 (ex. /api/v1.0/2016-01-01)<br>\
    End Date*: /api/v1.0/'start'/'end'<br>\
    *replace 'start' and 'end' with date values prior to 2017-08-24 (ex./api/v1.0/2016-01-01/2017-08-23)")

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def prec():
    # Create engine
    session = Session(engine)
    
    # Create Query
    Prec_Query = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date.desc()).all()
    
    session.close()
    
    # Generate Dictionary
    Precipitation = []
    for date, prcp in Prec_Query:
        Prec_Dict = {}
        Prec_Dict['date'] = date
        Prec_Dict['prcp'] = prcp
        Precipitation.append(Prec_Dict)
    return jsonify(Precipitation)
    
# Stations Route
@app.route("/api/v1.0/stations")
def station():
    # Create engine
    session = Session(engine)
    
    # Create Query
    Station_Query = session.query(Station.station, Station.name).all()
    
    session.close()
    
    # Create list
    Station_List = []
    for station in Station_Query:
        Station_List.append(station[0])
        
    return jsonify(Station_List)

# TOBS Route
@app.route("/api/v1.0/tobs")
def tobs():  
    # Create engine
    session = Session(engine)
      
    # Define Dates
    One_Year_Ago_Latest = dt.date(2017,8,23) - dt.timedelta(days = 365)
    Latest_Date = dt.date(2017,8,23)
    
    # Create Queries
    Most_Active_Station_Query = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()[0][0]
    
    Most_Active_Station_Temp_Data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == Most_Active_Station_Query).\
    filter(Measurement.date >= One_Year_Ago_Latest).\
    filter(Measurement.date <= Latest_Date).all()
    
    session.close()
    
    # Create List
    Most_Active_Station_Temp_Data_List = list(Most_Active_Station_Temp_Data)
    
    return jsonify(Most_Active_Station_Temp_Data_List)

# Start Date Route
@app.route("/api/v1.0/<start>")
def startdate(start):
    # Create engine
    session = Session(engine)
    
    # Create Query
    Date_Validation = session.query(func.max(Measurement.date)).all()[0][0]
    
    if (start <= Date_Validation):
        
        Start_Temp_Data = session.query(func.min(Measurement.tobs),\
                                        func.max(Measurement.tobs),\
                                        func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
        session.close()
    
        # Create List 
        Start_Temp_Data_List = list(Start_Temp_Data)
        
        #Successful Message
        message = [f"The min, max, and avg temps for the defined start date are {Start_Temp_Data_List}"]
    
    # Complete else statement for Data Validation query
    
    else:
        message = [f"Warning: Your Start Date is out of the data range, the max date is {Date_Validation}"]   
    
    return jsonify(message)

# End Date Route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    # Create engine
    session = Session(engine)
    
    # Create Query
    Date_Validation = session.query(func.max(Measurement.date)).all()[0][0]
    
    if (start <= Date_Validation):
        
        Start_End_Temp_Data = session.query(func.min(Measurement.tobs),\
                                        func.max(Measurement.tobs),\
                                        func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
        session.close()
    
        # Create List 
        Start_End_Temp_Data_List = list(Start_End_Temp_Data)
        
        #Successful Message
        message = [f"The min, max, and avg temps for the defined range {start} - {end} date are {Start_End_Temp_Data_List}"]
    
    # Complete else statement for Data Validation query
    
    else:
        message = [f"Warning: Your Start Date is out of the data range, the max start date is {Date_Validation}"]   
    
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug = True)