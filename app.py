import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Station = Base.classes.station

Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/percipitation")
def percipitation():
    
    session = Session(engine)
    
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days = 365)

    last_year_percip = (session.query(Measurement.date, Measurement.prcp).
                   filter(Measurement.date >= one_year_ago).
                   order_by(Measurement.date.asc()).
                    all())
    all_rain = []
    
    for date, rain in last_year_percip:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["prcp"] = rain
        all_rain.append(rain_dict)
    
    session.close()
    
    return jsonify(all_rain)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    
    station_activity = (session.query(Measurement.station).
                    group_by(Measurement.station).all())
    
    session.close()
    
    return jsonify(station_activity)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    one_year_temp = dt.date(2017,8,18) - dt.timedelta(days = 365)
    
    last_year_temp = (session.query(Measurement.date, Measurement.tobs).
                 filter(Measurement.station == 'USC00519281').
                 filter(Measurement.date >= one_year_temp)).all()
        
    session.close()
    
    return jsonify(last_year_temp)

@app.route("/api/v1.0/<start>")
def start_range(start):
    
    session = Session(engine)
    
    recorded_temps = [func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    
    
    station_temps = (session.query(Measurement.date, *recorded_temps).
    filter(Measurement.station == 'USC00519281').
    filter(Measurement.date >= start)).all()
    
    session.close()
    
    return jsonify(station_temps)

@app.route("/api/v1.0/<start>/<end>")
def user_range(start, end):
    
    session = Session(engine)
    
    recorded_temps = [func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    
    
    station_temps = (session.query(Measurement.date, *recorded_temps).
    filter(Measurement.station == 'USC00519281').
    filter(Measurement.date >= start).
    filter(Measurement.date <= end)).all()
    
    session.close()
    
    return jsonify(station_temps)



@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/percipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>     start_date: YYYY,MM,DD<br/>"
        f"/api/v1.0/start_date/end_date<br/>     start_date and end_date: YYYT,MM,DD<br/>"
    )


if __name__ == "__main__":
    app.run(debug=True)