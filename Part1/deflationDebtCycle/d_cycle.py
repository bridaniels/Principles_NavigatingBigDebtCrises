# Deflationary Debt Cycle

# import libraries 
import os
import pandas as pd
import numpy as np
import datetime as dt 

import matplotlib.pyplot as plt 

from matplotlib.ticker import FuncFormatter, PercentFormatter

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
        tot_debt.append('ASHMA') #All Sectors; 1-4-Family Residential Mortgages: Asset, Level
        tot_debt.append('ASMRMA') #All Sectors; Multifamily Residential Mortgages; Asset, Level 
        # Billions Quarterly
        tot_debt.append('MVLOAS') #Motor Vehicle Loans Owned and Securitized
        tot_debt.append('SLOAS') #Student Loans Owned and Securitized
        # Billions Monthly
        tot_debt.append('REVOLSL') #Revolving Consumer Credit Owned and Securitized
        return tot_debt
    def list_government_debt(self): 
        tot_debt = []
        # Millions Quarterly 
        tot_debt.append('FGDSLAQ027S') #Federal Government; Debt Securities; Liability, Level
        # Billions Quarterly 
        tot_debt.append('SLGSDODNS') #State and Local Governments; Debt Securities and Loans; Liability, Level
        return tot_debt
    def list_business_debt(self): 
        tot_debt = [] 
        # Millions Quarterly 
        tot_debt.append('ASCMA') #All Sectors; Commercial Mortgages; Asset, Level 
        tot_debt.append('ASFMA') #All Sectors; Farm Mortgages; Asset, Level 
        tot_debt.append('FBDSILQ027S') #Domestic Financial Sectors; Debt Securities; Liability, Level 
        tot_debt.append('FBLL') #Domestic Financial Sectors; Loans; Liability, Level 
        tot_debt.append('NCBDBIQ027S') #Nonfinancial Corporate Business; Debt Securities; Liability, Level 
        tot_debt.append('NCBLL') #Nonfinancial Corporate Business; Loans; Liability, Level 
        tot_debt.append('NNBLL') #Nonfinancial Noncorporate Business; Loans; Liability, Level 
        return tot_debt
    def list_category_debt(self): 
        tot_debt = []
        tot_debt.extend(self.list_household_nonprofit_debt())
        tot_debt.extend(self.list_government_debt())
        tot_debt.extend(self.list_business_debt())
        return tot_debt

        



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


    def df_debt_to_gdp(self): 
        list = self.list_debt_to_gdp()
        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, kwargs=self.frequency)
        df = pd.DataFrame(df)
        df['GDP'] = df['GDP'] * 1000 #Billions to Millions
        df['debt_sum'] = df.iloc[:,:-1].sum(axis=1) #.iloc[:,:-1] to not get GDP column 
        df['pcnt_GDP'] = df['debt_sum'] / df['GDP']
        df['yoy_change'] = df['pcnt_GDP'] - df['pcnt_GDP'].shift(4,axis=0)
        return df

    def df_household_debt(self): 
        list = self.list_household_nonprofit_debt()
        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, kwargs=self.frequency)
        df = pd.DataFrame(df)
        df['debt_sum'] = df.sum(axis=1)
        return df 
    def df_government_debt(self): 
        list = self.list_government_debt()
        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, kwargs=self.frequency)
        df = pd.DataFrame(df)
        df['debt_sum'] = df.sum(axis=1)
        return df 
    def df_business_debt(self): 
        list = self.list_business_debt()
        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, kwargs=self.frequency)
        df = pd.DataFrame(df)
        df['debt_sum'] = df.sum(axis=1)
        return df 
    def df_category_debt(self): 
        list = self.list_category_debt()
        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, kwargs=self.frequency)
        df = pd.DataFrame(df)
        df['debt_sum'] = df.sum(axis=1)
        return df 
    


class BUBBLE_PLOTTING(BUBBLE):
    def __init__(self, frequency='q', start=default_start, end=default_end) -> None:
        super().__init__(frequency, start, end)
        self.frequency = frequency
        self.start = start
        self.end = end 

    def fromTMilly(x,pos): 
        #Trillions from Millions
        return '%1.1fT' % (x*1e-6)

    def plot_debt_to_gdp(self): 
        yoy = self.df_debt_to_gdp()
        fig,ax = plt.subplots(figsize=(19,8))

        ax.plot(yoy.index, yoy.yoy_change, label='YOY GDP Change', color='skyblue')
        ax.bar(yoy.index, yoy.yoy_change, width=50, color='tab:olive')
        ax.fill_between(yoy.index, 0, yoy.yoy_change, color='green', alpha=0.3)
        ax.axhline(y=0, linewidth=0.5, linestyle='--')
        ax.yaxis.set_major_formatter(PercentFormatter())
        ax.set_ylabel('YOY Change in Debt to GDP', fontsize=12)
        ax.legend(loc=2)

        ax2 = ax.twinx()
        ax2.plot(yoy.pcnt_GDP, label='%'+' of GDP', color='0.1', linewidth=2)
        ax2.yaxis.set_major_formatter(PercentFormatter(1))
        ax2.set_ylabel('Total Debt to GDP %', fontsize=12)
        ax2.legend(loc=1)
        ax2.set_title('US Debt to GDP', fontsize=20)

    def plot_category_debt(self):
        biz = self.df_business_debt()
        gov = self.df_government_debt()
        house = self.df_household_debt()
        #formatterTMilly = FuncFormatter(self.fromTMilly)

        fig,ax = plt.subplots(figsize=(16,8))

        ax.plot(biz['debt_sum'], label='Business Debt', color='g', linewidth=2)
        ax.fill_between(biz.index, biz.debt_sum, color='g', alpha=0.4)
        ax.plot(gov['debt_sum'], label='Government Debt', color='b', linewidth=2)
        ax.fill_between(gov.index, gov.debt_sum, color='b', alpha=0.2)
        ax.plot(house['debt_sum'], label='Household + Non-Profit Debt', color='#ffbd74', linewidth=2)
        ax.fill_between(house.index, house.debt_sum, color='#ffa33f', alpha=0.4)

        ax.set_title('Debt by Category', fontsize=20)
        ax.set_ylabel('Debt (in Trillions)', fontsize=12)
        #ax.yaxis.set_major_formatter(formaterTMilly)
        ax.legend(borderpad=1, loc=2)


'''
HOUSEHOLD DEBT NOT QUARTERLY IN BUBBLE()

FUNCFORMATTER TMILLY ISSUE -> ADD TO INIT AS FUNCTION? 
    - CATEGORY DEBT CHART ISSUE 
    - Household debt isn't showing up right -> frequency issue? 

KEEP WORKING THROUGH DEBTTOGDP
what dates to pull for bubbles? 
'''

bub = BUBBLE()
k = bub.df_household_debt()
print(k.tail(20))

#lol = ARTICLE_LISTS()
#lolly = lol.list_household_debt()
#print(lolly)

#plotty = BUBBLE_PLOTTING()
#debty = plotty.plot_category_debt()
#debty

