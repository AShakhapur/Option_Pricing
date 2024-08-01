# Pricing Models Script

# Libraries
import pandas as pd
import numpy as np
from scipy.stats import norm
from datetime import datetime


# Class Definition

class pricing_models:

    def __init__(self):
        # Class Constructor
        print("Hello, this is the pricing_models.py script by Abhay Shakhapur. \nThis script will create a pricing model class based on user input. \nIt will then use the options provided and the dataset made by get_data.rmd to\nuse different pricing algorithms to price the specified assets. Any feedback \nwould be greatly appreciated.\n")
        self.__get_options__()
        self.__load_data__()

    def __eval__(self, str):

        if (str == 'Y'):
            return True
        else:
            return False

    def __get_options__(self): 

        bs_string = input("Would you like to run Black_Scholes Pricing (Y/N)\n")
        bi_string = input("Would you like to run Binomial Pricing (Y/N)\n")
        mo_string = input("Would you like to run Monte-Carlo Pricing (Y/N)\n")
        imp_string = input("Would you like to run Implicity Bayesian Pricing (Y/N)\n")

        self.black_scholes = self.__eval__(bs_string)
        self.binomial = self.__eval__(bi_string)
        self.monte_carlo = self.__eval__(mo_string)
        self.implicit_bayesian = self.__eval__(imp_string)

    def __load_data__(self):

        try:
            self.stock_df = pd.read_csv("stock_df.csv")
        except:
            print("\nNo Stock Dataframe Present\n")

        try:
            self.security_df = pd.read_csv("securities.csv")
        except:
            print("\nNo Security Dataframe Present\n")

    def run_pricing(self):

        if (self.black_scholes):
            self.__run_bs__()
        else:
            exit(0)
    
    def __run_bs__(self):

        #S = Asset_Price
            # Closing Price

        #K = Strike_Price
            # Set Strike Price

        #T = Time_Expiration
            # Set Expiration Date

        #r = Risk-Free rate
            # Default is 0.0415 for the 10-year Treasury rate 
            # on July 30, 2024

        #sigma = Volatility
            # Annualized standard deviation * sqrt(252)
            # 252 trading days in a year 

        #q = Annual Dividend Yield



        print("\nRunning Black_Scholes_Merton Pricing Algorithm\n")

        r = 0.0415

        S = int(input("Set the Strike Price: "))

        date_string = datetime.strptime(input("Set the Expiration Date (mm-dd-yyy): "), '%m/%d/%Y')

        r_string = input("Set the Risk-Free Rate (type NA for default): ")

        if (r_string != "NA"):
            r = int(r_string)
        
        


        print(self.stock_df)

        


        

    
def driver():
    
    pricer = pricing_models()
    pricer.run_pricing()

    

driver()



    