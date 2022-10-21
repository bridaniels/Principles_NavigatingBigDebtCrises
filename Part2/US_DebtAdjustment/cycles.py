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
start_07 = '2007-01-01'
start_08 = '2008-01-01'

'''

2008 Bubble: 2004-2008
- Housing Market Debt Bubble
- Emerging Broader Based Bubble 

'''

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
                Changes in Billions Over Charted Time: \n    \
                Personal Income: {round(pi_change,2)} \n    \
                Personal Consumption Expenditures: {round(pce_change, 2)}\n    \
                Total Consumer Credit Owned and Securitized: {round(totalsl_change, 2)}",
                xy=(0,-0.3),
                xycoords='axes fraction',
                ha='left',
                va='center',
                fontsize=15)

        plt.show()

class DEBT_FINANCED_ASSETS(): 
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
    
    
    def margin_excel(self): 
        df = pd.DataFrame(pd.read_excel("margin-statistics.xlsx"))

        df.index = df['Year-Month']
        df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')
        df = df.drop(['Year-Month'], axis=1)
        
        col_names = ['debit_bal_securities_margin', 'free_credit_bal_cash_acct', 'free_credit_bal_securities_margin']
        df.columns = col_names
        df = df.drop(['free_credit_bal_securities_margin'], axis=1)
        
        df.index.names = ['date']
        df = df[(df.index > self.start) & (df.index < self.end)]
        df = df.iloc[::-1]
        

        return df 
    
    def plot_margin(self): 
        df = self.margin_excel()
        df['debit_bal_growth'] = (df.debit_bal_securities_margin - df.debit_bal_securities_margin.shift(1,axis=0)) / df.debit_bal_securities_margin.shift(1,axis=0)
        df['free_credit_growth'] = (df.free_credit_bal_cash_acct - df.free_credit_bal_cash_acct.shift(1,axis=0)) / df.free_credit_bal_cash_acct.shift(1,axis=0)

        fig, ax = plt.subplots(figsize=(20,8))

        ax.set_title("Margin Statistics During 2008", fontsize=25)
        sns.barplot(x=df.index, y=df.debit_bal_growth, ax=ax, color='red', alpha=0.3, label='Debit Balance Growth')
        sns.barplot(x=df.index, y=df.free_credit_growth, ax=ax, color='green', alpha=0.2, label='Credit Balance Growth')

        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
        ax.set_ylabel("Percent Change in Balance")

        ax.legend(loc=2)
        ax.grid(False)
        plt.xticks(rotation=50, fontsize=9)



        ax2 = ax.twinx()
        sns.lineplot(x=df.index, y=df.debit_bal_securities_margin, ax=ax2, label='Debit Balance')
        sns.lineplot(x=df.index, y=df.free_credit_bal_cash_acct, ax=ax2, label='Free Credit Balance')

        ax2.fill_between(x=df.index, y1=df.free_credit_bal_cash_acct, y2=df.debit_bal_securities_margin, where=df.free_credit_bal_cash_acct>df.debit_bal_securities_margin, label='Able to Meet Margin Call', alpha=0.5)
        ax2.fill_between(x=df.index, y1=df.debit_bal_securities_margin, y2=df.free_credit_bal_cash_acct, where=df.debit_bal_securities_margin>df.free_credit_bal_cash_acct, color='red', alpha=0.5, label='Unable to Meet Margin Call')

        ax2.set_ylabel("Millions", fontsize=15)

        ax2.legend(loc=4)
        ax2.annotate("Red zones show over-leveraged debt-financed asset appreciation", 
                        xy = (0,-0.3), 
                        xycoords = 'axes fraction', 
                        ha = 'left', 
                        va = 'center', 
                        fontsize=15)
        ax2.grid(False)
        plt.xticks(rotation=50, fontsize=9)

        plt.show()

