import pandas as pd
import sys
import numpy as np

def getAveragePrice(dataframe):
    priceArr = np.array(dataframe.loc[:,'price'].values)
    return np.mean(priceArr)

def getMinPrice(dataframe):
    minPrice = sys.maxsize
    for index, row in dataframe.iterrows():
        if row['price'] < minPrice:
            minPrice = row['price']
    return minPrice

# Return a dataframe of new posts
def getNewPostings(old_dataframe, new_dataframe, last_checked):
        new_postings = pd.DataFrame({'title': [], 'link': [], 'price': [], 'has_image': [], 'time_posted': []}).set_index('link')
        existing_listings = old_dataframe.index
        for index, row in new_dataframe.iterrows():
                if not (index in existing_listings):
                    if row['time_posted'] > last_checked:
                        new_postings = new_postings.append(row)
        return new_postings
