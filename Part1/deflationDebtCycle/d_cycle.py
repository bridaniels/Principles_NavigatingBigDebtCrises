# Deflationary Debt Cycle

# import libraries 
import os
import pandas as pd
import numpy as np
import datetime as dt 

import matplotlib.pyplot as plt 

# IMPORT API KEY 
from fredapi import Fred
api_key = os.environ.get("FRED_API_KEY")
fred = Fred(api_key=api_key)


# default date range 
default_start = '1960-01-01'
default_end = '2021-10-01'


class ARTICLE_LISTS(): 
    def __init__(self) -> None:
        pass

    def list_us_debt(self): 
        tot_debt = []
        # Millions Quarterly 
        tot_debt.append('ASTLL') #All Sectors; Total Loans; Liability, Level 
        tot_debt.append('ASTDSL') #All Sectors; Total Debt Securities; Liability, Level 
        return tot_debt
    def list_debt_to_gdp(self): 
        tot_debt = []
        # Millions Quarterly 
        tot_debt.extend(self.list_us_debt())
        # Billions Quarterly 
        tot_debt.append('GDP') #Gross Domestic Product
        return tot_debt

    def list_household_nonprofit_debt(self): 
        tot_debt = []
        # Millions Quarterly 
        tot_debt.append('ASHMA')
        tot_debt.append('ASMRMA')
        # Billions Quarterly
        tot_debt.append('MVLOAS')
        tot_debt.append('SLOAS')
        # Billions Monthly
        tot_debt.append('REVOLSL')
        return tot_debt




    def list_government_debt(self): 
        tot_debt = []
    def list_business_debt(self): 
        tot_debt = [] 

        



class BUBBLE(ARTICLE_LISTS): 
    def __init__(self, frequency='q', start=default_start, end=default_end) -> None:
        '''
        Parameters: 
        -----------
        frequency: str
            'd' = daily
            'w' = weekly
            'bw' = biweekly
            'm' = monthly
            'q' = quarterly
            'sa' = semiannual
            'a' = annual
        start + end: datetime or datetime-like str
            '''
        super().__init__()
        self.frequency = frequency
        self.start = start 
        self.end = end


    def debt_to_gdp(self): 
        list = self.list_debt_to_gdp()
        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, kwargs=self.frequency)
        df = pd.DataFrame(df)
        df['GDP'] = df['GDP'] * 1000 #Billions to Millions
        df['debt_sum'] = df.iloc[:,:-1].sum(axis=1)
        df['pcnt_GDP'] = df['debt_sum'] / df['GDP']
        df['yoy_change'] = df['pcnt_GDP'] - df['pcnt_GDP'].shift(4,axis=0)
        return df

# MAKE HOUSEHOLD NUMBERS
# MAKE GOVERNMENT NUMBERS + biz
# KEEP WORKING THROUGH DEBTTOGDP
# what dates to pull for bubbles? 


bub = BUBBLE()
k = bub.debt_to_gdp()
print(k.tail(20))

lol = ARTICLE_LISTS()
lolly = lol.list_household_nonprofit_debt()
print(lolly)