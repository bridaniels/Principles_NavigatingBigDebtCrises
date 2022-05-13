# Deflationary Debt Cycle

# import libraries 
import os
import pandas as pd
import numpy as np
import datetime as dt 

import matplotlib.pyplot as plt 

from typing import List

# FORMAT PLOT TICKERS  
from matplotlib.ticker import FuncFormatter, PercentFormatter
#PercentFormatter(x): x=how many decimal places you want to move
def fromTMilly(x, pos): 
    #Trillions from Millions
    return '%1.1fT' % (x*1e-6)
formatterTMilly = FuncFormatter(fromTMilly)

# IMPORT API KEY 
from fredapi import Fred
api_key = os.environ.get("FRED_API_KEY")
fred = Fred(api_key=api_key)

# DEFAULT DATE RANGE
default_start = '1960-01-01'
default_end = '2021-10-01'



# Pull headers into list to be added to DF 
class DATA_LISTS(): 
    def __init__(self) -> None:
        pass

    def list_us_debt(self, list_urls=False): 
        tot_debt = []
        # Millions Quarterly 
        tot_debt.append('ASTLL') #All Sectors; Total Loans; Liability, Level 
        tot_debt.append('ASTDSL') #All Sectors; Total Debt Securities; Liability, Level 
        if list_urls is not False: 
            return self.list_to_url(tot_debt)
        return tot_debt
    def list_debt_to_gdp(self, list_urls=False): 
        tot_debt = []
        # Millions Quarterly 
        tot_debt.extend(self.list_us_debt())
        # Billions Quarterly 
        tot_debt.append('GDP') #Gross Domestic Product
        if list_urls is not False:
            return self.list_to_url(tot_debt)
        return tot_debt

    def list_household_nonprofit_debt(self, list_urls=False): 
        tot_debt = []
        # Millions Quarterly 
        tot_debt.append('ASHMA') #All Sectors; 1-4-Family Residential Mortgages: Asset, Level
        tot_debt.append('ASMRMA') #All Sectors; Multifamily Residential Mortgages; Asset, Level 
        # Billions Quarterly
        tot_debt.append('MVLOAS') #Motor Vehicle Loans Owned and Securitized
        tot_debt.append('SLOAS') #Student Loans Owned and Securitized
        # Billions Monthly
        tot_debt.append('REVOLSL') #Revolving Consumer Credit Owned and Securitized
        if list_urls is not False: 
            return self.list_to_url(tot_debt)
        return tot_debt
    def list_government_debt(self, list_urls=False): 
        tot_debt = []
        # Millions Quarterly 
        tot_debt.append('FGDSLAQ027S') #Federal Government; Debt Securities; Liability, Level
        # Billions Quarterly 
        tot_debt.append('SLGSDODNS') #State and Local Governments; Debt Securities and Loans; Liability, Level
        if list_urls is not False: 
            return self.list_to_url(tot_debt)
        return tot_debt
    def list_business_debt(self, list_urls=False): 
        tot_debt = [] 
        # Millions Quarterly 
        tot_debt.append('ASCMA') #All Sectors; Commercial Mortgages; Asset, Level 
        tot_debt.append('ASFMA') #All Sectors; Farm Mortgages; Asset, Level 
        tot_debt.append('FBDSILQ027S') #Domestic Financial Sectors; Debt Securities; Liability, Level 
        tot_debt.append('FBLL') #Domestic Financial Sectors; Loans; Liability, Level 
        tot_debt.append('NCBDBIQ027S') #Nonfinancial Corporate Business; Debt Securities; Liability, Level 
        tot_debt.append('NCBLL') #Nonfinancial Corporate Business; Loans; Liability, Level 
        tot_debt.append('NNBLL') #Nonfinancial Noncorporate Business; Loans; Liability, Level 
        if list_urls is not False: 
            return self.list_to_url(tot_debt)
        return tot_debt
    def list_category_debt(self, list_urls=False): 
        tot_debt = []
        tot_debt.extend(self.list_household_nonprofit_debt())
        tot_debt.extend(self.list_government_debt())
        tot_debt.extend(self.list_business_debt())
        if list_urls is not False: 
            return self.list_to_url(tot_debt)
        return tot_debt

    def list_to_url(self, debt_list):
        '''
        debt_list: List[str]
            - returned list from selected list function 
        '''
        for i in range(len(debt_list)): 
            debt_list[i] = 'https://fred.stlouisfed.org/series/'+debt_list[i]
        return debt_list



        



