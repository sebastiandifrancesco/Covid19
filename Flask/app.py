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
    client = bigquery.Client()
    QUERY = (
        'SELECT DISTINCT date, sum(new_persons_fully_vaccinated) OVER (ORDER BY date) as cum_new_ppl_fully_vaxxed, avg(new_confirmed) OVER (ORDER BY date) as avg_new_confirmed_cases FROM `bigquery-public-data.covid19_open_data.covid19_open_data` WHERE country_code = "US" AND cumulative_persons_fully_vaccinated IS NOT NULL AND new_confirmed IS NOT NULL ORDER BY date ASC'
        )
    query_job = client.query(QUERY)
    rows = query_job.result()
    # print(rows)
    date = []
    cum_new_ppl_fully_vaxxed = []
    avg_new_confirmed_cases = []
    for row in rows:
        date.append(row.date)
        cum_new_ppl_fully_vaxxed.append(row.cum_new_ppl_fully_vaxxed)
        avg_new_confirmed_cases.append(row.avg_new_confirmed_cases)
    US_linechart = pd.DataFrame(cum_new_ppl_fully_vaxxed,date).reset_index().rename(columns={"index":"date",0:"cum_new_ppl_fully_vaxxed"})
    US_linechart["avg_new_confirmed"] = avg_new_confirmed_cases
    US_linechart["Country"] = "United States of America"

    client = bigquery.Client()
    QUERY = (
        'SELECT DISTINCT date, sum(new_persons_fully_vaccinated) OVER (ORDER BY date) as cum_new_ppl_fully_vaxxed, avg(new_confirmed) OVER (ORDER BY date) as avg_new_confirmed_cases FROM `bigquery-public-data.covid19_open_data.covid19_open_data` WHERE country_code = "BR" AND cumulative_persons_fully_vaccinated IS NOT NULL AND cumulative_persons_fully_vaccinated != 0 AND new_confirmed IS NOT NULL ORDER BY date ASC'
        )
    query_job = client.query(QUERY)
    rows = query_job.result()
    date = []
    cum_new_ppl_fully_vaxxed = []
    avg_new_confirmed_cases = []
    for row in rows:
        date.append(row.date)
        cum_new_ppl_fully_vaxxed.append(row.cum_new_ppl_fully_vaxxed)
        avg_new_confirmed_cases.append(row.avg_new_confirmed_cases)
    BR_linechart = pd.DataFrame(cum_new_ppl_fully_vaxxed,date).reset_index().rename(columns={"index":"date",0:"cum_new_ppl_fully_vaxxed"})
    BR_linechart["avg_new_confirmed"] = avg_new_confirmed_cases
    BR_linechart["Country"] = "Brazil"

    client = bigquery.Client()
    QUERY = (
        'SELECT DISTINCT date, sum(new_persons_fully_vaccinated) OVER (ORDER BY date) as cum_new_ppl_fully_vaxxed, avg(new_confirmed) OVER (ORDER BY date) as avg_new_confirmed_cases FROM `bigquery-public-data.covid19_open_data.covid19_open_data` WHERE country_code = "IN" AND cumulative_persons_fully_vaccinated IS NOT NULL AND new_confirmed IS NOT NULL ORDER BY date ASC'
        )
    query_job = client.query(QUERY)
    rows = query_job.result()
    date = []
    cum_new_ppl_fully_vaxxed = []
    avg_new_confirmed_cases = []
    for row in rows:
        date.append(row.date)
        cum_new_ppl_fully_vaxxed.append(row.cum_new_ppl_fully_vaxxed)
        avg_new_confirmed_cases.append(row.avg_new_confirmed_cases)
    IN_linechart = pd.DataFrame(cum_new_ppl_fully_vaxxed,date).reset_index().rename(columns={"index":"date",0:"cum_new_ppl_fully_vaxxed"})
    IN_linechart["avg_new_confirmed"] = avg_new_confirmed_cases
    IN_linechart["Country"] = "India"

    client = bigquery.Client()
    QUERY = (
        'SELECT DISTINCT date, sum(new_persons_fully_vaccinated) OVER (ORDER BY date) as cum_new_ppl_fully_vaxxed, avg(new_confirmed) OVER (ORDER BY date) as avg_new_confirmed_cases FROM `bigquery-public-data.covid19_open_data.covid19_open_data` WHERE country_code = "IT" AND cumulative_persons_fully_vaccinated IS NOT NULL AND cumulative_persons_fully_vaccinated != 0 AND new_confirmed IS NOT NULL ORDER BY date ASC'
        )
    query_job = client.query(QUERY)
    rows = query_job.result()
    date = []
    cum_new_ppl_fully_vaxxed = []
    avg_new_confirmed_cases = []
    for row in rows:
        date.append(row.date)
        cum_new_ppl_fully_vaxxed.append(row.cum_new_ppl_fully_vaxxed)
        avg_new_confirmed_cases.append(row.avg_new_confirmed_cases)
    IT_linechart = pd.DataFrame(cum_new_ppl_fully_vaxxed,date).reset_index().rename(columns={"index":"date",0:"cum_new_ppl_fully_vaxxed"})
    IT_linechart["avg_new_confirmed"] = avg_new_confirmed_cases
    IT_linechart["Country"] = "Italy"

    client = bigquery.Client()
    QUERY = (
        'SELECT DISTINCT date, sum(new_persons_fully_vaccinated) OVER (ORDER BY date) as cum_new_ppl_fully_vaxxed, avg(new_confirmed) OVER (ORDER BY date) as avg_new_confirmed_cases FROM `bigquery-public-data.covid19_open_data.covid19_open_data` WHERE country_code = "ID" AND cumulative_persons_fully_vaccinated IS NOT NULL AND cumulative_persons_fully_vaccinated != 0 AND new_confirmed IS NOT NULL ORDER BY date ASC'
        )
    query_job = client.query(QUERY)
    rows = query_job.result()
    date = []
    cum_new_ppl_fully_vaxxed = []
    avg_new_confirmed_cases = []
    for row in rows:
        date.append(row.date)
        cum_new_ppl_fully_vaxxed.append(row.cum_new_ppl_fully_vaxxed)
        avg_new_confirmed_cases.append(row.avg_new_confirmed_cases)
    ID_linechart = pd.DataFrame(cum_new_ppl_fully_vaxxed,date).reset_index().rename(columns={"index":"date",0:"cum_new_ppl_fully_vaxxed"})
    ID_linechart["avg_new_confirmed"] = avg_new_confirmed_cases
    ID_linechart["Country"] = "Indonesia"

    linechart = pd.concat([US_linechart,BR_linechart,IN_linechart,IT_linechart,ID_linechart]).reset_index(drop=True)

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

    linechart = linechart.dropna()

    heatmap.to_csv('static/data/heatmap.csv', index=False)
    linechart.to_csv('static/data/linechart.csv', index=False)

    heatmap = pd.read_csv('static/data/heatmap.csv')
    linechart = pd.read_csv('static/data/linechart.csv')

    # Insert DF into mongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client.Coronavirus19_Dashboard
    collection = db.linechart
    data = linechart.to_dict(orient='records')
    db.linechartandscatterchart.insert_many(data)

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