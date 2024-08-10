# Pricing Models Script

# Libraries
import pandas as pd
import numpy as np
from scipy.stats import norm
import scipy.stats as si
import sys as sys
from datetime import datetime
from datetime import timedelta


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
        #mo_string = input("Would you like to run Monte-Carlo Pricing (Y/N)\n")
        #imp_string = input("Would you like to run Implicity Bayesian Pricing (Y/N)\n")

        self.black_scholes = self.__eval__(bs_string)
        self.binomial = self.__eval__(bi_string)
        #self.monte_carlo = self.__eval__(mo_string)
        #self.implicit_bayesian = self.__eval__(imp_string)

    def __load_data__(self):

        try:
            self.stock_df = pd.read_csv("stock_df.csv")
            self.stock_df['Dates'] = pd.to_datetime(self.stock_df['Dates'])

            self.stock_identity = pd.read_csv("stock_identity.csv")
        except:
            print("\nNo Stock Dataframe Present\n")


        try:
            self.security_df = pd.read_csv("securities.csv")
        except:
            print("\nNo Security Dataframe Present\n")

    def run_pricing(self):

        if (self.black_scholes):
            self.__run_bs__()

        if (self.binomial):
            self.__run_bi__()
    

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

        var_dict = self.__setup_bs__()
        self.__calc_bs__(var_dict)

    def __setup_bs__(self):


        S = self.stock_df.tail(1)['Close'].item()
        sigma = self.stock_df.tail(1)['volatility_avg'].item()

        r = 0.0415
        K = int(input("Set the Strike Price: "))


        date_format = "%Y-%m-%d"
        date_string = input("Set the Expiration Date (yyyy-mm-dd): ")


        try:
            date_time = datetime.strptime(date_string, date_format)
        except:
            #print(date_time + " " + self.stock_df['Dates'].max())
            #print("exception " + date_string)
            sys.exit('Invalid DateTime')

        duration = date_time - datetime.strptime(self.stock_identity['End_Date'][0], date_format)
        
        difference_in_years = (duration.days + duration.seconds/86400)/365.2425

        T = difference_in_years

        if (difference_in_years <= 0):
            print(difference_in_years)
            sys.exit('Invalid DateTime (Before Close Period)')

        r_string = input("Set the Risk-Free Rate (type NA for default): ")
        
        if (r_string != "NA"):
            try:
                r = float(r_string)
            except:
                sys.exit('Invalid Risk-Free Rate Value')


        q = self.stock_identity['div_yield_percentage'][0]/100
        
        var_dict = {"S": S, 
                    "K": K, 
                    "T": T,
                    "r": r,
                    "sigma": sigma,
                    "q": q}


        #print(self.stock_df)
        
        return var_dict

    def __calc_bs__(self, var_dict):

        S = var_dict["S"]
        K = var_dict["K"]
        T = var_dict["T"]
        r = var_dict["r"]
        q = var_dict["q"]
        sigma = var_dict["sigma"]

        put = self.__bs_put__(S, K, T, r, q, sigma)
        call = self.__bs_call__(S, K, T, r, q, sigma)

        print("Call Price is " + str(call) + "\n")
        print("Put Price is " + str(put) + ".\n")

        print(str(S) + " " + str(K) + " " + str(T) + " " + str(r) + " " + str(q) + " " + str(sigma))

        return
    
    def __bs_call__(self, S, K, T, r, q, sigma):

        N = norm.cdf

        d1 = (np.log(S/K) + (r - q + sigma**2/2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma* np.sqrt(T)
        return S*np.exp(-q*T) * N(d1) - K * np.exp(-r*T)* N(d2)
    
    def __bs_put__(self, S, K, T, r, q, sigma):

        N = norm.cdf

        d1 = (np.log(S/K) + (r - q + sigma**2/2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma* np.sqrt(T)
        return K*np.exp(-r*T)*N(-d2) - S*np.exp(-q*T)*N(-d1)

    def __run_bi__(self):

        self.__setup_bi__()
        return 0


    def __setup_bi__(self):

        var_dict = self.__setup_bs__()

        try:
            n = int(input("Set Binomial Tree Height"))
        except:
            sys.exit("Invalid Tree Height")

        var_dict['n'] = n
        

        return 0
    

        


def driver():
    
    pricer = pricing_models()
    pricer.run_pricing()

    

driver()



    