class HOME_PRICES(): 
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

    def home_price_df(self): 
        list = []

        # Home Price Index 
        list.append('USSTHPI') #All-Transactions House Price Index for the United States (iIndex 1980: Q1 = 100) 
        list.append('CSUSHPINSA') # S&P/Case-Shiller U.S. National Home Price Index (indexed to January 2000 at 100 (Not Seasonally Adjusted))

        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, frequency=self.frequency)
        df = pd.DataFrame(df)
        df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')


        jan_idx = df._get_value('2000-01-01','USSTHPI')
        df['to_jan_idx'] = (df.USSTHPI/jan_idx) * 100 

        df['yoy_change'] = (df.CSUSHPINSA - df.CSUSHPINSA.shift(4,axis=0)) / df.CSUSHPINSA.shift(4,axis=0)

        return df 



    def sold_by_df(self): 
        list = []
        # Thousands of Units 
        # HOUSES SOLD BY TYPE OF FINANCING
        list.append('HSTFC') #Cash Purchase 
        list.append('HSTFCM') #Conventional 
        list.append('HSTFFHAI') #FHA Insured 
        list.append('HSTFVAG') #Verteran's Administration (VA) Guaranteed

        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, frequency=self.frequency)
        df = pd.DataFrame(df)
        df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')

        df['con_cash'] = df.HSTFCM + df.HSTFC
        df['con_cash_va'] = df.con_cash + df.HSTFVAG
        df['con_cash_va_fha'] = df.con_cash_va + df.HSTFFHAI

        return df 

    def sales_p_df(self): 
        list=[]
        # Thousands of Units 
        #NEW HOUSES SOLD BY SALES PRICE IN THE US
        list.append('NHSUSSP75O') #BETWEEN $750,000 and Over
        list.append('NHSUSSP50T74') #Between $500,000 and $749,999
        list.append('NHSUSSP40T49') #Between $400,000 and $499,999
        list.append('NHSUSSP30T39') #Between $300,000 and $399,999
        list.append('NHSUSSP20T29') #Between $200,000 and $299,999
        list.append('NHSUSSP15T19') #Between $150,000 and $199,999
        list.append('NHSUSSPU15') #Under $150,000

        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, frequency=self.frequency)
        df = pd.DataFrame(df)
        df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')

        return df 

    def completed_df(self): 
        list=[]
        # Thousands of Units 
        #New Privately-Owned Housing Units Completed
        list.append('COMPUTNSA') #Total Units 
        list.append('COMPU1UNSA') #Single-Family Units 
        list.append('COMPU24UNSA') #Units in Buildings with 2-4 Units 
        list.append('COMPU5MUNSA') #Units in Buildings with 5 Units or More

        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, frequency=self.frequency)
        df = pd.DataFrame(df)
        df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')

        return df 

    def financing_df(self): 
        list = []

        # Dollars
        # AVERAGE SALES PRICE OF HOUSES SOLD BY TYPE OF FINANCING
        list.append('ASPTFC') #Cash Purchase 
        list.append('ASPTFCM') #Conventional
        list.append('ASPTFFHAI') #FHA Insured 
        list.append('ASPTFVAG') #Verteran's Administration (VA) Guaranteed
        list.append('ASPUS') #Houses Sold 
        list.append('ASPNHSUS') #New Houses Sold 
        # MEDIAN SALES PRICE OF HOUSES SOLD BY TYPE OF FINANCING 
        list.append('MSPTFC') #Cash Purchase
        list.append('MSPTFCM') #Conventional
        list.append('MSPTFFHAI') #FHA Insured
        list.append('MSPTFVAG') #Veteran's Administration (VA) Guaranteed 
        list.append('MSPUS') #Houses Sold
        list.append('MSPNHSUS') #New Houses Sold

        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, frequency=self.frequency)
        df = pd.DataFrame(df)
        df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')

        return df 

        

    
    def plot_home_price(self): 
        df = self.home_price_df()

        fig, ax = plt.subplots(figsize=(16,8))

        ax.set_title("S&P/Case-Shiller U.S. National Home Price Index", fontsize=25)
        sns.barplot(x=df.index, y=df.yoy_change, ax=ax, alpha=0.3, label='YOY index change')
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
        ax.set_ylabel('YOY Index Growth')

        plt.xticks(rotation=50, fontsize=10)

        ax2 = ax.twinx()
        sns.lineplot(x=df.index, y=df.CSUSHPINSA, ax=ax2, label='Home Price Index', color='darkblue')
        ax2.axvline(x='2000-01-01', linestyle='--', alpha=0.5, label='January 1, 2000')
        ax2.axhline(y=100, linestyle='--', alpha=0.5)
        ax2.set_ylabel("Index January 2000 = 100")

        ax2.axvspan(xmin=start_recession01, xmax=end_recession01, alpha=0.2, label='2001 Recession',color='yellow')
        ax2.axvspan(xmin=start_bubble, xmax=start_top, alpha=0.2, label='2008 Bubble', color='orange')

        ax2.legend(loc=2)


        plt.show()

    def plot_home_sales(self): 
        df1 = self.sold_by_df()
        df2 = self.sales_p_df()
        df3 = self.completed_df()
        df4 = self.financing_df()

        fig, ax = plt.subplots(2,2, figsize=(25,18))

        # PLOT ONE
        ax[0,0].set_title("Houses Sold by Type of Financing") 
        ax[0,0].plot(df1.HSTFFHAI, label='FHA Insured',alpha=0.4, color='purple')
        ax[0,0].legend(loc=2, fontsize=11)
        ax[0,0].set_ylabel("Thousands of FHA Insured Units", fontsize=12)
        ax2 = ax[0,0].twinx()
        ax2.plot(df1.HSTFCM, label='Conventional')
        ax2.plot(df1.con_cash, label='+ Cash Purchase')
        ax2.plot(df1.con_cash_va, label='+ VA Guaranteed')
        ax2.plot(df1.con_cash_va_fha, label='+ FHA Insured')
        ax2.legend(loc=1, fontsize=12)
        ax2.set_ylabel("Thousands of Units", fontsize=11)
        ax2.grid(False)

        # PLOT TWO 
        ax[0,1].set_title("Houses Sold by Sales Price")
        ax[0,1].plot(df2.NHSUSSP75O, label="$750,000 +")
        ax[0,1].plot(df2.NHSUSSP50T74, label="$500,000 - $749,999")
        ax[0,1].plot(df2.NHSUSSP40T49, label="$400,000 - $499,999")
        ax[0,1].plot(df2.NHSUSSP30T39, label="$300,000 - $399,999")
        ax[0,1].plot(df2.NHSUSSP20T29, label="$200,000 - $299,999")
        ax[0,1].plot(df2.NHSUSSP15T19, label="$150,000 - $199,999")
        ax[0,1].plot(df2.NHSUSSPU15, label="$150,000 - $0", color='green')
        ax[0,1].set_ylabel("Thousands of Units", fontsize=11)
        ax[0,1].legend(loc=6, fontsize=11)

        # PLOT THREE 
        ax[1,0].set_title("Completed Privately-Owned Housing Units")
        ax[1,0].plot(df3.COMPUTNSA, label='Total Units')
        ax[1,0].plot(df3.COMPU1UNSA, label='Single Family Units')
        ax[1,0].plot(df3.COMPU24UNSA, label='2-4 Unit Buildings')
        ax[1,0].plot(df3.COMPU5MUNSA, label='5+ Unit Buildings')
        ax[1,0].legend(loc=2, fontsize=11)
        ax[1,0].set_ylabel("Thousands of Units", fontsize=12)


        # PLOT FOUR 
        ax[1,1].set_title("Average and Medial Home Sale Prices By Financing Type")
        ax[1,1].plot(df4.ASPTFC, label='Average Cash')
        ax[1,1].plot(df4.MSPTFC, label='Median Cash')
        ax[1,1].fill_between(x=df4.index, y1=df4.ASPTFC, y2=df4.MSPTFC, color='blue', alpha=0.2)
        ax[1,1].plot(df4.ASPTFCM, label='Average Conventional')
        ax[1,1].plot(df4.MSPTFCM, label='Median Conventional')
        ax[1,1].fill_between(x=df4.index, y1=df4.ASPTFCM, y2=df4.MSPTFCM, color='lightgreen', alpha=0.2)
        ax[1,1].plot(df4.ASPTFFHAI, label='Average FHA Insured')
        ax[1,1].plot(df4.MSPTFFHAI, label='Median FHA Insured', color='orange')
        ax[1,1].fill_between(x=df4.index, y1=df4.ASPTFFHAI, y2=df4.MSPTFFHAI, color='orange', alpha=0.2)
        ax[1,1].plot(df4.ASPTFVAG, label='Average VA Guarantee')
        ax[1,1].plot(df4.MSPTFVAG, label='Median VA Guarantee', color='darkred')
        ax[1,1].fill_between(x=df4.index, y1=df4.ASPTFVAG, y2=df4.MSPTFVAG, color='red', alpha=0.2)
        ax[1,1].set_ylabel("Average Purchase Price", fontsize=12)
        ax[1,1].legend(loc=2, fontsize=11)


        for a in ax.flatten(): 
            plt.sca(a)
            plt.xticks(rotation=50, fontsize=9)
        plt.subplots_adjust(left=0.2,
                        bottom=0.4,
                        right=1,
                        top=0.9,
                        wspace=0.2,
                        hspace=0.4)
        plt.show()

