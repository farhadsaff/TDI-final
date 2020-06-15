# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 10:50:35 2020

@author: fsaff
"""

from flask import Flask, redirect, url_for, render_template, request, Markup
from flask import session
from alpha_vantage.timeseries import TimeSeries
import simplejson as json
import requests
import pandas as pd
import bokeh
from bokeh.embed import components
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
#from flask.ext.session import Session
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.embed import components, file_html
from bokeh.models.sources import ColumnDataSource
from bokeh.resources import CDN

#ts = TimeSeries(key='RY2L4CH6JN0YT3IF',output_format='pandas')
#data, meta_data = ts.get_intraday(symbol='FB',interval='60min', outputsize='full')
app = Flask(__name__)

app.secret_key = 'super secret key'
#app.config['SESSION_TYPE'] = 'filesystem'
#sess.init_app(app)

app.vars={}

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        U=[]
        U.append(user)
        ch1='Open' in request.form
        ch2='High' in request.form
        ch3='low' in request.form
        ch4='Closing' in request.form
        U.extend([ch1,ch2,ch3,ch4])
        session["chk"]=ch1
        session["user"]=U
        
#        checked1 = 'Closing' in request.form
#        session1["user"]=checked1
        return redirect(url_for("user"))
    else:
        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    if "user" in session:
        U=session["user"]
        API_URL = "https://www.alphavantage.co/query"
    #symbols = 'usr'
        data = {
                "function": "TIME_SERIES_DAILY",
                "symbol": U[0],
                "outputsize": "compact",
                "datatype": "json",
                "apikey": "RY2L4CH6JN0YT3IF" }
        response = requests.get(API_URL, data)
        responsej = response.json()
        dresponse=pd.DataFrame(responsej)
        #xdate=list(data_top.index) ["index"]
        for majorkey, subdict in responsej.items():
            print (majorkey)
        for subkey, value in subdict.items():
            print (subkey, value)
            V=(subkey, value)
            df=pd.DataFrame([[i,j,responsej[i][j] ] for i in responsej.keys() for j in responsej[i].keys()],columns=['key', 'inner_key', 'values'])        
            h1=df['values'].apply(pd.Series)
            L1 =h1["1. open"].dropna(axis=0)
            L2 =h1["2. high"].dropna(axis=0)
            L3 =h1["3. low"].dropna(axis=0)
            L4 =h1["4. close"].dropna(axis=0)
            plot = figure()
            print(U[1])
            xdata = range(0, len(L1))
            xdata1=df["inner_key"].iloc[5:105]
            plot = figure(title='Stock prices for %s' % U[0],
            x_axis_label="last 100 days",
            x_axis_type="auto")
            if (U[1]==True):
                plot.line(xdata, L1,line_width=2, legend='Openning price in $')
            if (U[2]==True):
                plot.line(xdata, L2, line_width=2, line_color="red", legend='Highest price in $') 
            if (U[3]==True):
                plot.line(xdata, L3,line_width=2, line_color="blue", legend='Lowest price in $')
            if (U[4]==True):
                plot.line(xdata, L4,line_width=2, line_color="black", legend='Closing price in $')        
            return Markup(file_html(plot, CDN, "my plot"))
    else:
        return render_template("login.html")
        
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

#    sess.init_app(app)
    app.run(port=33507)