import cg_page_crawler as crawler
import cg_analysis as analyzer
import numpy as np 
import pandas as pd
import datetime

# TODO parse from a csv
# TODO parse the parameters and sort by date?
links_to_follow = ["https://vancouver.craigslist.org/search/sss?query=macbook+pro+13&sort=rel&min_price=900&max_price=1300"]
num_links = len(links_to_follow)
cachedAnalysisDict = {"source_link": links_to_follow, "average_price": np.zeros(num_links), "min_price": np.zeros(num_links), "time_checked": [datetime.datetime.now()]*num_links} 
cachedRawDataDict = {}
analysisCache = pd.DataFrame(cachedAnalysisDict).set_index('source_link')

# Initialize cache
for link in links_to_follow:
    dataframe = crawler.getDataForQuery(link)
    avg_price = analyzer.getAveragePrice(dataframe)
    min_price = analyzer.getMinPrice(dataframe)
    cachedRawDataDict[link] = dataframe
    analysisCache.loc[[link], ['min_price']] = min_price
    analysisCache.loc[[link], ['average_price']] = avg_price

# print(cachedRawDataDict)
# print(analysisCache)

# dataframe = crawler.getDataForQuery(main_link)
# print(analyzer.getMinPrice(dataframe))

# TODO email link if new posting comes up with price lower than min price

# TODO save current data to a csv