class MORTGAGE_DATA(): 
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

        def mortgage_df(self): 
            list = []

            #Millions of Dollars
            list.append('ASTMA') #All Sectors; Total Mortgages; Asset, Level

            #Debt Service Payments as a Percent of Disposable Personal Income 
            list.append('TDSP') #TOTAL Household (Mortgage + Consumer)
            list.append('MDSP') #Mortgage 
            list.append('CDSP') #Consumer 

            # Fixed Rate Mortgage Average 
            list.append('MORTGAGE30US') #30-Year
            list.append('MORTGAGE15US') #15-Year 

            # Delinquency Rate 
            list.append('DRSFRMACBS') #Single-Family Residential Mortgages, Booked in Domestic Offices, All Commercial Banks 
            list.append('DRCRELEXFACBS') #Commercial Real Estate Loans (Excluding Farmland), Booked in Domestic Offices, All Commercial Banks 
            list.append('DRFLACBS') #Farmland Loans, Booked in Domestic Offices, All Commercial Banks 

            list.append('DRSFRMT100S') #Single-Family Residential Mortgages, Booked in Domestic Offices, Banks Ranked 1st to 100th Largest in Size by Assets
            list.append('DRSFRMOBS') #Single-Family Residential Mortgages, Booked in Domestic Offices, Banks Not Among the 100 Largest in Size by Assets 
            list.append('DRALT100S') #All Loans, Banks Ranked 1st to 100th Larges in Size by Assets 
            list.append('DRALOBS') #All Loans, Banks Not Among the 100 Largest in Size by Assets 
            list.append('DRSRET100S') #Loans Secured by Real Estate, Banks Ranked 1st to 100th Largest in Size by Assets 
            list.append('DRSREOBS') #Loans Secured by Real Estate, Banks Not Among the 100 Largest in Size by Assets 


            list.append('DRSREACBS') #Loans Secured by Real Estate, All Commercial Banks 
            list.append('DRALACBS') #All Loans, All Commercial Banks
            list.append('DRCLACBS') #Consumer Loans, All Commercial Banks 
            list.append('DRBLACBS') #Business Loans, All Commercial Banks 





print(f" 1990s: {start_early90} \n\
     LTCM Crash: {start_ltcm} \n\
         2001 Recession Start: {start_recession01} \n\
             2001 Recession End: {end_recession01} \n\
                 Bubble Start: {start_bubble} \n\
                     2007 Start: {start_07} \n\
                        Top Start: {start_top} \n\
                            2008 Start: {start_08} ")
