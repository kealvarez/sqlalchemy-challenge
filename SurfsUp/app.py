import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


@app.route("/")
def home():
	return ("Weather API!<br><br>"
		f"/api/v1.0/precipitation<br>"
		f"/api/v1.0/stationn<br>"
		f"/api/v1.0/tobs<br>"
		f"/api/v1.0/start (YYYY-MM-DD)<br>"
		f"/api/v1.0/start/end YYYY-MM-DD)<br>"
	)

@app.route("/api/v1.0/precipitation")
def precipitation():
	results = session.query(measurement).all()
	session.close()


	year_prcp = []
	for result in results:
		year_prcp_dict = {}
		year_prcp_dict["date"] = result.date
		year_prcp_dict["prcp"] = result.prcp
		year_prcp.append(year_prcp_dict)
	
	return jsonify(year_prcp)

@app.route("/api/v1.0/stations")
def stations():
	results = session.query(station.station).all()
	session.close()

	stations = list(np.ravel(results))
	return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temperature():
	Last_Year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

	temperature_results = session.query(measurement.tobs).filter(measurement.date > Last_Year).all()
	session.close()
	temperatures = list(np.ravel(temperature_results))

	return jsonify(temperatures)

@app.route("/api/v1.0/<start>")
def single_date(start):
	Start_Date = dt.datetime.strptime(start,"%Y-%m-%d")

	summary_stats = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.round(func.avg(measurement.tobs))).\
	filter(measurement.date >= Start_Date).all()
	session.close() 
	
	summary = list(np.ravel(summary_stats))

	return jsonify(summary)


@app.route("/api/v1.0/<start>/<end>")
def trip_dates(start,end):
	Start_Date = dt.datetime.strptime(start,"%Y-%m-%d")
	End_Date = dt.datetime.strptime(end,"%Y-%m-%d")
	summary_stats = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.round(func.max(measurement.tobs))).\
	filter(measurement.date.between(Start_Date,End_Date)).all()
	
	session.close()    

	summary = list(np.ravel(summary_stats))

	return jsonify(summary)

	if __name__ == "__main__":
		app.run(debug=True)
