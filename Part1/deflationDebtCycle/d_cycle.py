# Deflationary Debt Cycle

# import libraries 
import os
import pandas as pd
import numpy as np
import datetime as dt 

import matplotlib.pyplot as plt 
import seaborn as sns
sns.set(style='darkgrid', context='talk', palette='rainbow')

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
default_end = '2019-10-01'



class RANGE():  
    def __init__(self, cycle_start, cycle_end, frequency='q'): 
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
        self.cycle_start = cycle_start
        self.cycle_end = cycle_end
        self.frequency = frequency

    # BUBBLE = Debt Growth GREATER than Income Growth 
    def bubble_range(self):
        list = self.list_gdi_debt()
        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.cycle_start, self.cycle_end, frequency='a')
        df = pd.DataFrame(df)
        df['GDI yoy Growth'] = df['GDI'] / df['GDI'].shift(1,axis=0)
        df['Debt yoy Growth'] = (df['ASTLL'] + df['ASTDSL']) / (df['ASTLL'].shift(1,axis=0) + df['ASTDSL'].shift(1,axis=0))
        df['Income vs Debt yoy Change'] = df['GDI yoy Growth'] - df['Debt yoy Growth']
        bubble_df = pd.DataFrame(df['Income vs Debt yoy Change'])
        bubble_df = bubble_df[bubble_df['Income vs Debt yoy Change'] <= 0]
        bubble_df.index = pd.to_datetime(bubble_df.index)
        bubble_start = bubble_df.first_valid_index().strftime('%Y-%m-%d')
        bubble_end = bubble_df.last_valid_index().strftime('%Y-%m-%d')
        return bubble_start, bubble_end 
    
    def top_range(self): 
        list = self.list_fed_funds()
        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.cycle_start, self.cycle_end, frequency='q')
        df = pd.DataFrame(df)
        df['Yearly Rate Change'] = df['DFF'] - df['DFF'].shift(4,axis=0)
        df['Quarterly Rate Change'] = df['DFF'] - df['DFF'].shift(1,axis=0)
        df.index = pd.to_datetime(df.index)

        # BOUNDARIES ARE ARBITRARY NUMBERS I PICKED OUT VIA 2008 DATA 
        tighten_df = df.loc[df['Yearly Rate Change'] > 1]
        top_start = tighten_df.first_valid_index().strftime('%Y-%m-%d')
        plateau_df = df.loc[df['Yearly Rate Change'] < -2]
        # works with end of bubble 
        top_end = plateau_df.last_valid_index().strftime('%Y-%m-%d')
        # before end of bubble
        #top_end = plateau_df['Yearly Rate Change'].idxmax().strftime('%Y-%m-%d')
        return top_start, top_end

    def depression_range(self):
        # Nominal Growth Rate Above Nominal Interest Rate  
        gdp_exp, gdp_deflation, nom_ir = self.list_nominal_ir_gdp()
        # All Billions/Quarterly 

        # [StateLocalGovExp, FederalGovExp, GovExp, NetExports, GrossPrivateBizInvestment, PersonalConsumptionExp(monthly)] 
        df = {}
        list = gdp_exp
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.cycle_start, self.cycle_end, frequency='q')
        df = pd.DataFrame(df)
        df['GDP_EXP'] = df.sum(axis=1)

        # [GDPImplicitPriceDeflator(%change, monthly), GDP]
        df2 = {}
        list2 = gdp_deflation
        for i in range(len(list2)): 
            df2[list2[i]] = fred.get_series(list2[i], self.cycle_start, self.cycle_end, frequency='q')
        df2 = pd.DataFrame(df2)
        df2['GDP_DEFLATION'] = df2['A191RI1Q225SBEA'] * df2['GDP']

        #Nominal Interest Rate
        df3 = {}
        list3 = nom_ir
        for i in range(len(list3)): 
            df3[list3[i]] = fred.get_series(list3[i], self.cycle_start, self.cycle_end, frequency='q')
        df3 = pd.DataFrame(df3)
        df3['NOM_IR'] = df3.sum(axis=1)

        return df, df2, df3



    def all_cycle_ranges(self):
        cycle_boundaries = []
        bubble_start, bubble_end = self.bubble_range()
        cycle_boundaries.append(bubble_start)
        cycle_boundaries.append(bubble_end)


        return cycle_boundaries

    # LISTS    
    def list_gdi_debt(self, list_urls=False): 
        tot_debt = []
        # Billions Quarterly 
        tot_debt.append('GDI') #Gross Domestic Income (Seasonally Adjusted )
        # Millions Quarterly 
        tot_debt.append('ASTLL') #All Sectors; Total Loans; Liability, Level 
        tot_debt.append('ASTDSL') #All Sectors; Total Debt Securities; Liability, Level 
        if list_urls is not False: 
            return self.list_to_url(tot_debt)
        return tot_debt
    def list_fed_funds(self, list_urls=False): 
        fed_fund = []
        fed_fund.append('DFF')
        if list_urls is not False: 
            return self.list_to_url(fed_fund)
        return fed_fund
    def list_t_bonds(self, list_urls=False): 
        t_bonds = ['DGS2', 'DGS5', 'DGS10', 'DGS20', 'DGS30']
        if list_urls is not False: 
            return self.list_to_url(t_bonds)
        return t_bonds
    def list_nominal_ir_gdp(self, list_urls=False):
        # All Billions/Quarterly 
        # [StateLocalGovExp, FederalGovExp, GovExp, NetExports, GrossPrivateBizInvestment, PersonalConsumptionExp(monthly)] 
        gdp_exp = ['W079RCQ027SBEA','W019RCQ027SBEA', 'W068RCQ027SBEA', 'NETEXP', 'W987RC1Q027SBEA', 'PCE']
        # [GDPImplicitPriceDeflator(%change, monthly), GDP]
        gdp_deflation = ['A191RI1Q225SBEA', 'GDP']
        nom_ir = ['DGS2']
        if list_urls is not False: 
            return self.list_to_url(gdp_exp, gdp_deflation, nom_ir)
        return gdp_exp, gdp_deflation, nom_ir
    

    def list_to_url(self, debt_list):
        '''
        debt_list: List[str]
            - returned list from selected list function 
        '''
        for i in range(len(debt_list)): 
            debt_list[i] = 'https://fred.stlouisfed.org/series/'+debt_list[i]
        return debt_list