class BUBBLE(DATA_LISTS): 
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
            df[list[i]] = fred.get_series(list[i], self.start, self.end, frequency=self.frequency)
        df = pd.DataFrame(df)
        df['GDP'] = df['GDP'] * 1000
        df['debt_sum'] = df.iloc[:,:-1].sum(axis=1) #.iloc[:,:-1] to not get GDP column 
        df['pcnt_GDP'] = df['debt_sum'] / df['GDP']
        df['yoy_change'] = df['pcnt_GDP'] - df['pcnt_GDP'].shift(4,axis=0)
        return df

    def df_household_debt(self): 
        list = self.list_household_nonprofit_debt()
        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, frequency=self.frequency)
            if fred.get_series_info(list[i]).units_short == 'Bil. of $':
                df[list[i]] = df[list[i]] * 1000
        df = pd.DataFrame(df)
        df['debt_sum'] = df.sum(axis=1)
        return df 
    def df_government_debt(self): 
        list = self.list_government_debt()
        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, frequency=self.frequency)
            if fred.get_series_info(list[i]).units_short == 'Bil. of $':
                df[list[i]] = df[list[i]] * 1000
        df = pd.DataFrame(df)
        df['debt_sum'] = df.sum(axis=1)
        return df 
    def df_business_debt(self): 
        list = self.list_business_debt()
        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, frequency=self.frequency)
            if fred.get_series_info(list[i]).units_short == 'Bil. of $':
                df[list[i]] = df[list[i]] * 1000
        df = pd.DataFrame(df)
        df['debt_sum'] = df.sum(axis=1)
        return df 
    def df_category_debt(self): 
        list = self.list_category_debt()
        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, frequency=self.frequency)
            if fred.get_series_info(list[i]).units_short == 'Bil. of $':
                df[list[i]] = df[list[i]] * 1000
        df = pd.DataFrame(df)
        df['debt_sum'] = df.sum(axis=1)
        return df 
    
    def df_add_gdp(self): 
        g = fred.get_series('GDP', self.start, self.end, frequency=self.frequency)
        g = pd.DataFrame(g)
        g.columns=['GDP']
        g['GDP'] = g['GDP']*1000
        return g 
    


class BUBBLE_PLOTTING(BUBBLE):
    def __init__(self, frequency='q', start=default_start, end=default_end) -> None:
        super().__init__(frequency, start, end)

    def plot_debt_to_gdp(self): 
        yoy = self.df_debt_to_gdp()
        fig,ax = plt.subplots(figsize=(19,8))

        ax.plot(yoy.index, yoy.yoy_change, label='YOY GDP Change', color='skyblue')
        ax.bar(yoy.index, yoy.yoy_change, width=50, color='tab:olive')
        ax.fill_between(yoy.index, 0, yoy['yoy_change'], color='green', alpha=0.3)
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

        fig,ax = plt.subplots(figsize=(16,8))

        ax.plot(biz['debt_sum'], label='Business Debt', color='g', linewidth=2)
        ax.fill_between(biz.index, biz.debt_sum, color='g', alpha=0.4)
        ax.plot(gov['debt_sum'], label='Government Debt', color='b', linewidth=2)
        ax.fill_between(gov.index, gov.debt_sum, color='b', alpha=0.2)
        ax.plot(house['debt_sum'], label='Household + Non-Profit Debt', color='#ffbd74', linewidth=2)
        ax.fill_between(house.index, house.debt_sum, color='#ffa33f', alpha=0.4)

        ax.set_title('Debt by Category', fontsize=20)
        ax.set_ylabel('Debt (in Trillions)', fontsize=12)
        ax.yaxis.set_major_formatter(formatterTMilly)
        ax.legend(borderpad=1, loc=2, fontsize=10)

    def plot_debt_vs_gdp(self, adjusted_GDP=False): 
        df = self.df_debt_to_gdp()
        cdf = self.df_category_debt()

        fig,ax = plt.subplots(figsize=(16,8))

        ax.plot(df['debt_sum'], label='Total US Debt', color='red', linewidth=2)
        ax.plot(cdf['debt_sum'], label='Category US Debt', color='purple', linewidth=1.7)
        ax.plot(df['GDP'], label='Real GDP', color='green', linewidth=2)

        ax.fill_between(df.index, df.GDP, df.debt_sum, color='red', alpha=0.1)
        ax.fill_between(df.index, df.GDP, color='green', alpha=0.2)
        ax.yaxis.set_major_formatter(formatterTMilly)
        ax.set_ylabel('Real GDP vs. Debt', fontsize=12)
        ax.legend(loc=2, borderpad=1, fontsize=10)
        ax.set_title('US GDP vs. Debt', fontsize=20)

        if adjusted_GDP is not False: 
            ax2 = ax.twinx()
            ax2.plot(df.GDP, label='Adjusted Real GDP', color='green', linewidth=1.5, alpha=0.6, linestyle='--')
            ax2.yaxis.set_major_formatter(formatterTMilly)
            ax2.set_ylabel('Adjusted Real GDP', fontsize=12)
            ax2.legend(loc=1, borderpad=1, fontsize=10)





