import cg_page_crawler as crawler
import cg_analysis as analyzer
import numpy as np 
import pandas as pd
import datetime
import time

# TODO parse from a csv
# TODO parse the parameters and sort by date?
links_to_follow = ["https://vancouver.craigslist.org/search/sss?query=macbook+pro+13&sort=rel&min_price=900&max_price=1300"]
num_links = len(links_to_follow)

# Cached data
cachedAnalysisDict = {"source_link": links_to_follow, "average_price": np.zeros(num_links), "min_price": np.zeros(num_links), "time_checked": [datetime.datetime.now()]*num_links} 
cachedRawDataDict = {}
analysisCache = pd.DataFrame(cachedAnalysisDict).set_index('source_link')

while(True):

    # Useful stuff to email
    relevantPostingsDict = {}
    print("Looping Again. Current time:")
    print(datetime.datetime.now)

    for link in links_to_follow:
        new_dataframe = crawler.getDataForQuery(link)
        old_dataframe = cachedRawDataDict[link]

        # Don't do anything if current retrieval failed
        if new_dataframe is not None:
            print('New Dataframe is not None')

            # Compare if there is a cache
            if old_dataframe is not None:
                print('Old Dataframe is not None')
                new_listings = analyzer.getNewPostings(old_dataframe, new_dataframe)
                cached_avg_price = analysisCache.loc[link, 'average_price']
                print(new_listings)
                print(new_listings.loc[new_listings['price'] < float(cached_avg_price)])

            # Update old values
            avg_price = analyzer.getAveragePrice(new_dataframe)
            min_price = analyzer.getMinPrice(new_dataframe)
            cachedRawDataDict[link] = new_dataframe
            analysisCache.loc[[link], ['min_price']] = min_price
            analysisCache.loc[[link], ['average_price']] = avg_price
            print('Analysis Cache')
            print(analysisCache)

    # Sleep for a bit!
    time.sleep(120)

    # TODO email link if new posting comes up with price lower than min price

    # TODO save current data to a csv