# 2008 BUBBLE PARAMS
start_2008 = '2002-01-01'
end_2008 = '2012-01-01'
bub = RANGE(start_2008, end_2008, 'a') #'a'=annual
bubble_start_08, bubble_end_08 = bub.bubble_range()
print("2008 Bubble Start: {}\n2008 Bubble End: {}".format(bubble_start_08, bubble_end_08))
top_start_08, top_end_08 = bub.top_range()
print("2008 Top Start: {}\n2008 Top End: {}".format(top_start_08, top_end_08))


class GDP_MEASUREMENTS(): 
    def __init__(self, cycle_start, cycle_end, frequency='q'):
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
        self.cycle_start = cycle_start
        self.cycle_end = cycle_end
        self.frequency = frequency
    
    def gdp_growth(self): 
        list = ['GDP', 'fedfunds']
        
        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.cycle_start, self.cycle_end, frequency='q')
        df = pd.DataFrame(df)
        df['GDP_qoq_growth'] = df['GDP'] - df['GDP'].shift(1,axis=0)
        df['GDP_change'] = (df['GDP'] - df['GDP'].shift(1,axis=0)) / df['GDP'].shift(1,axis=0)
        df['fedfunds_change'] = (df['fedfunds'] - df['fedfunds'].shift(1,axis=0)) / df['fedfunds'].shift(1,axis=0)
        df = df.dropna()

        return df
    
    def gdp_recession(self): 
        gdp_df = self.gdp_growth()
        
        recession = gdp_df[gdp_df['GDP_qoq_growth'] <= 0]
        start_date = recession.first_valid_index().strftime('%Y-%m-%d')

        return recession, start_date






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
    
    def list_bubble_range(self, list_urls=False): 
        tot_debt = []
        # Billions Quarterly 
        tot_debt.append('GDI') #Gross Domestic Income (Seasonally Adjusted )
        # Millions Quarterly 
        tot_debt.append('ASTLL') #All Sectors; Total Loans; Liability, Level 
        tot_debt.append('ASTDSL') #All Sectors; Total Debt Securities; Liability, Level 
        if list_urls is not False: 
            return self.list_to_url(tot_debt)
        return tot_debt

    def list_t_bond(self, list_urls=False): 
        t_bond = ['DGS2', 'DGS5', 'DGS10', 'DGS20', 'DGS30']
        if list_urls is not False: 
            return self.list_to_url(t_bond)
        return t_bond 
    def list_equity_price_index(self,list_urls=False): 
        equity = ['NASDAQCOM']
        if list_urls is not False: 
            return self.list_to_url(equity)
        return equity
    def list_asset_price_changes(self, list_urls=False): 
        list = ['NASDAQCOM', 'GDI', 'DRCCLACBS', 'GDP']
        if list_urls is not False: 
            return self.list_to_url(list)
        return list

    def list_to_url(self, debt_list):
        '''
        debt_list: List[str]
            - returned list from selected list function 
        '''
        for i in range(len(debt_list)): 
            debt_list[i] = 'https://fred.stlouisfed.org/series/'+debt_list[i]
        return debt_list



