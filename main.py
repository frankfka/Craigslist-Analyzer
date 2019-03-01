import cg_page_crawler as crawler
import cg_analysis as analyzer
import numpy as np 
import pandas as pd
import datetime
import time
import re
import cg_email_notification as email

links_to_follow = []
with open('links_to_track.csv','r') as csv:
    links_to_follow = csv.readlines()
links_to_follow = [link.strip() for link in links_to_follow]
num_links = len(links_to_follow)

# Cached data
cachedAnalysisDict = {"source_link": links_to_follow, "average_price": np.zeros(num_links), "min_price": np.zeros(num_links), "time_checked": [datetime.datetime.now()]*num_links} 
cachedRawDataDict = {}
analysisCache = pd.DataFrame(cachedAnalysisDict).set_index('source_link')

# Helper function to get the file name
def getFileName(link):
    return 'data/' + re.sub(r'\W+', '', link[link.find('.org') + 4:]) + '.csv'

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

        print("****\nAnalyzing: " + link)

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

                print('Cached Avg Price: ' + str(cached_avg_price))
                print('Cached Min Price: ' + str(cached_min_price))

                # Get historical data from csv
                historical_data = pd.read_csv(getFileName(link), index_col=0)

                for index, row in new_listings.iterrows():
                    print('**\nNEW LISTING: ' + str(index))
                    historical_data = historical_data.append(row)

                    # Only keep listings that are 90% of the avg cached price
                    if row['price'] < cached_avg_price * 0.9:
                        print("Lower than 0.9 of average price")
                        
                        # Add these to email list
                        relevant_postings.append(index)
                        
                    if row['price'] < cached_min_price:
                        print("Lower than minimum price")
                        
                
                # Save historical data with the new postings
                historical_data.to_csv(getFileName(link))

            else:
                # No cache, so need to save a new file
                # Simplest file name is to just take the alphanumeric characters from the link following the .org
                new_dataframe.to_csv(getFileName(link))

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


