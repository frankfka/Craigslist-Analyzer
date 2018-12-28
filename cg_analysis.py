import pandas as pd
import numpy as np

def getAveragePrice(dataframe):
    priceArr = np.array(dataframe['price'].values)
    return np.mean(priceArr)