class DATA_DF(DATA_LISTS): 
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

    def df_t_bond(self): 
        list = self.list_t_bond()
        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, frequency=self.frequency)
        df = pd.DataFrame(df)
        df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')
        return df    
    def df_equity_price_index(self): 
        list = self.list_equity_price_index()
        df = {}
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, frequency=self.frequency)
        df = pd.DataFrame(df)
        df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')
        return df 
    def df_asset_price_changes(self): 
        list = self.list_asset_price_changes()
        df = {} 
        for i in range(len(list)): 
            df[list[i]] = fred.get_series(list[i], self.start, self.end, frequency='q')
        df =  pd.DataFrame(df)
        df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')
        df['Equity_Change'] = (df['NASDAQCOM']-df['NASDAQCOM'].shift(1,axis=0)) / df['NASDAQCOM']
        df['Income_Change'] = (df['GDI'] - df['GDI'].shift(1,axis=0)) / df['GDI']
        df['Credit_Change'] = (df['DRCCLACBS'] - df['DRCCLACBS'].shift(1,axis=0)) / df['DRCCLACBS']
        df['GDP_Change'] = (df['GDP'] - df['GDP'].shift(1,axis=0)) / df['GDP']
        return df



class PLOTTING(DATA_DF):
    def __init__(self, frequency='q', start=default_start, end=default_end) -> None:
        super().__init__(frequency, start, end)


    def plot_debt_to_gdp(self): 
        yoy = self.df_debt_to_gdp()
        fig,ax = plt.subplots(figsize=(19,8))


        ax.plot(yoy.index, yoy.yoy_change, label='YOY GDP Change', color='skyblue', linewidth=0.9)
        ax.bar(yoy.index, yoy.yoy_change, width=50, color='tab:olive')
        ax.fill_between(yoy.index, 0, yoy['yoy_change'], color='green', alpha=0.3)
        ax.axhline(y=0, linewidth=0.5, linestyle='--')
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.set_ylabel('YOY Change in Debt to GDP', fontsize=12)
        ax.legend(loc=2)

        ax2 = ax.twinx()
        ax2.plot(yoy.pcnt_GDP, label='%'+' of GDP', color='0.1', linewidth=2)
        ax2.yaxis.set_major_formatter(PercentFormatter(1))
        ax2.set_ylabel(' Total Debt to GDP %', fontsize=12)
        ax2.legend(loc=1)
        ax2.set_title('US Debt to GDP', fontsize=20)
    def plot_bubble_debt_to_gdp(self): 
        yoy = self.df_debt_to_gdp()
        yoy['three_yr_change'] = yoy['pcnt_GDP'] - yoy['pcnt_GDP'].shift(12,axis=0)
        yoy['two_yr_change'] = yoy['pcnt_GDP'] - yoy['pcnt_GDP'].shift(8,axis=0)
        two_three = yoy.copy(deep=True)
        two_three = two_three.iloc[::4, :]

        fig,ax=plt.subplots(figsize=(16,8))

        ax.bar(two_three.index, two_three['three_yr_change'], label='3yr Change', width=50, color='g')
        ax.bar(two_three.index, two_three['two_yr_change'], label='2yr Change', width=50, color='tab:olive')
        ax.axhline(y=0.2, linewidth=0.5, linestyle='--', color='r')
        ax.axhline(y=0.25, linewidth=0.5, linestyle='--', color='r')
        ax.fill_between(two_three.index, 0.2, 0.25, color='r', alpha=0.2)
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.set_ylabel('Change in Debt to GDP', fontsize=12)
        ax.legend(loc=2)
        ax.set_title('Change in Debt to GDP Ratio During a Bubble', fontsize=20)

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

    def plot_t_bond_maturity(self): 
        df = self.df_t_bond()

        plt.figure(figsize=(16,8))

        plt.plot(df['DGS30'], label='30-Year Bond', color='mediumblue')
        plt.plot(df['DGS20'], label='20-Year Bond', color='royalblue')
        plt.plot(df['DGS10'], label='10-Year Note', color='limegreen')
        plt.plot(df['DGS5'], label='5-Year Note', color='springgreen')
        plt.plot(df['DGS2'], label='2-Year Note', color='green')

        plt.title("U.S. Treasury Securities Market Yield (Constant Maturity)", fontsize=20)
        plt.ylabel("Market Yield (in percent", fontsize=12)
        plt.tick_params(rotation=50)
        plt.legend(loc=2)
        plt.grid(True, linestyle='--', alpha=0.9)
    def plot_SR_LR(self): 
        df = self.df_t_bond()
        df['SR - LR'] = df['DGS2'] - df['DGS30']
        df['SR/LR'] = df['DGS2'] / df['DGS30']
        even_yield = [i for i, val in enumerate(df['SR/LR']) if val==1]
        inverted = [i for i, val in enumerate(df['SR/LR']) if val>1]

        fig, ax = plt.subplots(figsize=(16,8))

        ax.plot(df['SR - LR'], label='SR - LR', color='blue')
        ax.tick_params(rotation=50)
        ax.grid(True, linestyle='--', alpha=0.9)
        ax.set_ylabel('SR - LR', fontsize=12, color='blue')
        ax.legend(loc=2)

        ax2 = ax.twinx()
        ax2.plot(df['SR/LR'], label='SR / LR', color='purple')
        ax2.plot(df['SR/LR'][even_yield], linestyle='none', color='red', marker='o', label='SR = LR')
        ax2.plot(df['SR/LR'][inverted], linestyle='none', color='yellow', marker='o', label='inverted')
        ax2.set_ylabel('SR / LR', fontsize=12, color='purple')
        ax2.legend(loc=1)

        ax2.set_title('YIELD CURVE', fontsize=20)
    def plot_equity_price_index(self): 
        df = self.df_equity_price_index()

        fig,ax = plt.subplots(figsize=(16,8))

        ax.plot(df['NASDAQCOM'], label='NASDAQ Composite Index', color='green')
        ax.set_ylabel('Index Feb 5, 1971 = 100', fontsize=12, color='green')
        ax.legend(loc=2)
        ax.tick_params(rotation=50)
        ax.grid(True, linestyle='--', alpha=0.9)
        ax.set_title('Equity Price Index')
    def plot_asset_price_changes(self): 
        df = self.df_asset_price_changes()
        df2 = self.df_t_bond()
        df2['2yr_Change'] = (df2['DGS2']- df2['DGS2'].shift(1,axis=0)) / df2['DGS2']
        df2['10yr_Change'] = (df2['DGS10']-df2['DGS10'].shift(1,axis=0)) / df2['DGS10']
        df2['30yr_Change'] = (df2['DGS30']-df2['DGS30'].shift(1,axis=0)) / df2['DGS30']

        short_max = df2['DGS2'].idxmax()
        market_max = df['NASDAQCOM'].idxmax()

        fig,ax = plt.subplots(figsize=(20,8))
        
        ax.plot(df2['2yr_Change'], label='2yr Note Change', color='green', linestyle='--', alpha=0.5)
        ax.plot(df2['10yr_Change'], label='10yr Note Change', color='springgreen', linestyle='--', alpha=0.5)
        ax.plot(df2['30yr_Change'], label='30yr Bond Change', color='limegreen', linestyle='-', alpha=0.5)
        ax.axvline(short_max, linestyle='-.', color='green', alpha=0.5, label='Short Rate Peak')
        ax.legend(loc=2)
        ax.tick_params(rotation=50)
        ax.set_ylabel('U.S. T-Bond Changes', color='forestgreen', fontsize=12)

        ax2 = ax.twinx()
        ax2.plot(df['Equity_Change'], label='NASDAQ Composite Index Change', linewidth=3)
        ax2.plot(df['Income_Change'], label='Income Change', color='skyblue')
        ax2.plot(df['Credit_Change'], label='Change in Bad Credit', color='cornflowerblue')
        ax2.plot(df['GDP_Change'], label='GDP Change', color='orange', linewidth=3)
        ax2.axvline(market_max, color='blue', linestyle='-.', alpha=0.7, label='Market Peak')

        ax2.tick_params(rotation=50)
        ax2.set_ylabel('Asset Price Changes', color='mediumblue', fontsize=12)
        ax2.legend(loc=1)
        ax2.set_title('Impacts of Asset Price Changes', fontsize=20)
        


        


