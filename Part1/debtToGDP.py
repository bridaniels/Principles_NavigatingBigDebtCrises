# US DEBT TO GDP

# import libraries 
import os
import csv

import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt 

# desired date range 
start = '1960-01-01'
end = '2021-10-01'

# import .csv data from FRED
files = os.listdir('data/FRED')
measurements = {}
for file in files: 
    if file.split('.')[1] == 'csv':
        name = file.split('.')[0]
        measurements[name] = pd.read_csv('data/FRED/'+file, index_col='DATE')
        measurements[name].index = pd.to_datetime(measurements[name].index)

def date_range(file_addy, start, end): 
    new_df = file_addy[start:end]
    new_df = new_df.astype(float, errors='raise')
    return new_df


class DEBT():
    def __init__(self, measurements, start='1960-01-01', end='2021-10-01'):
        self.start = start
        self.end = end
        self.measurements = measurements 
        
    def date_range(self,file_addy): 
        new_df = measurements[file_addy][self.start:self.end]
        new_df = new_df.astype(float, errors='raise')
        return new_df
        
    def total_us_debt(self): #if plotting=True
        tot_loans = self.date_range('ASTLL')
        tot_d_securities = self.date_range('ASTDSL')
        tot_debt = pd.concat([tot_loans,tot_d_securities], axis=1, join='outer')
        tot_debt['Total_Debt'] = tot_debt['ASTLL'] + tot_debt['ASTDSL']
        return tot_debt

    def usDebt_to_gdp(self):
        tot_loans = self.date_range('ASTLL')
        tot_d_securities = self.date_range('ASTDSL')
        gdp_ = self.date_range('GDP')
        tot_debt = pd.concat([tot_loans,tot_d_securities,gdp_], axis=1, join='outer')
        tot_debt['Total_Debt'] = tot_debt['ASTLL'] + tot_debt['ASTDSL']
        # GDP measured in Billions -> others measured in Millions 
        tot_debt['GDP'] = tot_debt['GDP'] * 1000
        tot_debt['Debt_as_%_GDP'] = tot_debt['Total_Debt'] / tot_debt['GDP']
        return tot_debt

    def yoy_debt_to_gdp_change(self): 
        og_debt_gdp = self.usDebt_to_gdp()
        og_debt_gdp['Change'] = og_debt_gdp['Debt_as_%_GDP'] - og_debt_gdp['Debt_as_%_GDP'].shift(-4,axis=0)
        return og_debt_gdp

    def total_household_nonprofit_debt(self): 
        onefour_mort = self.date_range('ASHMA') #millions Quarterly
        multi_mort = self.date_range('ASMRMA') #millions Quarterly
        auto_loan = self.date_range('MVLOAS')*1000 #billions Quarterly
        stu_loan = self.date_range('SLOAS')*1000 #billions Quarterly
        credit_card = self.date_range('REVOLSL')*1000 #billions MONTHLY
        tot_house_debt = pd.concat([onefour_mort, multi_mort, auto_loan, stu_loan, credit_card], 
                               axis=1, join='outer')
        tot_house_debt = tot_house_debt.fillna(0)
        tot_house_debt = tot_house_debt[tot_house_debt['ASHMA'] != 0]
        tot_house_debt['debt_sum'] = tot_house_debt.sum(axis=1)
        return tot_house_debt

    def total_gov_debt(self): 
        fed_securities = self.date_range('FGDSLAQ027S') #millions Quarterly
        state_local = self.date_range('SLGSDODNS')*1000 #billions Quarterly
        tot_gov_debt = pd.concat([fed_securities, state_local],
                                axis=1, join='outer')
        tot_gov_debt = tot_gov_debt.fillna(0)
        tot_gov_debt['debt_sum'] = tot_gov_debt.sum(axis=1)
        return tot_gov_debt

    def total_business_debt(self): 
        tot_commercial_mort = self.date_range('ASCMA') #millions Quarterly
        tot_farm_mort = self.date_range('ASFMA') #millions Quarterly
        tot_fin_biz_debt_secur = self.date_range('FBDSILQ027S') #millions Quarterly
        tot_fin_biz_loans_liab = self.date_range('FBLL') #millions Quarterly
        tot_nf_corp_debt_secur = self.date_range('NCBDBIQ027S') #millions Quarterly
        tot_nf_corp_loans = self.date_range('NCBLL') #millionsQuarterly
        tot_nf_ncorp_biz_loans = self.date_range('NNBLL') #millionsQuarterly
    
        tot_biz_debt = pd.concat([tot_commercial_mort, tot_farm_mort, tot_fin_biz_debt_secur,
                             tot_fin_biz_loans_liab, tot_nf_corp_debt_secur, tot_nf_corp_loans,
                             tot_nf_ncorp_biz_loans],
                             axis=1, join='outer')
        tot_biz_debt = tot_biz_debt.fillna(0)
        tot_biz_debt['debt_sum'] = tot_biz_debt.sum(axis=1)
        return tot_biz_debt

        
