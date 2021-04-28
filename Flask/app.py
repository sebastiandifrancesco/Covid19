import flask
from flask import render_template, redirect, url_for, jsonify
from google.cloud import bigquery
import pandas as pd
from pymongo import MongoClient
import schedule
import time
import csv

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
        'SELECT DISTINCT date, country_name, sum(new_persons_fully_vaccinated) OVER (PARTITION BY country_name ORDER BY date) as cum_new_ppl_fully_vaxxed, avg(new_confirmed) OVER (PARTITION BY country_name ORDER BY date) as avg_new_confirmed_cases, avg(new_deceased) OVER (PARTITION BY country_name ORDER BY date) as avg_new_deceased, sum(new_deceased) OVER (PARTITION BY country_name ORDER BY date) as cum_deceased, population FROM `bigquery-public-data.covid19_open_data.covid19_open_data` WHERE cumulative_persons_fully_vaccinated IS NOT NULL AND new_confirmed IS NOT NULL AND new_deceased IS NOT NULL AND cumulative_deceased IS NOT NULL AND country_name IS NOT NULL ORDER BY date ASC'
        )
    query_job = client.query(QUERY)
    rows = query_job.result()
    date = []
    cum_new_ppl_fully_vaxxed = []
    avg_new_confirmed_cases = []
    avg_new_deceased = []
    cum_deceased = []
    country_name = []
    population = []
    for row in rows:
        date.append(row.date)
        cum_new_ppl_fully_vaxxed.append(row.cum_new_ppl_fully_vaxxed)
        avg_new_confirmed_cases.append(row.avg_new_confirmed_cases)
        avg_new_deceased.append(row.avg_new_deceased)
        cum_deceased.append(row.cum_deceased)
        country_name.append(row.country_name)
        population.append(row.population)
    chartdata = pd.DataFrame(cum_new_ppl_fully_vaxxed,date).reset_index().rename(columns={"index":"date",0:"cum_new_ppl_fully_vaxxed"})
    chartdata["avg_new_confirmed"] = avg_new_confirmed_cases
    chartdata["avg_new_deceased"] = avg_new_deceased
    chartdata["cum_deceased"] = cum_deceased
    chartdata["country"] = country_name
    chartdata["population"] = population
    second_column = chartdata.pop('country')
    chartdata.insert(1, 'country', second_column)
    chartdata = chartdata.dropna().sort_values(["date","country"], ascending=True)

    # Create Global Data
    globalchartdata = chartdata[['date','cum_new_ppl_fully_vaxxed','avg_new_confirmed','avg_new_deceased','cum_deceased']]
    globalchartdata = chartdata.groupby("date").sum().reset_index()
    globalchartdata['country'] = 'Global'
    globalchartdata
    chartdata = pd.concat([chartdata,globalchartdata])

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

    chartdata = chartdata.dropna()
    # globalchartdata = globalchartdata.dropna()
    heatmap = heatmap.dropna()

    # Convert to csvs to automatically convert date column to string format
    heatmap.to_csv('static/data/heatmap.csv', index=False)
    chartdata.to_csv('static/data/chartdata.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
    # globalchartdata.to_csv('static/data/globalchartdata.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)


    # Read csvs into variables for mongodb insertion
    heatmap = pd.read_csv('static/data/heatmap.csv')
    chartdata = pd.read_csv('static/data/chartdata.csv')
    # globalchartdata = pd.read_csv('static/data/globalchartdata.csv')

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

    # # Insert DF into mongoDB
    # client = MongoClient('mongodb://localhost:27017')
    # db = client.Coronavirus19_Dashboard
    # collection = db.globalchartdata
    # data = globalchartdata.to_dict(orient='records')
    # db.globalchartdata.insert_many(data)

@app.route("/")
def home():
    return render_template("map.html")
@app.route("/avg_new_confirmed")
def avg_new_confirmed():
    return render_template("avg_new_confirmed.html")
@app.route("/cum_new_ppl_fully_vaxxed")
def cum_new_ppl_fully_vaxxed():
    return render_template("cum_new_ppl_fully_vaxxed.html")
@app.route("/avg_new_deceased")
def avg_new_deceased():
    return render_template("avg_new_deceased.html")
@app.route("/cum_deceased")
def cum_deceased():
    return render_template("cum_deceased.html")
@app.route("/load_data")
def load_data():
    getdata()
    return "hello"
@app.route("/access_data")
def access_data():
    client = MongoClient('mongodb://localhost:27017')
    db = client.Coronavirus19_Dashboard
    print(db)
    chartdata = db.chartdata.find()
    chartdatadict = []
    print(chartdata)
    for position, i in enumerate(chartdata):
        chartdatadict.append([position,{'cumulative_deceased':i['cumulative_deceased']}])
        # print(i)
        # print(type(i))
        for key in i.keys():
            print(key)
    heatmap = db.heatmap.find()
    return jsonify(chartdatadict)
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