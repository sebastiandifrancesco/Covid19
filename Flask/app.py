import flask
from flask import render_template, redirect, url_for, jsonify
# from google.cloud import bigquery
import pandas as pd
from pymongo import MongoClient
import schedule
import time
import csv
import numpy as np
from google.cloud import bigquery


app = flask.Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')
app.config["DEBUG"] = True

def getdata():
    # import config
    # !export GOOGLE_APPLICATION_CREDENTIALS="C:\Users\Sebeast\Desktop\GT-Data-Analytics-Bootcamp\Project2\coronavirus19-dashboard-04be631d347b.json"
    client = bigquery.Client()
    QUERY = (
        'SELECT DISTINCT date, country_name, sum(new_persons_fully_vaccinated) OVER (PARTITION BY country_name ORDER BY date) as cum_new_ppl_fully_vaxxed, avg(new_confirmed) OVER (PARTITION BY country_name ORDER BY date) as avg_new_confirmed_cases, avg(new_deceased) OVER (PARTITION BY country_name ORDER BY date) as avg_new_deceased, sum(new_deceased) OVER (PARTITION BY country_name ORDER BY date) as cum_deceased FROM `bigquery-public-data.covid19_open_data.covid19_open_data` WHERE cumulative_persons_fully_vaccinated IS NOT NULL AND new_confirmed IS NOT NULL AND new_deceased IS NOT NULL AND cumulative_deceased IS NOT NULL AND country_name IS NOT NULL ORDER BY date ASC'
        )
    query_job = client.query(QUERY)
    rows = query_job.result()
    date = []
    cum_new_ppl_fully_vaxxed = []
    avg_new_confirmed_cases = []
    avg_new_deceased = []
    cum_deceased = []
    country_name = []
    for row in rows:
        date.append(row.date)
        cum_new_ppl_fully_vaxxed.append(row.cum_new_ppl_fully_vaxxed)
        avg_new_confirmed_cases.append(row.avg_new_confirmed_cases)
        avg_new_deceased.append(row.avg_new_deceased)
        cum_deceased.append(row.cum_deceased)
        country_name.append(row.country_name)
    chartdata = pd.DataFrame(cum_new_ppl_fully_vaxxed,date).reset_index().rename(columns={"index":"date",0:"cum_new_ppl_fully_vaxxed"})
    chartdata["avg_new_confirmed"] = avg_new_confirmed_cases
    chartdata["avg_new_deceased"] = avg_new_deceased
    chartdata["cum_deceased"] = cum_deceased
    chartdata["country"] = country_name
    second_column = chartdata.pop('country')
    chartdata.insert(1, 'country', second_column)
    chartdata = chartdata.dropna().sort_values(["date","country"], ascending=True)

    # Add Global Data
    globalchartdata = chartdata[['date','cum_new_ppl_fully_vaxxed','avg_new_confirmed','avg_new_deceased','cum_deceased']]
    globalchartdata = chartdata.groupby("date").sum().reset_index()
    globalchartdata['country'] = 'Global'
    chartdata = pd.concat([chartdata,globalchartdata])
    chartdata = chartdata.dropna().sort_values(["date","country"], ascending=True)

    # Create Population Data
    # Create dictionary containing dataframes by country
    allGroup = ['Global','Albania', 'Andorra', 'Argentina', 'Aruba', 'Australia', 'Austria',
                    'Azerbaijan', 'Bahrain', 'Bangladesh', 'Belarus', 'Belgium',
                    'Bermuda', 'Bolivia', 'Brazil', 'Bulgaria', 'Cambodia', 'Canada',
                    'Cayman Islands', 'Chile', 'Colombia', 'Costa Rica', 'Croatia',
                    'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Dominica',
                    'Dominican Republic', 'Ecuador', 'El Salvador',
                    'Equatorial Guinea', 'Estonia', 'Falkland Islands',
                    'Faroe Islands', 'Finland', 'France', 'Germany', 'Gibraltar',
                    'Greece', 'Greenland', 'Guatemala', 'Guernsey', 'Guinea',
                    'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran',
                    'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Japan', 'Jersey',
                    'Jordan', 'Kazakhstan', 'Kuwait', 'Laos', 'Latvia', 'Lebanon',
                    'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malaysia', 'Maldives',
                    'Malta', 'Marshall Islands', 'Mexico', 'Moldova', 'Monaco',
                    'Montenegro', 'Montserrat', 'Morocco', 'Netherlands',
                    'New Zealand', 'Norway', 'Oman', 'Palau', 'Palestine', 'Panama',
                    'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Romania',
                    'Russia', 'Saint Helena', 'San Marino', 'Serbia', 'Seychelles',
                    'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia',
                    'South Africa', 'South Korea', 'Spain', 'Sweden', 'Switzerland',
                    'Thailand', 'Tunisia', 'Turkey', 'Ukraine', 'United Arab Emirates',
                    'United Kingdom', 'United States of America', 'Uruguay',
                    'Zimbabwe']
    df_dict = {}
    for country in allGroup:
        df_dict[country] = chartdata[chartdata['country'] == country]
    # Save global data for scatterchart
    scatterchartdata = df_dict["Global"]
    # Create list containing the last row of each dataframe
    barchartdata = []
    for key in df_dict:
        barchartdata.append(df_dict[key].tail(1))
    barchartdata = pd.DataFrame(np.concatenate(barchartdata))
    barchartdata = barchartdata.rename(columns={0:"date",1:"country",2:"cum_new_ppl_fully_vaxxed",3:"avg_new_confirmed",
                               4:"avg_new_deceased",5:"cum_deceased"})
    # Remove global row
    barchartdata = barchartdata.drop(barchartdata.index[0])
    # Scrape population data
    allGroup2 = ['Albania', 'Andorra', 'Argentina', 'Aruba', 'Australia', 'Austria',
                    'Azerbaijan', 'Bahrain', 'Bangladesh', 'Belarus', 'Belgium',
                    'Bermuda', 'Bolivia', 'Brazil', 'Bulgaria', 'Cambodia', 'Canada',
                    'Cayman Islands', 'Chile', 'Colombia', 'Costa Rica', 'Croatia',
                    'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Dominica',
                    'Dominican Republic', 'Ecuador', 'El Salvador',
                    'Equatorial Guinea', 'Estonia', 'Falkland Islands',
                    'Faroe Islands', 'Finland', 'France', 'Germany', 'Gibraltar',
                    'Greece', 'Greenland', 'Guatemala', 'Guernsey', 'Guinea',
                    'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran',
                    'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Japan', 'Jersey',
                    'Jordan', 'Kazakhstan', 'Kuwait', 'Laos', 'Latvia', 'Lebanon',
                    'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malaysia', 'Maldives',
                    'Malta', 'Marshall Islands', 'Mexico', 'Moldova', 'Monaco',
                    'Montenegro', 'Montserrat', 'Morocco', 'Netherlands',
                    'New Zealand', 'Norway', 'Oman', 'Palau', 'Palestine', 'Panama',
                    'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Romania',
                    'Russia', 'Saint Helena', 'San Marino', 'Serbia', 'Seychelles',
                    'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia',
                    'South Africa', 'South Korea', 'Spain', 'Sweden', 'Switzerland',
                    'Thailand', 'Tunisia', 'Turkey', 'Ukraine', 'United Arab Emirates',
                    'United Kingdom', 'United States', 'Uruguay',
                    'Zimbabwe']
    url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'
    tables = pd.read_html(url)
    pop_data = tables[0]
    # Rename and clean country column
    pop_data = pop_data[['Country(or dependent territory)','Population']].rename(columns={'Country(or dependent territory)':'country',
                                                                                        'Population':'population'})
    pop_data['country'] = pop_data['country'].str.split('[').str[0]
    # Filter for only countries in chartdata
    pop_data = pop_data[pop_data['country'].isin(allGroup2)].reset_index()
    # Change United States to Unites States of America
    pop_data.loc[(pop_data.country == 'United States'),'country']='United States of America'
    # Merge data
    barchartdata = pd.merge(left=barchartdata, right=pop_data, left_on='country', right_on='country')
    barchartdata["perc_ppl_fully_vaxxed"] = barchartdata["cum_new_ppl_fully_vaxxed"]/barchartdata["population"]*100
    barchartdata = barchartdata[['country','perc_ppl_fully_vaxxed']]
    barchartdata = barchartdata.sort_values(['perc_ppl_fully_vaxxed'], ascending=False).reset_index(drop=True)
    barchartdata = barchartdata[3:13]



    

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
    heatmap = heatmap.dropna()

    # Convert to csvs to automatically convert date column to string format
    heatmap.to_csv('static/data/heatmap.csv', index=False)
    chartdata.to_csv('static/data/chartdata.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
    barchartdata.to_csv('static/data/barchartdata.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
    scatterchartdata.to_csv('static/data/scatterchartdata.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
    scatterchartdata

    # Read csvs into variables for mongodb insertion
    heatmap = pd.read_csv('static/data/heatmap.csv')
    chartdata = pd.read_csv('static/data/chartdata.csv')
    barchartdata = pd.read_csv('static/data/barchartdata.csv')
    scatterchartdata = pd.read_csv('static/data/scatterchartdata.csv')

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

    # Insert DF into mongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client.Coronavirus19_Dashboard
    collection = db.barchartdata
    data = barchartdata.to_dict(orient='records')
    db.barchartdata.insert_many(data)

    # Insert DF into mongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client.Coronavirus19_Dashboard
    collection = db.scatterchartdata
    data = scatterchartdata.to_dict(orient='records')
    db.scatterchartdata.insert_many(data)

@app.route("/")
def home():
    return render_template("index.html")
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
@app.route("/scatterchart")
def scatterchart():
    return render_template("scatterchart.html")
@app.route("/barchart")
def barchart():
    return render_template("barchart.html")
@app.route("/map")
def map():
    return render_template("map.html")
# Can be called to load current data
@app.route("/load_data")
def load_data():
    getdata()
    return "hello"

# Below route is for future use in case we want to access the data for another project but this route is still in the works

# @app.route("/access_data")
# def access_data():
#     client = MongoClient('mongodb://localhost:27017')
#     db = client.Coronavirus19_Dashboard
#     print(db)
#     chartdata = db.chartdata.find()
#     chartdatadict = []
#     print(chartdata)
#     for position, i in enumerate(chartdata):
#         chartdatadict.append([position,{'cumulative_deceased':i['cumulative_deceased']}])
#         for key in i.keys():
#             print(key)
#     heatmap = db.heatmap.find()
#     return jsonify(chartdatadict)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

    # Schedule getdata to run every day to update data
    schedule.every().day.at("00:00").do(getdata)
    while True:
  
        # Checks whether a scheduled task 
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)   