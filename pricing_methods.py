# Code File

# Libraries
import pandas as pd
import numpy as np
from scipy.stats import norm
import sys as sys
from datetime import datetime
import argparse

# Class Definition

class PricingModel:

    def __init__(self):
        # Class Constructor
        print("Hello, this is the pricing_models.py script by Abhay Shakhapur. \nThis script will create a pricing model class based on user input. \nIt will then use the options provided and the dataset made by get_data.rmd to\nuse different pricing algorithms to price the specified assets. Any feedback \nwould be greatly appreciated.\n")

        self.args = self.__get_options__()
        self.__load_data__()       

    def __get_options__(self):



        parser = argparse.ArgumentParser(

            prog = "pricing_models.py",
            description="This program runs the selected option pricing model based on user input.\n Atleast one option must be selected.",
            epilog = "--End of Help--"
            )
        
        parser.add_argument('-bs', "--black_scholes", action='store_true', help="Run Black-Scholes Pricing")
        parser.add_argument('-bi', "--binomial", action='store_true', help="Run Binomial Pricing")
        parser.add_argument('-mc', "--monte_carlo", action='store_true', help="Run Monte-Carlo Pricing")
        parser.add_argument('-ip', "--implicit_bayesian", action='store_true' , help="Run Implicit Bayesian Pricing")
                

        return parser.parse_args()
    
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

        return 0
    
    def run_pricing(self):

        if (self.args.black_scholes):
            model = BlackScholesModel()
        elif (self.args.binomial):
            model = BinomialModel()
        elif (self.args.monte_carlo):
            model = MonteCarlo()
        elif (self.args.implicit_bayesian):
            print("Not Ready Yet")
            sys.exit(1)

        model.run_pricing()

        sys.exit(0)
        

class BlackScholesModel(PricingModel):

    def __init__(self):

        super().__load_data__()
        self.var_dict = self.__setup_bs__()

    def run_pricing(self):

        #S = Asset_Price
            # Spot Price

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

        self.__calc_bs__()

        return

    def __setup_bs__(self):

        S = self.stock_df.tail(1)['Close'].item()
        sigma = self.stock_df.tail(1)['volatility_avg'].item()

        r = 0.0415

        K = int(input("Set the Strike Price: "))
        try:
            K = int(K)
        except:
            False

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

    def __calc_bs__(self):

        S = self.var_dict["S"]
        K = self.var_dict["K"]
        T = self.var_dict["T"]
        r = self.var_dict["r"]
        q = self.var_dict["q"]
        sigma = self.var_dict["sigma"]

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


