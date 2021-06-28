# Load the relevant libraries
from flask import Flask, render_template, request, redirect
from utils import *

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
  return render_template('tickerinfo.html')

@app.route('/next',methods=['GET','POST'])
def next():
  
  ticker = request.form['ticker']
  month = request.form['month']
  year = request.form['year']
  features = request.form.getlist('feature')

  # fetch the stock data for the given month and year
  rawdata = getData(ticker)
  df = processData(rawdata, ticker, month, year)

  # check if the dataframe is valid
  if (df is not None) and (not df.empty):
    script, div, cdn_js, cdn_css = graph(df, features, ticker, month, year) 
  else:
    if year == 2021:
      err = f':(....Sorry data not available beyond {month} {year} !'
    else:
      err = f':(....Sorry data requested for {ticker} is not avilable for {month} {year}'
    return render_template('error.html',msg=err)

  return render_template('stockchart.html', stock=ticker, script = script, div= div, cdn_js=cdn_js, cdn_css=cdn_css) 


if __name__ == '__main__':
  app.run(debug=True)


