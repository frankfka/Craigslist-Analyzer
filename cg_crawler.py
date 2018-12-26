import pandas as pd
from bs4 import BeautifulSoup as bs4
import requests
import datetime

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

def makeRequest(link):
    return requests.get(link, headers=header)

main_link = "https://vancouver.craigslist.org/search/sss?query=macbook+pro+13&sort=rel&min_price=900&max_price=1300"

# Make request and parse with bs4
rsp = makeRequest(main_link)
html = bs4(rsp.text, 'html.parser')

# Each post is an 'li' with class 'result-row'
posts = html.find_all('li', attrs={'class': 'result-row'})

# Define a test post and get several important parameters
test_post = posts[0]
price = float(str(test_post.find('span', attrs={'class': 'result-price'}).text).replace("$", ""))
title = str(test_post.find('a', attr={'class': 'result-title'}))
# Does not work for all cases
# location_string = str(test_post.find('span', attr={'class': 'nearby'})['title'])
time_posted = datetime.datetime.strptime(test_post.find('time')['datetime'], "%Y-%m-%d %H:%M")
print(price)
print(title)
print(time_posted)
print(html.find('li', attrs={'data-pid':'6753890879'}))
#TODO: hasImage

#### NOTE: this will return an RSS link within - can call that module here