class BinomialModel(PricingModel):

    def __init__(self):

        super().__load_data__()
        self.var_dict = self.__setup_bi__()

    def __setup_bi__(self):

        S = self.stock_df.tail(1)['Close'].item()
        sigma = self.stock_df.tail(1)['volatility_avg'].item()

        r = 0.0415

        K = int(input("Set the Strike Price: "))
        try:
            K = int(K)
        except:
            False

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

        try:
            n = int(input("Set Binomial Tree Height: "))
        except:
            sys.exit("Invalid Tree Height")

        try: 
            am_str = input("What Option Model should the pricing be (American/European)? ")
        except:
            sys.exit("Invalid Region Status")

        if (am_str == "American"):
            american = True
        elif (am_str == "European"):
            american = False
        else:
            sys.exit("Invalid Region Status")

        var_dict['n'] = n
        var_dict['american'] = american

        return var_dict
    
    def run_pricing(self):

        print("\nRunning Binomial Pricing Algorithm\n")
        
        self.__calc_bi__()

        return

    def __calc_bi__(self):

        S = self.var_dict['S']
        K = self.var_dict['q']
        T = self.var_dict['T']
        r = self.var_dict['r']
        q = self.var_dict['q']
        sigma = self.var_dict['sigma']
        n = self.var_dict['n']
        american = self.var_dict['american']

        delta = self.var_dict['T'] / self.var_dict['n']

        u = np.exp(sigma * np.sqrt(delta))
        d = np.exp(-sigma * np.sqrt(delta))
        p = (np.exp((r - q) * delta) - d) / (u - d)

        self.var_dict['delta'] = delta
        self.var_dict['u'] = u
        self.var_dict['d'] = d
        self.var_dict['p'] = p

        call = self.__bi_call__()
        put = self.__bi_put__()

        print("Call price is: " + str(call))
        print("Put price is: " + str(put))

        return 1
    
    def __bi_call__(self):

        S = self.var_dict['S']
        K = self.var_dict['K']
        N = self.var_dict['n']
        u = self.var_dict['u']
        p = self.var_dict['p']
        r = self.var_dict['r']
        dt = self.var_dict['delta']
        d = self.var_dict['d']
        american = self.var_dict['american']

        ST = np.zeros(N + 1)
        for i in range(N + 1):
            ST[i] = S * (u ** (N - i)) * (d ** i)

        option_values = np.maximum(0, ST - K)

        for j in range(N - 1, -1, -1):
            for i in range(j + 1):
                option_values[i] = np.exp(-r * dt) * (p * option_values[i] + (1 - p) * option_values[i + 1])
                if (american):
                    option_values[i] = np.maximum(option_values[i], ST[i] - K)

        option_price = option_values[0]

        return option_price
    
    def __bi_put__(self):

        S = self.var_dict['S']
        K = self.var_dict['K']
        N = self.var_dict['n']
        u = self.var_dict['u']
        p = self.var_dict['p']
        r = self.var_dict['r']
        dt = self.var_dict['delta']
        d = self.var_dict['d']
        american = self.var_dict['american']

        ST = np.zeros(N + 1)
        for i in range(N + 1):
            ST[i] = S * (u ** (N - i)) * (d ** i)

        option_values = np.maximum(0, K - ST)

        for j in range(N - 1, -1, -1):
            for i in range(j + 1):

                option_values[i] = np.exp(-r * dt) * (p * option_values[i] + (1 - p) * option_values[i + 1])

                if (american):

                    option_values[i] = np.maximum(option_values[i], K - ST[i])
        
        option_value = option_values[0]

        return option_value


class MonteCarlo(PricingModel):

    def __init__(self):

        super().__load_data__()
        self.var_dict = self.__setup_mc__()

    def __setup_mc__(self):

        S = self.stock_df.tail(1)['Close'].item()
        sigma = self.stock_df.tail(1)['volatility_avg'].item()

        r = 0.0415

        K = int(input("Set the Strike Price: "))
        try:
            K = int(K)
        except:
            False

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
        
        try:
            num_sims = int(input("Number of Simulations to Run (): "))
        except:
            sys.exit('Invalid Number of Sims')

        try:
            num_steps = int(input("Number of steps in simulation: "))
        except:
            sys.exit('Invalid number of steps')

        var_dict = {"S": S, 
                    "K": K, 
                    "T": T,
                    "r": r,
                    "sigma": sigma,
                    "q": q,
                    "nsteps": num_steps,
                    "nsims": num_sims
                    }

        var_dict["dt"] = var_dict["T"] / var_dict["nsteps"]
        var_dict["discount"] = np.exp(-var_dict['r'] * var_dict["T"])
        
        return var_dict

    def run_pricing(self):
        print("\nRunning Monte-Carlo Pricing Algorithm (Currently European Only)\n")
        
        self.__calc_mc__()
        return

    def __calc_mc__(self):

        S = self.var_dict['S']
        K = self.var_dict['q']

        r = self.var_dict['r']
        q = self.var_dict['q']
        sigma = self.var_dict['sigma']


        nsteps = self.var_dict['nsteps']
        nsims = self.var_dict['nsims']
        dt = self.var_dict['dt']
        discount = self.var_dict['discount']


        price_paths = np.zeros((nsims, nsteps + 1))
        price_paths[:, 0] = S

        for i in range(1, nsteps + 1):
            z = np.random.standard_normal(nsims)
            price_paths[:, i] = price_paths[:, i-1] * np.exp((r-q-0.5 * sigma**2)*dt + sigma * np.sqrt(dt) * z)
        
        call_pay = np.maximum(price_paths[:, -1] - K, 0)
        put_pay = np.maximum(K - price_paths[:, -1], 0)

        call = discount * np.mean(call_pay)
        put = discount * np.mean(put_pay)

        print("Call price is: " + str(call))
        print("Put price is: " + str(put))

        return
    
    