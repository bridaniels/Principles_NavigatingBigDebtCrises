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

def total_us_debt(start, end):
    tot_loans = date_range(measurements['ASTLL'], start, end)
    tot_d_securities = date_range(measurements['ASTDSL'], start, end)
    tot_debt = pd.concat([tot_loans,tot_debt], axis=1, join='outer')
    
