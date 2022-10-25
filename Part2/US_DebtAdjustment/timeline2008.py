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
        '2007-01-04',
        '2007-01-26',
        '2007-02-08',
        '2007-03-10',
        '2007-03-23',
        '2007-05-17',
        '2007-05-25',
        '2007-06-15',
        '2007-07-13',
        '2007-07-16',
        '2007-08-07',
        '2007-08-09',
        '2007-08-11',
        '2007-08-31',
        '2007-09-07',
        '2007-09-20',
        '2007-09-28',
        '2007-10-10',
        '2007-10-25',
        '2007-10-27',
        '2007-11-02',
        '2007-11-24'
        
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
        'SEC memo: With refinancing and real estate booms over, smaller subprime originators business models no longer viable'
        '2006 home sales with the biggest drop in past 17 years',
        'HSBC reports ~20% more than anticipated charge for bad debts in 2006 due to problems in mortgage portfolio.',
        'Mortgage lenders credit lines being cut off due to high default rates on mortgages written in 2006 (more relaxed standards).',
        'Existing-home sales rise most in 3 years.',
        'Mixed reading on the housing sector glossed over in lieu of growth in industrial output.',
        'Home sales surged in April by largest jump in 14 years.',
        'Subprime mortgage delinquencies growing. Fed holds a hearing to assess abusive lending practices.',
        'Fitch may downgrade bonds tied to subprime mortgages.',
        'ABX Index Crash: (sub-indexed into *tranches* grouped by credit rating) Higher Rated Subprime Mortgage-Backed Securities(RMBS) Fell. Spreads Growing.',
        'American Home Mortgage files for chapter 11 bankruptcy protection.',
        'Gov. might raise limit on purchases of home loans by Fannie Mae and Fredie Mac to increase liquidity in mortgage market.',
        'Europeans worried about subprime exposure.',
        'Countrywide Financial: (largest mortgage lender in the US) at risk of bankruptcy. Tapped into $11.5b credit line to boost cash on hand.',
        'Bush offers relief to some on home loans, by changing the federal mortgage insurance program.',
        'American household sector with bad balance sheet and poor cash flows. Injecting more capital will only worsen issues.',
        'Fed calls for tighter mortgage regulations.',
        'Home Sales + Prices FALL',
        'Fannie and Freddie with new fund for affordable rental housing in a market with unaffordable subprime mortgages and falling home prices.',
        'Home sales slump at 8-yr low.',
        'Homeownership Declines for Four Consecutive Quarter.',
        'New York Appraiser Inflated Value of Homes',
        'Housing History suggestions a recession to follow. Fed forecasts no forseeable recession (unemployment barely rising).'



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
        '2006-07-10',
        '2007-03-22',
        '2007-03-28',
        '2007-05-25',
        '2007-06-15',
        '2007-08-07',
        '2007-08-10',
        '2007-08-11',
        '2007-08-18',
        '2007-08-22',
        '2007-09-18',
        '2007-09-22',
        '2007-10-18'
        
        ],
    'event': [
        'Alan Greenspan claims deflation threat is gone. Hints rising productivity will keep interest rates lower, longer.',
        'Alan Greenspan claims growing mortgage debt is not a big burden.',
        'When is accumulated debt unsustainable? Time to raise interest rates from rock bottom.',
        'Fed contemplating pricking US Housing Bubble (asset prices out of jurisdiction)',
        'Greenspan predicts that the housing boom and consumer spending spree is near an end',
        'Greenspan steps down after 18 years of service as Federal Reserve Chairman. Replaced by Ben Bernanke.',
        'Fed signals policy shift on interest rates. Might stop campaign to raise IR next month (ST IR moved up 15x in the past 2 years)',
        'Former Goldman Sachs Exec. Henry M. Paulson sworn in as Treasury Secretary.',
        'Fed stops tightening leaving rates unchanged at 5.25% and markets soar (DJIA best 3 day performance since 2004).',
        'Chairman Bernanke in Congressional Testimony claiming no concerns for systemic risk from subprime market.',
        'Largest jump in home sales over past 14 years dampens hopes of monetary policy easing.',
        'Federal Reserve holds a hearing to address abusive lending practices with subprime mortgages.',
        'Fed leaves interest rate unchanged at 5.25% (no signs of future cut).',
        'Fed announces willingness to inject reserves and act as lender of last resort to keep financial markets churning.',
        'Worldwide central banks injecting liquidity into the market to help keep financial markets afloat.',
        'Fed cuts bank loan discount rate half a percent. Acknowledge that tight credit and uncertainty are hurting the overall market.',
        'Top banks draw on Fed discount-lending rate amid credit market turmoil (taking loans directly from the Fed)',
        'Fed cuts rates by 0.5% when market was expecting 0.25%. Market Rally.',
        'Fed Govenor Warns Against Shielding Investors from Their Losses.',
        'Fed puzzled by steady core inflation despite state of economy and financial markets.'

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
        '2007-03-10',
        '2007-03-22',
        '2007-03-22',
        '2007-04-02',
        '2007-04-17',
        '2007-04-22',
        '2007-04-26', 
        '2007-05-17',
        '2007-05-02',
        '2007-06-05',
        '2007-06-08',
        '2007-06-08',
        '2007-06-21',
        '2007-07-03',
        '2007-07-13',
        '2007-07-14',
        '2007-07-14',
        '2007-07-26',
        '2007-08-01',
        '2007-08-03',
        '2007-08-09',
        '2007-08-10',
        '2007-08-16',
        '2007-08-22',
        '2007-08-22', 
        '2007-08-31',
        '2007-09-01',
        '2007-09-06',
        '2007-09-07',
        '2007-09-07',
        '2007-09-08',
        '2007-09-14',
        '2007-09-14',
        '2007-09-19',
        '2007-09-21',
        '2007-09-27',
        '2007-10-02',
        '2007-10-06',
        '2007-10-09',
        '2007-10-19',
        '2007-10-22',
        '2007-10-24',
        '2007-10-30',
        '2007-11-03',
        '2007-11-03',
        '2007-11-06',
        '2007-11-08',
        '2007-11-10',
        '2007-11-20'


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
        'Mortgage lenders credit lines being cut off due to high default rates on mortgages written in 2006 (more relaxed standards).',
        'DJIA up 337 points with best 3 days since 2004.',
        'Chinese stock market back up and running.',
        'New Century Files for Bankruptcy',
        'Strong earnings reports show a healthy increase in consumer spending.',
        'Dow with three record highs in five days',
        'Durable goods strong.',
        'Mixed reading on the housing sector glossed over in lieu of growth in industrial output.',
        'Economic data renews confidence in the economy and hit record closes across major indexes.',
        'Slight gains cause Chinese market slide to be shrugged off.',
        '10-yr Treasury rates rise above 5% for the first time since previous summer.',
        'Share prices with steepest 3-day decline since February.',
        'Bear Stearns saves 2 hedge funds from collapse and baisl out another troubled fund.',
        'Pickup in implied volatility (from very low levels). Overall market volatility expected to stay low.',
        'Fitch may downgrade bonds tied to subprime mortgages.',
        'Dow and S&P 500 setting record highs. Dow swung 450+ points and rose 283 points in one day.',
        'Investors uneasy about subprime loans and impact on the broader economy.',
        'Markets fall as housing market concerns grow and oil prices near record levels.',
        'Slow growth in consumer spending, but with inflation moderated it appears consumer mood has increased.',
        'Credit fears cause stocks to fall.',
        'BNP Paribas (France): froze 2.2b USD citing problems in US subprime mortgage market causing evaporating liquidity which makes it impossible to value various assets regardless of credit ratings.',
        'BNP Paribas reaction to US mortgage market causes stocks to fall.',
        'Largest mortgage lender in the US (Countrywide Capital) draws on credit line for cash and is at risk of bankruptcy -> market reacts negatively.',
        'Bank of America takes Countrywide Financial stake.',
        'Top banks draw on Fed discount-lending rate amid credit market turmoil (taking loans directly from the Fed).',
        'President Bush to change federal mortgage lending insurance program to help lower payment requirements, increase loan limits, and offer flexible pricing.',
        'Reasurring words from president and the fed. chairman that Wall Street will not be left to handle alone cause big market gains.',
        'Fed says credit crisis is contained and stocks fall.',
        'Home foreclosure rate hits a record.', 
        'Abnormal Credit Crisis: *credit* continues to flow and *debt* continues to increase. American household secotor with bad balance sheets and poor cash flows (allowing more credit will only worsen the issues).',
        'Stocks fall due to poor job report showing increased unemployment (fear of recession looming).',
        'Credit Fears Ease, Markets Climb',
        'Bank of England to provide a *liquidity support facility* to native european mortgage lender. Signifying broadening effects of US bred crisis.',
        'Global markets rise after rate cut of 0.5% rather than 0.25%',
        'Summer credit storm shows up on Wall Street reports. Goldman Sachs up, while Bear Stearns down.',
        'Economic Indicators Drop Most in 6 Months as Confidence Ebbs',
        'SEC opens investigation into credit rating agencies potential inflation of MBS due to conflict of interest.',
        'Blue-Chip stocks into record territory. Banks predicted third quarter declines and eased anxiety arounding LT fallout from MBS.',
        'Big Loss at Merrill Stirs Unease',
        'S&P 500 closes at all-time high. High not reached again until 2013. JPM reports $2billion write-down.',
        'Earnings Reports Trigger Steep Stock Sell-Offs.',
        'Bear Stearns 3Q07 Earnings Down 61%. China Bank buys $1 billion stake.',
        'Merrill Lynch 3Q07 with first quarterly loss in 6 years. Tied to subprime mortgage market and writing down value of debt obligations.',
        'UBS with larger than expected loss.',
        'Citigroup Chief set to exit amid losses.',
        'Merrill Lynch still operating with interim CEO. Shares fall as speculation about future write-downs of high risk credit exposure.',
        'Bond buyers loosing confidence as write-down pace accelerates with credit downgrades in mortgages. Concerned about spillage into other markets.',
        'Morgan Stanley takes hit on Morgages',
        'Wachovia, Bank of America, and JPMorgan Chase warn about continuous losses in credit market. Barclays of London denies asset write-down.',
        'Credit concerns further drive down stock market.'


    ]

})


bank_bankruptcy_timeline = pd.DataFrame.from_dict({
    'date': [
        '2007-04-02',
        '2007-08-07'
    ],
    'business': [
        'New Century Financial Corp.',
        'American Home Mortgage'

    ],
    'what happened':[ 
        'largest independent U.S. subprime mortgage provider',
        '10th lartest retail mortgage lender. Filed for bankruptcy and liquidated.'
    ]
})


us_europe_crisis = pd.DataFrame.from_dict({
    'dates': [ 
        '2007-10-25',
        '2007-11-10'

    ],
    'events': [ 
        'Reduced growth forecast in Germany + Report by Bank of England that EU still vulnerable to US instability.',
        'Barclays of London denies speculation of large asset write-down.'

    ]
})

# References: 
# New Century: https://www.reuters.com/article/us-newcentury-bankruptcy-idUSN0242080520070403
