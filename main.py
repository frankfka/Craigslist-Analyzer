import cg_page_crawler as crawler
import cg_analysis as analyzer
import numpy as np 
import pandas as pd
import datetime
import time
import cg_email_notification as email

# TODO parse from a csv
# TODO parse the parameters and sort by date?
links_to_follow = ["https://vancouver.craigslist.org/search/sss?sort=date&max_price=1000&min_price=300&query=iphone%20x", "https://vancouver.craigslist.org/search/sss?query=lg+g7&sort=date&min_price=300&max_price=600", "https://vancouver.craigslist.org/search/sss?query=galaxy+s9&sort=date&min_price=200&max_price=600", "https://vancouver.craigslist.org/search/sss?query=pixel+2+xl&sort=date&min_price=200&max_price=500", "https://vancouver.craigslist.org/search/sss?query=ipad+pro&sort=date&min_price=300&max_price=550", "https://vancouver.craigslist.org/search/sss?query=airpods&sort=date&min_price=150&max_price=200"]
num_links = len(links_to_follow)

# Cached data
cachedAnalysisDict = {"source_link": links_to_follow, "average_price": np.zeros(num_links), "min_price": np.zeros(num_links), "time_checked": [datetime.datetime.now()]*num_links} 
cachedRawDataDict = {}
analysisCache = pd.DataFrame(cachedAnalysisDict).set_index('source_link')

# Initialize cache
for link in links_to_follow:
    cachedRawDataDict[link] = None

while(True):

    # Useful stuff to email
    relevant_postings = []

    print("\n\n/////////////////////////////////////////////////////")
    print("Crawling Craigslist. Current time:")
    print(datetime.datetime.now())

    # Iterate through links to search
    for link in links_to_follow:

        # Retrieve newest data and cached data
        new_dataframe = crawler.getDataForQuery(link)
        old_dataframe = cachedRawDataDict[link]

        # Don't do anything if current retrieval failed
        if new_dataframe is not None:

            # Compare if there is a cache
            if old_dataframe is not None:

                # Find which listings are newly posted
                new_listings = analyzer.getNewPostings(old_dataframe, new_dataframe)

                # Find cached analysis values
                cached_avg_price = float(analysisCache.loc[link, 'average_price'])
                cached_min_price = float(analysisCache.loc[link, 'min_price'])

                for index, row in new_listings.iterrows():
                    print('************** \nNEW LISTING: ' + str(index))

                    if row['price'] < cached_avg_price:
                        print("Lower than average price")
                    if row['price'] < cached_min_price:
                        print("Lower than minimum price")
                        
                        # Add these to email list
                        relevant_postings.append(index)

            # Update old values
            avg_price = analyzer.getAveragePrice(new_dataframe)
            min_price = analyzer.getMinPrice(new_dataframe)
            cachedRawDataDict[link] = new_dataframe
            analysisCache.loc[[link], ['min_price']] = min_price
            analysisCache.loc[[link], ['average_price']] = avg_price
            analysisCache.loc[[link], ['time_checked']] = datetime.datetime.now()

    # Send off the email
    email_string = ""
    for posting in relevant_postings:
        email_string = email_string + str(posting) + "\n"
    if email_string:
        email.send_gmail(email_string)

    # Sleep for a bit!
    time.sleep(600)

    # TODO save current data to a csv