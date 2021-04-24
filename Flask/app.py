import flask
from flask import render_template, redirect, url_for, jsonify
from google.cloud import bigquery
import pandas as pd
from pymongo import MongoClient
import schedule
import time

app = flask.Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')
app.config["DEBUG"] = True

def getdata():
    from google.cloud import bigquery
    import pandas as pd
    # import config
    # !export GOOGLE_APPLICATION_CREDENTIALS="C:\Users\Sebeast\Desktop\GT-Data-Analytics-Bootcamp\Project2\coronavirus19-dashboard-04be631d347b.json"
    client = bigquery.Client()
    QUERY = (
        'SELECT DISTINCT date, sum(new_persons_fully_vaccinated) OVER (ORDER BY date) as cum_new_ppl_fully_vaxxed, avg(new_confirmed) OVER (ORDER BY date) as avg_new_confirmed_cases, new_deceased, cumulative_deceased, country_name FROM `bigquery-public-data.covid19_open_data.covid19_open_data` WHERE cumulative_persons_fully_vaccinated IS NOT NULL AND new_confirmed IS NOT NULL  AND new_deceased IS NOT NULL AND cumulative_deceased IS NOT NULL AND country_name IS NOT NULL ORDER BY date ASC'
        )
    query_job = client.query(QUERY)
    rows = query_job.result()
    date = []
    cum_new_ppl_fully_vaxxed = []
    avg_new_confirmed_cases = []
    new_deceased = []
    cumulative_deceased = []
    country_name = []
    for row in rows:
        date.append(row.date)
        cum_new_ppl_fully_vaxxed.append(row.cum_new_ppl_fully_vaxxed)
        avg_new_confirmed_cases.append(row.avg_new_confirmed_cases)
        new_deceased.append(row.new_deceased)
        cumulative_deceased.append(row.cumulative_deceased)
        country_name.append(row.country_name)
    chartdata = pd.DataFrame(cum_new_ppl_fully_vaxxed,date).reset_index().rename(columns={"index":"date",0:"cum_new_ppl_fully_vaxxed"})
    chartdata["avg_new_confirmed"] = avg_new_confirmed_cases
    chartdata["new_deceased"] = new_deceased
    chartdata["cumulative_deceased"] = cumulative_deceased
    chartdata["country_name"] = country_name
    chartdata = chartdata.dropna()

    # Grab heatmap data
    client = bigquery.Client()
    QUERY = (
            'SELECT date, cumulative_persons_fully_vaccinated, latitude, longitude, country_name FROM `bigquery-public-data.covid19_open_data.covid19_open_data` WHERE date >= "2021-01-01" and date <= current_date() AND cumulative_persons_fully_vaccinated IS NOT NULL AND cumulative_persons_fully_vaccinated != 0 ORDER BY date DESC'
            )
    query_job = client.query(QUERY)
    rows = query_job.result()
    date = []
    cumulative_persons_fully_vaccinated = []
    latitude = []
    longitude = []
    country_name = []
    for row in rows:
        date.append(row.date)
        cumulative_persons_fully_vaccinated.append(row.cumulative_persons_fully_vaccinated)
        latitude.append(row.latitude)
        longitude.append(row.longitude)
        country_name.append(row.country_name)
    heatmap = pd.DataFrame(cumulative_persons_fully_vaccinated,date).reset_index().rename(columns={"index":"date",0:"cumulative_persons_fully_vaccinated"})
    heatmap["latitude"] = latitude
    heatmap["longitude"] = longitude
    heatmap["country_name"] = country_name

    heatmap = heatmap.dropna()

    # Convert to csvs to automatically convert date column to string format
    heatmap.to_csv('static/data/heatmap.csv', index=False)
    chartdata.to_csv('static/data/chartdata.csv', index=False)

    # Read csvs into variables for mongodb insertion
    heatmap = pd.read_csv('static/data/heatmap.csv')
    chartdata = pd.read_csv('static/data/chartdata.csv')

    # Insert DF into mongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client.Coronavirus19_Dashboard
    collection = db.chartdata
    data = chartdata.to_dict(orient='records')
    db.chartdata.insert_many(data)

    # Insert DF into mongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client.Coronavirus19_Dashboard
    collection = db.heatmap
    data = heatmap.to_dict(orient='records')
    db.heatmap.insert_many(data)

@app.route("/")
def home():
    return render_template("map.html")
@app.route("/loaddata")
def loaddata():
    getdata()
    return "hello"
@app.route("/accessdata")
def accessdata():
    client = MongoClient('mongodb://localhost:27017')
    db = client.Coronavirus19_Dashboard
    linechartandscatterchart = db.linechartandscatterchart.find({})
    heatmap = db.heatmap.find({})
    return jsonify(linechartandscatterchart)
@app.route("/map")
def map():
    return render_template("map.html")

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

    # Schedule getdata to run every day to update data
    schedule.every().day.at("00:00").do(getdata)
    while True:
  
        # Checks whether a scheduled task 
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)   