'''
CLEANUP: 


Debt Cycle as a Whole 
1. Start with '08 for each step 
2. Grab a few other smaller recessions -> same analysis 
3. Resize each dataset to fit onto the same X-Axis
    - differences/similarities in the timelines? 

01_early
- do whole cycle overall analysis 
- intro to debt cycle 
02_bubble
- shade out other parts of the cycle on graph so you can kinda see the whole thing
    - focus on the 'bubble' part 
- % change in numbers qoq not yoy -> too short a timespan 
03_top 


'''



#lol = DATA_LISTS()
#lolly = lol.list_household_debt()
#lolly = lol.list_government_debt(list_urls=True)
#print(lolly)
#print(lolly)

#bub = BUBBLE()
#k = bub.df_household_debt()
#print(k.tail(20))

#plotty = BUBBLE_PLOTTING()
#debty = plotty.plot_category_debt()
#debty = plotty.plot_debt_vs_gdp()
#debty



# stacked bar chart work 
# create new df with just positive and negative values to plot 
# US Debt to GDP via categories? 
    # https://matplotlib.org/stable/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html
    # change to dictionary -> dataframe data structure not working properly 
    # would need to sort positive vs. negative values in the DF to organize properly
        # then graph the positive values separate from the negative 
'''
g = d.df_add_gdp()
house = d.df_household_debt()
gov = d.df_government_debt()
biz = d.df_business_debt()


# Calc Percent of GDP
house['pcnt'] = house['debt_sum'] / g['GDP']
gov['pcnt'] = gov['debt_sum'] / g['GDP']
biz['pcnt'] = biz['debt_sum'] / g['GDP']

# Calc YOY Change 
house['yoy'] = house['pcnt'] - house['pcnt'].shift(4,axis=0)
gov['yoy'] = gov['pcnt'] - gov['pcnt'].shift(4,axis=0)
biz['yoy'] = biz['pcnt'] - biz['pcnt'].shift(4,axis=0)

# .fillna(0)
house = house.fillna(0)
gov = gov.fillna(0)
biz = biz.fillna(0)

def separate(data): 
    pos = len(data) * [0]
    neg = len(data) * [0]
    #headers = data.columns 
    for idx, number in enumerate(data['yoy']):
        if number < 0: 
            neg[idx] = number
            pos[idx] = None
        else: 
            pos[idx] = number
            neg[idx] = None
    data['negative'] = neg
    data['positive'] = pos
    return data  

house = separate(house)
gov = separate(gov)
biz = separate(biz)

house = house[['negative', 'positive']].copy()
house.rename(columns= {'negative':'neg_house', 'positive':'pos_house'},inplace=True)
gov = gov[['negative', 'positive']].copy()
gov.rename(columns={'negative':'neg_gov', 'positive':'pos_gov'}, inplace=True)
biz = biz[['negative', 'positive']].copy()
biz.rename(columns={'negative':'neg_biz', 'positive':'pos_biz'}, inplace=True)

cat = pd.concat([house,gov,biz], axis=1, join='outer')

'''
# PLOTTING ATTEMPTS
'''
plt.figure(figsize=(16,8))

plt.bar(biz.index, biz['positive'], width=40, color='skyblue')
plt.bar(biz.index, biz['negative'], width=40, color='skyblue')
plt.bar(house.index, height=house['positive']+biz['positive'], width=40, bottom=biz['positive'], color='tab:olive')
plt.bar(house.index, height=house['negative']+biz['negative'], width=40, bottom=biz['negative'], color='tab:olive')
plt.bar(gov.index, height=gov['positive']+house['positive']+biz['positive'], width=40, bottom=house['positive']+biz['negative'], color='blue')
plt.bar(gov.index, height=gov['negative']+house['negative']+biz['negative'], width=40, bottom=house['negative']+biz['negative'], color='blue')
'''
'''
plt.figure(figsize=(16,8))


plt.bar(biz.index, biz['positive'], width=40, color='skyblue')
plt.bar(gov.index, height=gov['positive']+biz['positive'], width=40, bottom=biz['positive'], color='blue')
plt.bar(house.index, height=house['positive']+biz['positive']+gov['positive'], width=40, bottom=biz['positive']+gov['positive'], color='tab:olive')

plt.bar(biz.index, biz['negative'], width=40, color='skyblue')
plt.bar(gov.index, height=gov['negative']+biz['negative'], width=40, bottom=biz['negative'], color='blue')
plt.bar(house.index, height=house['negative']+biz['negative']+gov['negative'], width=40, bottom=biz['negative']+gov['negative'], color='tab:olive')
'''