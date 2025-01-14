#import libraries
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template


#set up connection to sql through pgadmin
connection_string = "postgres:924runner@localhost:5432/covid_with_dates" #postgres:insert password
engine = create_engine(f'postgresql://{connection_string}')

Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

#reference the tables 
# Covid_cases = Base.classes.covid_cases
# Unemployment_numbers = Base.classes.unemployment_numbers
# Home_price = Base.classes.home_price

Covid_cases = Base.classes.covid_cases_date
Unemployment_numbers = Base.classes.unemployment_numbers_date
Home_price = Base.classes.home_price_date


app = Flask(__name__)

#set up paths for api
@app.route("/")
def welcome():
    return render_template("index2.html")

#covid case data api route
@app.route("/covid_cases_date")
def covid():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Return a list of covid case data including the county, month, new cases, new deaths
    # Query all the data
    # results = session.query(Covid_cases.county, Covid_cases.month, Covid_cases.new_cases, Covid_cases.new_deaths).all()
    results = session.query(Covid_cases.county, Covid_cases.date, Covid_cases.total_case_count).all()

    session.close()

    # Create a dictionary from the row data and append to a list of data
    all_months = []
    # for county, month, new_cases, new_deaths in results:
    for county, date, total_case_count in results:
        covid_case_dict = {}
        covid_case_dict["county"] = county
        covid_case_dict["date"] = date
        covid_case_dict["total_case_count"] = total_case_count
        # covid_case_dict["month"] = month
        # covid_case_dict["new cases"] = new_cases
        # covid_case_dict["new deaths"] = new_deaths
        all_months.append(covid_case_dict)

    return jsonify(all_months)

#set up unemployment numbers data api route
@app.route("/unemployment_numbers_date")
def unemployment():
    # Create our session (link) from Python to the DB
    session = Session(engine)

#return a list of all the info in the sql table, such as county, month, labor_force, employment, unemployment, unemployment_rate
# Query all the data 
    # results = session.query(Unemployment_numbers.county, Unemployment_numbers.month, Unemployment_numbers.labor_force, Unemployment_numbers.employment, Unemployment_numbers.unemployment, Unemployment_numbers.unemployment_rate).all()
    results = session.query(Unemployment_numbers.county, Unemployment_numbers.date, Unemployment_numbers.unemployment).all()

    session.close()

    # Create a dictionary from the row data and append to a list of data
    all_months_unemp = []
    # for county, month, labor_force, employment, unemployment, unemployment_rate in results:
    for county, date, unemployment in results:
        unemp_num_dict = {}
        unemp_num_dict["county"] = county
        unemp_num_dict["date"] = date
        unemp_num_dict["unemployment"] = unemployment
        # unemp_num_dict["month"] = month
        # unemp_num_dict["labor force"] = labor_force
        # unemp_num_dict["employment"] = employment
        # unemp_num_dict["unemployment"] = unemployment
        # unemp_num_dict["unemployment rate"] = unemployment_rate
        all_months_unemp.append(unemp_num_dict)

    return jsonify(all_months_unemp)


# #set up housing data api route
@app.route("/home_price_date")
def housing():
    # Create our session (link) from Python to the DB
    session = Session(engine)

#return a list of all the info in the sql table, such as county, month and price 
# Query all the data 
    # results = session.query(Home_price.county, Home_price.month, Home_price.price).all()
    results = session.query(Home_price.county, Home_price.date, Home_price.price).all()

    session.close()

    # Create a dictionary from the row data and append to a list of data
    all_months_home_price = []
    #for county, month, price in results:
    for county, date, price in results:
        home_price_dict = {}
        home_price_dict["county"] = county
        home_price_dict["date"] = date
        # home_price_dict["month"] = month
        home_price_dict["price"] = price
        all_months_home_price.append(home_price_dict)

    return jsonify(all_months_home_price)


    


if __name__ == '__main__':
    app.run(debug=True)
