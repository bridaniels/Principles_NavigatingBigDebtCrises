# Bridgewater Daily Observations (BDO)
# News

import pandas as pd
import numpy as np 

from datetime import datetime, timedelta 

# https://datagy.io/pandas-add-row/
# https://towardsdatascience.com/how-to-access-relational-databases-in-python-f711cb38e235


housing_crisis_timeline = pd.DataFrame.from_dict({ 
    'date': [
        '2004-01-22',
        '2004-09-26',
        '2004-10-20',
        '2005-04-28',
        '2005-05-10',
        '2005-05-25'
        
        ],
    'event': [ 
        'Increased Home Building Driving Economy', 
        'Flipping Houses Hits Reality TV',
        'Alan Greenspan claims growing mortgage debt is not a big burden',
        'Mortgage applications up due to decline in borrowing costs (purchase or refinance)',
        'U.S. Housing Bubble Appears',
        'Steep Price Rises in Homes'

        ],
})


federal_reserve_timeline = pd.DataFrame.from_dict({
    'date':[
        '2004-04-22',
        '10-2004',
        '11-2004'
        
        ],
    'event': [
        'Alan Greenspan claims deflation threat is gone. Hints rising productivity will keep interest rates lower, longer.'
        'Alan Greenspan claims growing mortgage debt is not a big burden.',
        'When is accumulated debt unsustainable? Time to raise interest rates from rock bottom.'

        ]

})

