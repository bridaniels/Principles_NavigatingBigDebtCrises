# Bridgewater Daily Observations (BDO)
# News

import pandas as pd
import numpy as np 

from datetime import datetime, timedelta 

# https://datagy.io/pandas-add-row/
# https://towardsdatascience.com/how-to-access-relational-databases-in-python-f711cb38e235
# https://github.com/sukhbinder/timeline_in_python/blob/master/timeline_in_matplotlib.py
# https://dadoverflow.com/2021/08/17/making-timelines-with-python/




housing_crisis_timeline = pd.DataFrame.from_dict({ 
    'date': [
        '2004-01-22',
        '2004-09-26',
        '2004-10-20',
        '2005-04-28',
        '2005-05-10',
        '2005-05-25',
        '2005-05-31',
        '2005-07-09',
        '2005-08-17',
        '2005-08-28',
        '2005-10-04',
        '2006-01-08',
        '2006-08-23',
        '2006-08-24',
        '2006-09-14',
        '2006-10-27',
        '2006-11-07',
        '2006-12-06',
        '2007-01-26',
        '2007-02-08',
        '2007-03-10'
        
        ],
    'event': [ 
        'Increased Home Building Driving Economy', 
        'Flipping Houses Hits Reality TV',
        'Alan Greenspan claims growing mortgage debt is not a big burden',
        'Mortgage applications up due to decline in borrowing costs (purchase or refinance)',
        'U.S. Housing Bubble Appears',
        'Steep Price Rises in Homes',
        'Fed Debates Pricking US Housing Bubble (asset prices out of Fed jurisdiction)',
        'Real estate bringing in over 700,000 new jobs over past four years',
        'Healthy Housing Market Lifted the Economy in July (prev. month)',
        'Alan Greenspan predicts that the housing boom and consumer spending spree is near an end',
        'Hot housing markets beginning to see a slowdown',
        'Real estate investors warned that they would not expect repeated gains in 2005. Those who stayed course saw continued profits in the RE sector.',
        'Housing market showing signs of potentially dragging down the economy.',
        'Pre-owned home sales at their lowest level July 2006. Prices flattened and homes staying on the market longer.',
        'Prime Adjustable-Rate Mortgages Foreclosing: Homeowners with good credit unable to pay their bills.',
        'Housing Market Weakening: Offering Price Cuts + Discounts',
        'Number of unsold homes increasing and builders beginning to pull out',
        'Home price statistics misleading due to only factoring in homes actually sold',
        '2006 home sales with the biggest drop in past 17 years',
        'HSBC reports ~20% more than anticipated charge for bad debts in 2006 due to problems in mortgage portfolio.',
        'Mortgage lenders credit lines being cut off due to high default rates on mortgages written in 2006 (more relaxed standards).'




        ],
})


federal_reserve_timeline = pd.DataFrame.from_dict({
    'date':[
        '2004-04-22',
        '2004-10-20',
        '2004-11-06',
        '2005-05-31',
        '2005-08-28',
        '2006-02-01',
        '2006-04-19',
        '2006-07-10'
        
        
        ],
    'event': [
        'Alan Greenspan claims deflation threat is gone. Hints rising productivity will keep interest rates lower, longer.',
        'Alan Greenspan claims growing mortgage debt is not a big burden.',
        'When is accumulated debt unsustainable? Time to raise interest rates from rock bottom.',
        'Fed contemplating pricking US Housing Bubble (asset prices out of jurisdiction)',
        'Greenspan predicts that the housing boom and consumer spending spree is near an end',
        'Greenspan steps down after 18 years of service as Federal Reserve Chairman. Replaced by Ben Bernanke.',
        'Fed signals policy shift on interest rates. Might stop campaign to raise IR next month (ST IR moved up 15x in the past 2 years)',
        'Former Goldman Sachs Exec. Henry M. Paulson sworn in as Treasury Secretary.'

        ]

})


general_financial_news_timeline = pd.DataFrame.from_dict({
    'date': [
        '2005-12-17',
        '2006-02-10',
        '2006-07-10',
        '2006-10-24',
        '2007-01-10',
        '2007-02-02',
        '2007-02-05',
        '2007-02-08',
        '2007-02-07',
        '2007-03-06',
        '2007-03-10'

    ],
    'event': [
        'Citigroup expanding existing retail business across the US',
        'US Trade Deficit Record High in 2005. Up nearly 18% with a $725.8 billion gap (twice the 2001 deficit). Last surplus in 1975.',
        'Former Goldman Sachs Exec. Henry M. Paulson sworn in as Treasury Secretary.',
        'President Bush campaigning on theme of a good economy that was born out of his tax relief',
        '2006 ends with a strong job market, retail sales in good standing and highest consumer sentiment in 3 years.',
        'Job growth still strong but slowing entering 2007.',
        'Highly liquid markets are raising prices of risky assets, while lowering expected returns. Assumptions of stable volatility increasing use of leverage to increase returns.', 
        'HSBC reports ~20% more than anticipated charge for bad debts in 2006 due to problems in mortgage portfolio.',
        'China Black Tuesday: markets sell off and drop ~9% due to government plans to either raise interest rates or implement a capital gains tax.',
        '5-day Asian market slide ends as investors take advantage of low prices.',
        'Mortgage lenders credit lines being cut off due to high default rates on mortgages written in 2006 (more relaxed standards).'

    ]

})