"""
CLEANUP
========
Debt Cycle as a Whole 
1. Start with '08 for each step -> FIX DATES
2. Grab a few other smaller recessions -> same analysis 
3. Resize each dataset to fit onto the same X-Axis
    - differences/similarities in the timelines? 

FILL_BETWEENX(Y, X,X....)
y = np.arange(min, max) -> basically parameters of the y axis 

01_early
- do whole cycle overall analysis 
- intro to debt cycle 
- add cycle lines
02_bubble
- shade out other parts of the cycle on graph so you can kinda see the whole thing
    - focus on the 'bubble' part 
- % change in numbers qoq not yoy -> too short a timespan 
- add yield curve
03_top 
- When/Where are LT rates not falling in tandem with ST rates = monetary policy flop 
- Asset Price Changes (market peak too far out from short rate peak) - range issue 
04_depression 
- End Date for Depression Cycle
- PUT CODE INTO .PY FILE
- NOMINAL SR
- HOUSEHOLD DEBT AS % OF NET WORTH
- US 3YR MONEY GROWTH
- US NET WEALTH SHARES 
05_beautiful_deleveraging
- 
- 
06_pushing_string_normalization
- 
- 

Make list_urls in range a completely separate function? 

Don't iterate through entire cycle to get cycle range boundaries 
- would pull so much small data it would get icky and messy and you don't want that boooo
- focus on individual cycles -> store them and identify full cycles later in a big graph 
- do this separate from each indiivdual analyzation 
"""


# stacked bar chart work 
# create new df with just positive and negative values to plot 
# US Debt to GDP via categories? 
    # https://matplotlib.org/stable/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html
    # change to dictionary -> dataframe data structure not working properly 
    # would need to sort positive vs. negative values in the DF to organize properly
        # then graph the positive values separate from the negative 
