import yfinance as yf
import pandas as pd 
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime
from datetime import timedelta

class stockpredictor:
    '''
    This is a class that predicts stock prices using historical data and linear regression
  
    Args:
    None
    '''

    def __init__(self, stock_ticker):
        
        """
        Initializes the stock predictor with the stock ticker symbol.


        Args:
        stock_ticker (str): The stock symbol for the company (e.g., "AAPL" for Apple).
        """

        self.stock_ticker = stock_ticker
        self.data = None
        self.model = None
        self.sorted_stocks = None
#It takes some time for everything to load

    def data_fetch(self):
        '''
        This downloads the Yahoo Finance data from 01-01-2016 for the given stock ticker.
        ['Present_Close'] (Adjusted Close)
        ['Previous_Close'] (Shifted one day backwards)
        ['Next_Close'] (Shifted one day forward)
        ['Price_Change'] (Difference between Present_close and Previous_close)
      
        Args:
        None
      
        '''

        today = datetime.today().strftime('%Y-%m-%d')#This is to get the current time
        self.data = yf.download(self.stock_ticker, start = "2016-01-01", end = today)  #This gets the retrieval dates, but there is no way of making the day as present as possible for the end function
        self.data.reset_index(inplace = True) #This makes sure that the dates are lined up
        # print(self.data.head()) 
        # print(self.data.columns) #I need this line and the one above to make sure that the self.data is being
        #self.data.to_csv(str(stock_ticker + "_stock_self.data.csv"))

        self.data['Present_Close'] = self.data['Adj Close'] #I had trouble with this because I could not have 'Adj Close' as a column by itself 
        self.data['Previous_Close'] = self.data['Adj Close'].shift(1) #This reads the values that are one above, and then stores them as the 'Previous_Close'
        self.data['Next_Close'] = self.data['Adj Close'].shift(-1) #This reads the values that are one below, and then stores them as the 'Next_Close'
        self.data['Price_Change'] = self.data['Present_Close']- self.data['Previous_Close'] #This calculates the price change by subtracting the current close with the previous close
        self.data.dropna(inplace=True)#This is to drop any values that don't exist


    def model_training(self):
        """
        Trains a linear regression model to predict the 'Next_Close' based on 'Previous_Close' and 'Price_Change'.
        
        Splits the data into training and testing sets and fits the model on the training data.
        The trained model is used to predict the stock price, and the actual vs predicted values
        are stored in the 'sorted_stocks' attribute.
      
        Args:
        None
        """
 
        X = self.data[['Previous_Close', 'Price_Change']]
        Y = self.data['Next_Close']

        X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size = 0.25) #We can do a new random state
        self.model = LinearRegression() #This is linear regression basically it is a line of best fit(I will do logistic regression next and then average the two values to get something more accurate)
        self.model.fit(X_train,Y_train)
        y_pred = self.model.predict(X_test)

        self.sorted_stocks = pd.DataFrame({'Actual': Y_test, 'Predicted': y_pred})
        self.sorted_stocks['Date'] = self.data.loc[Y_test.index, 'Date']
        self.sorted_stocks = self.sorted_stocks.sort_values(by="Date", ascending=True)

        # print("Top Predictions Sorted by Date (Chronological Order):")
        # print(self.sorted_stocks.head(-1))
        

    # print(type(sorted_stocks))

    def stock_prediction(self, forecast_days):
        '''
        Predicts the stocks using linear regression from historical information downloaded
      
        Arg:
        forecast_days (int): The number of days to predict ahead.
      
        Returns:
        pd.DataFrame: This is a dataframe that contains forecasted stock prices
          
        '''

        last_close = self.data['Adj Close'].iloc[-1]
        forecast_dates = pd.date_range(start=self.data['Date'].iloc[-1] + timedelta(days=1), periods=forecast_days)
        forecast_df = pd.DataFrame({'Date': forecast_dates})
        future_data = pd.DataFrame({
            'Previous_Close': [last_close] * forecast_days,  
            'Price_Change': [0] * forecast_days             
        })
        future_prices = []
        for i in range(forecast_days):
            input_data = future_data.iloc[i:i+1]
            next_close = self.model.predict(input_data)[0]  
            future_prices.append(next_close)  
            if i + 1 < forecast_days:
                
                future_data.at[i + 1, 'Previous_Close'] = next_close

        forecast_df['Predicted_Close'] = future_prices

        print("\nForecasted Prices:")
        print(forecast_df)
        return forecast_df

    def plot_machinelearning_model(self,forecast_df= None,):
        """
        Plots the actual vs predicted stock prices along with the forecasted stock prices.


        Args:
           forecast_df (pd.DataFrame, optional): DataFrame containing the forecasted prices. Defaults to None.
        """

        plt.figure(figsize=(12, 6))
        plt.plot(self.sorted_stocks['Date'], self.sorted_stocks['Actual'], label='Actual', marker='o', color='green')
        plt.plot(self.sorted_stocks['Date'], self.sorted_stocks['Predicted'], label='Predicted', marker='o', color='red')
        if forecast_df is not None:
            plt.plot(forecast_df['Date'], forecast_df['Predicted_Close'], label='Forecasted Prices', linestyle='--', color='blue')
        plt.title(self.stock_ticker + 'Actual, Predicted, and Forecasted Stock Prices')
        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        plt.legend()
        plt.xticks(rotation=45)
        plt.show()

# if __name__ == "__main__":
#     try:
#         stock_ticker = input("Enter the stock ticker that you would like to search up: ").upper()
#         predictor = stockpredictor(stock_ticker)
#         predictor.data_fetch()
#         predictor.model_training()
#         forecast_days = int(input("Enter the number of days to predict ahead: "))
#         forecast_df = predictor.stock_prediction(forecast_days)
#         predictor.plot_machinelearning_model(forecast_df)
#     except ValueError as e:
#         print(f"Value Error: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")


# model, sorted_stocks = model_training(self) #THIS IS GOING TO BE SENT OUT LATER ON ***DO NOT DELETE***

# forecast_df = stock_prediction(self.data, model) #THIS IS GOING TO BE SENT OUT LATER ON ***DO NOT DELETE***

# plot_machinelearning_model(sorted_stocks, forecast_df) #THIS IS GOING TO BE SENT OUT LATER ON ***DO NOT DELETE***

#This asks for the ticker that the user wants