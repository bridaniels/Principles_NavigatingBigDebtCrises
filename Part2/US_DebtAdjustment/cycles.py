# US Debt Adjustment 

# Import Libraries
import os 
import pandas as pd
import numpy as np 
import datetime as dt 

import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='darkgrid', context='talk', palette='rainbow')

# FORMAT PLOT TICKERS  
from matplotlib.ticker import FuncFormatter, PercentFormatter
#PercentFormatter(x): x=how many decimal places you want to move
def fromTMilly(x, pos): 
    #Trillions from Millions
    return '%1.1fT' % (x*1e-6)
formatterTMilly = FuncFormatter(fromTMilly)

# IMPORT FRED API KEY
from fredapi import Fred
api_key = os.environ.get("FRED_API_KEY")
fred = Fred(api_key=api_key)


# Default Date Ranges: 
start_early90 = '1990-01-01'
start_ltcm = '1998-01-01'
start_recession01 = '2001-01-01'
end_recession01 = '2001-10-01'
start_bubble = '2004-01-01'
start_top = '2007-04-01'



class DEBT_TO_GDP():
    def __init__(self, start, end, frequency='q'): 
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
        self.start = start
        self.end = end
        self.frequency = frequency
    
    def debt_gdp_df(self): 
        list = []
        # Billions Quarterly 
        list.append('GDP') #Gross Domestic Product
        # Millions Quarterly 
        list.append('ASTLL') #All Sectors; Total Loans; Liability, Level 
        list.append('ASTDSL') #All Sectors; Total Debt Securities; Liability, Level 

        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, frequency=self.frequency)
        df = pd.DataFrame(df)
        df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')

        df['GDP'] = df['GDP'] * 1000
        df['debt_sum'] = df.iloc[:,:-1].sum(axis=1)

        return df 

    def plot_debt2gdp_ratio(self):
        df = self.debt_gdp_df()
        df['debt_to_gdp'] = df['debt_sum']/df['GDP']
        y = [df['debt_to_gdp'].min(), df['debt_to_gdp'].max()]

        fix, ax = plt.subplots(figsize=(18,6))

        ax.set_title("Debt-to-GDP Ratio", fontsize=25)
        sns.lineplot(x=df.index, y=df.debt_to_gdp, ax=ax)
        ax.set_ylabel("Debt-to-GDP Ratio", fontsize=12)

        ax.fill_betweenx(y=y, x1=start_recession01, x2=end_recession01, color='grey', alpha=0.3, label='2001 Recession')
        ax.fill_betweenx(y=y, x1=start_bubble, x2=start_top, color='lightblue', alpha=0.3, label='2008 Bubble')
        
        ax.legend(loc=2)
        ax.annotate('1990s: Debt-to-GDP Ratio increased slightly. \n1993: Internet access avaliable to general public. \n2001: Recession (dot-com boom -> tightened monetary policy -> lowered IR down to ~1% and 9/11)',
                xy = (0, -0.3),
                xycoords='axes fraction', 
                ha = 'left', 
                va = 'center', 
                fontsize=12)
        plt.xticks(rotation=50, fontsize=15)
        plt.show()

class BUBBLE_FEDFUNDS():
    def __init__(self, start, end, frequency='q'): 
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
        self.start = start
        self.end = end
        self.frequency = frequency

    def fedfunds_df(self): 
        list = []
        list.append('fedfunds')
        
        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, frequency=self.frequency)
        df = pd.DataFrame(df)
        df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')

        return df

    def plot_basicFEDFUNDS(self): 
        df = self.fedfunds_df()
        y = [df['fedfunds'].min(), df['fedfunds'].max()]

        fig, ax = plt.subplots(figsize=(16,6))

        ax.set_title("Fed Funds Rate", fontsize=25)
        sns.lineplot(x=df.index, y=df.fedfunds, ax=ax)
        ax.set_ylabel("Fed Funds Rate", fontsize=12)

        ax.fill_betweenx(y=y, x1=start_recession01, x2=end_recession01, color='grey', alpha=0.3, label='2001 Recession')
        ax.fill_betweenx(y=y, x1=start_bubble, x2=start_top, color='lightblue', alpha=0.3, label='2008 Bubble')
        ax.legend(loc=2)

        ax.annotate('2001 Recession: fed funds rate drops to 1% \n \
            - Stimulated Borrowing and Spending (especially by households) \nTightening monetary policy begins in 2004 as credit markets begin to heat up', 
                    xy = (0, -0.3), 
                    xycoords='axes fraction', 
                    ha = 'left', 
                    va = 'center', 
                    fontsize=15)
        
        plt.xticks(rotation=50, fontsize=10)
        plt.show()
    
