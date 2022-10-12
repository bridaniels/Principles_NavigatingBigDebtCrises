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

        ax.set_title("Debt-to-GDP Ratio", fontsize=20)
        sns.lineplot(x=df.index, y=df.debt_to_gdp, ax=ax)
        ax.set_ylabel("Debt-to-GDP Ratio", fontsize=12)

        ax.fill_betweenx(y=y, x1=start_recession01, x2=end_recession01, color='grey', alpha=0.3, label='2001 Recession')
        ax.fill_betweenx(y=y, x1=start_bubble, x2=start_top, color='lightblue', alpha=0.3, label='2008 Emerging Bubble')
        
        ax.legend(loc=2)

        plt.xticks(rotation=50, fontsize=8)
        plt.show()



#calling = DEBT_TO_GDP(start_early90, start_top)
#print(calling.debt_gdp_df())
#calling.plot_debt2gdp_ratio()


print(f" 1990s: {start_early90} \n 2001 Recession Start: {start_recession01} \n 2001 Recession End: {end_recession01} \n Bubble Start: {start_bubble} \n Top Start: {start_top}")
