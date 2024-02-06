from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func, inspect

# Assuming you've already executed the code for reflecting tables and saving references
# ...

# Create a Flask app
app = Flask(__name__)

# Create a route for the homepage
@app.route('/')
def home():
    return (
        f"Welcome to the Climate Analysis API!"
        f"Available Routes:"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/start"
        f"/api/v1.0/start/end"
    )

# Create a route for precipitation data
@app.route('/api/v1.0/precipitation')
def precipitation():
    most_recent_date = session.query(func.max(measurement.date)).scalar()
    most_recent_date = pd.to_datetime(most_recent_date)
    one_year_ago = most_recent_date - pd.DateOffset(years=1)
    
    results = session.query(measurement.date, measurement.prcp)\
                    .filter(measurement.date >= one_year_ago)\
                    .order_by(measurement.date)\
                    .all()

    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)

# Create a route for station data
@app.route('/api/v1.0/stations')
def stations():
    stations = session.query(measurement.station).all()
    station_list = [station[0] for station in stations]

    return jsonify(station_list)

# Create a route for temperature observations
@app.route('/api/v1.0/tobs')
def tobs():
    specific_station_id = 'USC00519281'
    most_recent_date = session.query(func.max(measurement.date))\
                              .filter(measurement.station == specific_station_id)\
                              .scalar()
    most_recent_date = pd.to_datetime(most_recent_date)
    one_year_ago = most_recent_date - pd.DateOffset(years=1)

    results = session.query(measurement.date, measurement.tobs)\
                    .filter(measurement.station == specific_station_id)\
                    .filter(measurement.date >= one_year_ago)\
                    .order_by(measurement.date)\
                    .all()

    tobs_data = [{'date': date, 'temperature': tobs} for date, tobs in results]

    return jsonify(tobs_data)

# Create a route for temperature statistics for a specified start or start-end range
@app.route('/api/v1.0/')
def temperature_stats_start(start):
    results = session.query(func.min(measurement.tobs),
                             func.avg(measurement.tobs),
                             func.max(measurement.tobs))\
                     .filter(measurement.date >= start)\
                     .all()

    temperature_stats = [{'TMIN': result[0], 'TAVG': result[1], 'TMAX': result[2]} for result in results]

    return jsonify(temperature_stats)

# Create a route for temperature statistics for a specified start-end range
@app.route('/api/v1.0//')
def temperature_stats_start_end(start, end):
    results = session.query(func.min(measurement.tobs),
                             func.avg(measurement.tobs),
                             func.max(measurement.tobs))\
                     .filter(measurement.date >= start)\
                     .filter(measurement.date <= end)\
                     .all()

    temperature_stats = [{'TMIN': result[0], 'TAVG': result[1], 'TMAX': result[2]} for result in results]

    return jsonify(temperature_stats)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)