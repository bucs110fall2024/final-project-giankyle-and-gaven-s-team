import yfinance as yf
import pandas as pd 
import numpy as np
import seaborn as sb
import datetime

from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
from sklearn import metrics
from datetime import datetime


today = datetime.today().strftime('%Y-%m-%d') 
stock_ticker = input("Enter the stock ticker that you would like to search up: ").upper() #This asks for the ticker that the user wants
data = yf.download(stock_ticker, start = "2016-01-01", end = today) #This gets the retrieval dates, but there is no way of making the day as present as possible for the end function

data = data[['Close']] #We only want to use the closing prices because we need to keep this clean
data['Previous_Close'] = data['Close'].shift(1) #There is no way of getting the previous days price, so we are essentially going to have to shift the data to the left one
data['Price_Change'] = data['Close'] - data['Previous_Close']
data['Next_Close'] = data['Close'].shift(-1)
data.dropna(inplace=True)

X = data['Previous_Close', 'Price_Change']
Y = data['Next_Close']

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size = 0.25, random_state = 42)
model = LinearRegression()
model.fit(X_train,Y_train)

# dat = yf.Ticker("MSFT")
# hd = dat.info
# print(hd)



import matplotlib.pyplot as plt
#Name is going to change later