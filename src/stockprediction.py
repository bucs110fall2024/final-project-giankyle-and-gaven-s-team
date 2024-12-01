import yfinance as yf
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime

#It takes some time for everything to load
today = datetime.today().strftime('%Y-%m-%d')#This is to get the current time
stock_ticker = input("Enter the stock ticker that you would like to search up: ").upper() #This asks for the ticker that the user wants
data = yf.download(stock_ticker, start = "2016-01-01", end = today)  #This gets the retrieval dates, but there is no way of making the day as present as possible for the end function
data.reset_index(inplace = True) #This makes sure that the dates are lined up
print(data.head()) 
print(data.columns) #I need this line and the one above to make sure that the data is being
#data.to_csv(str(stock_ticker + "_stock_data.csv"))

data['Present_Close'] = data['Adj Close'] #I had trouble with this because I could not have 'Adj Close' as a column by itself 
data['Previous_Close'] = data['Adj Close'].shift(1) #This reads the values that are one above, and then stores them as the 'Previous_Close'
data['Next_Close'] = data['Adj Close'].shift(-1) #This reads the values that are one below, and then stores them as the 'Next_Close'
data['Price_Change'] = data['Present_Close']- data['Previous_Close'] #This calculates the price change by subtracting the current close with the previous close
data.dropna(inplace=True)#This is to drop any values that don't exist

print(data['Price_Change'])

X = data[['Previous_Close', 'Price_Change']]
Y = data['Next_Close']

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size = 0.25) #We can do a new random state
model = LinearRegression() #This is linear regression basically it is a line of best fit(I will do logistic regression next and then average the two values to get something more accurate)
model.fit(X_train,Y_train)

y_pred = model.predict(X_test) 

print("\nSample Predictions (Actual vs Predicted):")
comparison = pd.DataFrame({'Actual': Y_test[:10].values, 'Predicted': y_pred[:10]})
print(comparison)

future_days = 0  # Number of days to predict
future_days = int(input("How many days ahead would you predict?"))
latest_row = data.iloc[-1]
future_predictions = []

for i in range(future_days):
    latest_previous_close = latest_row['Present_Close']
    latest_price_change = latest_row['Present_Close'] - latest_row['Previous_Close']
    
    # Prepare input for the model
    future_input = np.array([[latest_previous_close, latest_price_change]])
    next_pred = model.predict(future_input)[0]
    future_predictions.append(next_pred)
    
    # Update latest_row for the next prediction
    latest_row = {
        'Present_Close': next_pred,
        'Previous_Close': latest_previous_close
    }

# Add future predictions to a DataFrame for visualization
future_dates = pd.date_range(start=data['Date'].iloc[-1] + pd.Timedelta(days=1), periods=future_days)
future_df = pd.DataFrame({'Date': future_dates, 'Predicted_Close': future_predictions})

# Visualization
plt.figure(figsize=(10, 6))
plt.plot(data['Date'], data['Adj Close'], label='Actual Prices', color='blue')
plt.plot(future_df['Date'], future_df['Predicted_Close'], label='Future Predictions', color='orange', linestyle='--')
plt.title(f"{stock_ticker} Stock Price Prediction")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.show()

#Name is going to change later
