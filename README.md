# Craigslist Crawler/Analyzer 
Tools for keeping track of your craigslist searches. Get notified of the best deals before anyone else sees it! 

### Current Functionality
Once run, the script will:
* Query each search in "links_to_follow" every 600 seconds (adjust this by adjusting the parameter in time.sleep())
* Print to console when new listings have been found
* Print to console when new listings are below the historical average price
* Send an email notification with the link if the postings is below the historical average price
* Will keep historical data in a CSV, but does nothing with this yet

### Usage
* Clone or download the repo
* Fill in your information in email.csv for email notifications. NOTE: you will need a Gmail account and an [app password](https://support.google.com/accounts/answer/185833?hl=en) (you can't use your regular password)
* Run main.py with Python3 - I have the script looping forever on my Raspberry Pi so that it is always querying
* Customize to your liking! 

### Cool Features to Build
Stuff I might build in the future:
* Data analysis on historical price data
* Crawling each individual CG posting - though there is increased risk of being IP banned
* Using CG's RSS feed
* Front end framework with Flask to make customization easier
