import pandas as pd
import numpy as np
import pyodbc

#adding tickers to the instrument table
def add_name(company, ticker, market, sector):
    conn = pyodbc.connect('Driver={SQL Server};' 'Server=DESKTOP-A0508EI\SQLEXPRESS;'
        'Database=MFM_Financial;' 'Trusted_Connection=yes;')
    cursor = conn.cursor() #DESKTOP-A0508EI\SQLEXPRESS

    cursor.execute("INSERT INTO [MFM_Financial].[Findata].[Instrument] VALUES ('"+ company +"','"+ ticker +"','"+ market +"','"+ sector +"')")
    conn.commit()
add_name('Apple','AAPL','NASDAQ','Technology')
add_name('General Eletric','GE','NYSE','Industrial Goods')
add_name('Caterpillar Inc','CAT','NYSE','Industrial Goods')
add_name('3M company','MMM','NYSE','Industrial Goods')
add_name('United technologies','UTX','NYSE','Industrial Goods')
add_name('Coca-cola','KO','NYSE','Consumer Goods')
add_name('Exxon Mobile Corporation','XOM','NYSE','Basic Material')

ticker_set=['AAPL', 'GE', 'CAT', 'MMM', 'UTX', 'KO', 'XOM']

def get_name_id(ticker):
    conn = pyodbc.connect('Driver={SQL Server};' 'Server=DESKTOP-A0508EI\SQLEXPRESS;'  'Database=MFM_Financial;' 'Trusted_Connection=yes;')
    cursor = conn.cursor()

    cursor.execute("SELECT ID FROM [MFM_Financial].[Findata].[Instrument] WHERE StockTicker = '"+ ticker +"'")
    return cursor.fetchone()
#print(get_name_id('KO'))

def add_timeseries_from_csv(ticker,filepath):
    tickerid = get_name_id(ticker)
    conn = pyodbc.connect('Driver={SQL Server};' 'Server=DESKTOP-A0508EI\SQLEXPRESS;' 'Database=MFM_Financial;' 'Trusted_Connection=yes;')
    cursor = conn.cursor()

  

    df=pd.read_csv(filepath)
    
    for i in range(len(df)):
        cursor.execute("INSERT INTO [MFM_Financial].[Findata].[HistPrice] VALUES (" + str(tickerid) + ",CONVERT(DATETIME,'" + str(df.iloc[i]['Date']) + "', 102),"  + str(df.iloc[i]['Open']) + "," + str(df.iloc[i]['High']) + "," + str(df.iloc[i]['Low']) + "," + str(df.iloc[i]['Close']) + "," + str(df.iloc[i]['Volume']) + ")")

    conn.commit()

def populate(ticker_set):
    for ticker in ticker_set:
        add_timeseries_from_csv('AAPL', 'AAPL.csv')
        add_timeseries_from_csv('GE', 'GE.csv')
        add_timeseries_from_csv('CAT', 'CAT.csv')
        add_timeseries_from_csv('MMM', 'MMM.csv')
        add_timeseries_from_csv('UTX', 'UTX.csv')
        add_timeseries_from_csv('KO', 'KO.csv')
        add_timeseries_from_csv('XOM', 'XOM.csv')


    return populate(ticker_set)
    