class HOUSEHOLD_SPENDING(): 
    def __init__(self, start, end, frequency='q'): 
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
        self.start = start
        self.end = end
        self.frequency = frequency

    def spending(self): 
        list = [] 
        # Billions of Dollars (Monthly)
        list.append('PCE') # Personal Consumption Expenditures 
        list.append('PI') # Personal Income 
        list.append('TOTALSL') # Total Consumer Credit Owned and securitized 
        # FED FUNDS -> in percent format 
        list.append('FEDFUNDS')

        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, frequency=self.frequency)
        df = pd.DataFrame(df)
        df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')

        df['change_pce'] = (df.PCE - df.PCE.shift(4,axis=0))/df.PCE.shift(4,axis=0)
        max_pce = df['change_pce'].idxmax()
        df['change_totalsl'] = (df.TOTALSL - df.TOTALSL.shift(4,axis=0))/df.TOTALSL.shift(4,axis=0)
        max_totalsl = df.change_totalsl.idxmax()
        df['change_pi'] = (df.PI - df.PI.shift(4,axis=0))/df.PI.shift(4,axis=0)
        max_pi = df.change_pi.idxmax()

        df['FEDFUNDS'] = df['FEDFUNDS']/100

        df = df.dropna()

        return df

    def plot_consumer_spending(self): 
        df = self.spending()

        max_pce = df['change_pce'].idxmax()
        max_totalsl = df.change_totalsl.idxmax()
        max_pi = df.change_pi.idxmax()

        pce_change = df.PCE.max() - df.PCE.min()
        totalsl_change = df.TOTALSL.max() - df.TOTALSL.min()
        pi_change =df.PI.max() - df.PI.min()

        fig, ax = plt.subplots(figsize=(16,8))

        ax.set_title("Consumer Spending VS. Borrowing", fontsize=25)

        sns.lineplot(x=df.index, y=df.PCE, ax=ax, label='Personal Consumption Expenditures', alpha=0.6)
        sns.lineplot(x=df.index, y=df.TOTALSL, ax=ax, label='Total Consumer Credit Owned and Securitized', alpha=0.6)
        sns.lineplot(x=df.index, y=df.PI, ax=ax, label='Personal Income', alpha=0.6)
        ax.set_ylabel("Billions", fontsize=15)

        ax.legend(loc='best', bbox_to_anchor=(0.5,-0.43,0.5,0.8))
        plt.xticks(rotation=50, fontsize=10)

        ax2 = ax.twinx()
        sns.lineplot(x=df.index, y=df.change_pce, ax=ax2, label='PCE change')
        sns.lineplot(x=df.index, y=df.change_totalsl, ax=ax2, label='TOTALSL change')
        sns.lineplot(x=df.index, y=df.change_pi, ax=ax2, label='PI change')
        sns.lineplot(x=df.index, y=df.FEDFUNDS, ax=ax2, label='FEDFUNDS', color='green')

        ax2.axvline(x=max_pce, ymin=0, ymax=1, linestyle='--', alpha=0.8, linewidth=0.8, label='PCE Max')
        ax2.axvline(x=max_totalsl, ymin=0,ymax=1, linestyle='--', linewidth=0.8, alpha=0.8, label='TOTALSL Max')
        ax2.axvline(x=max_pi, ymin=0, ymax=1, linestyle='--', linewidth=0.8, alpha=0.8, label='PI Max')

        ax2.set_ylabel("Percent Change YOY", fontsize=15)

        ax2.yaxis.set_major_formatter(PercentFormatter(xmax=1))
        plt.xticks(rotation=50, fontsize=10)

        ax2.annotate(f"Federal Funds Effective Rate (FEDFUNDS) Cuts from 2001 Recession Stimulated Borrowing and Spending by Households \n\
                Changes in Billions: \n    \
                Personal Income: {round(pi_change,2)} \n    \
                Personal Consumption Expenditures: {round(pce_change, 2)}\n    \
                Total Consumer Credit Owned and Securitized: {round(totalsl_change, 2)}",
                xy=(0,-0.3),
                xycoords='axes fraction',
                ha='left',
                va='center',
                fontsize=15)

        plt.show()



#calling = DEBT_TO_GDP(start_early90, start_top)
#print(calling.debt_gdp_df())
#calling.plot_debt2gdp_ratio()


print(f" 1990s: {start_early90} \n LTCM Crash: {start_ltcm} \n 2001 Recession Start: {start_recession01} \n 2001 Recession End: {end_recession01} \n Bubble Start: {start_bubble} \n Top Start: {start_top}")
