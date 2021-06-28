import requests
import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Spectral4
from bokeh.resources import CDN

def getData(ticker):

  load_dotenv(find_dotenv())
  apikey = os.environ.get("ALPHA_VANTAGE_API_KEY")

  # Accordong to the alphavantage documentation website
  function   = 'TIME_SERIES_DAILY_ADJUSTED'
  outputsize = 'full'
  url = f'https://www.alphavantage.co/query?function={function}&symbol={ticker}&outputsize={outputsize}&apikey={apikey}'
  
  rawdata = requests.get(url)
  data = rawdata.json()

  # check for valid json output
  if 'Error Message' in data:
      print(data['Error Message'])
      return None

  return data['Time Series (Daily)']


def processData(data, ticker, month, year):
  ''' get data for a ticker label for specific month and year '''

  month_to_num = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7,
  'August':8, 'September':9, 'October':10, 'November':11, 'December':12}

  month = month_to_num[month]
  year = int(year)

  if data is not None:
    df = pd.DataFrame(data).transpose() 
    colnames = ['open','high','low','close','adj_close']
    df = df.iloc[:,:-3]
    df.columns = colnames
    df.index = pd.to_datetime(df.index)
  else:
    print("Something is wrong with the raw data !")
    return None

  # data available only for 2014-2021
  try:
    if year == 2021 and month > 6:
      print("Sorry data not available beyond June 2021 !")
      return None
    else:
      dfm = df.loc[(df.index.year == year) & (df.index.month== month)]
      return dfm
  except:
      flash("Sorry data outside the 2014-2021 timeframe is not available!")
      return None

def graph(dataframe, features, ticker, month, year):

  p = figure(x_axis_type="datetime", title=f"{ticker} Stock Price Data ({month} {year})")
  p.title.align = 'center'
  p.grid.grid_line_alpha=0.5
  p.xaxis.axis_label = 'Date'
  p.yaxis.axis_label = 'Price (USD)'

  for feature,color in zip(features,Spectral4):
    p.line(dataframe.index, dataframe[feature], line_width=2, color=color, legend_label=feature)

  p.legend.location = "top_left"
  script, div = components(p)
  
  cdn_jslist = CDN.js_files
  cdn_csslist = CDN.css_files

  cdn_js = (cdn_jslist[0] if len(cdn_jslist)>0 else cdn_jslist)
  cdn_css = (cdn_csslist[0] if len(cdn_csslist)>0 else cdn_csslist)

  return script, div, cdn_js, cdn_css




