# Import Flask
from flask import Flask,jsonify

# Python SQL Toolkit and ORM
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as NP
import datetime as DT

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
    Start Date: /api/v1.0/<start><br>\
    End Date: /api/v1.0/<start>/<end>")

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
    return ""

# Start Date Route
@app.route("/api/v1.0/<start>")
def start():
    return ""

# End Date Route
@app.route("/api/v1.0/<start>/<end>")
def end():
    return ""



if __name__ == "__main__":
    app.run(debug = True)