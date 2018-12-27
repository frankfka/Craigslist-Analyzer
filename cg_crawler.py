import pandas as pd
from bs4 import BeautifulSoup as bs4
import requests
import datetime
from random import randint
import time

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

def makeRequest(link):
    return requests.get(link, headers=header)

def getPostInformation(post_html):
    price = float(str(post_html.find('span', attrs={'class': 'result-price'}).text).replace("$", ""))
    title = str(post_html.find('a', attrs={'class': 'result-title'}).text)
    has_image = post_html.find('a', attrs={'class': 'empty'}) is None
    time_posted = datetime.datetime.strptime(post_html.find('time')['datetime'], "%Y-%m-%d %H:%M")
    return {'title': title, 'price': price, 'has_image': has_image, 'time_posted': time_posted}

def parseAllPostsForQueryLink(page_link):
    # Make request and parse with bs4
    #### NOTE: this will return an RSS link within - can call that module here
    rsp = makeRequest(page_link)
    html = bs4(rsp.text, 'html.parser')
    # Each post is an 'li' with class 'result-row'
    posts = html.find_all('li', attrs={'class': 'result-row'})
    parsedInfoList = []
    for post in posts:
        parsedInfoList.append(getPostInformation(post))

    next_page = str(html.find('a', attrs={'class': 'next'})['href'])
    if next_page:
        # Wait a bit before next pull
        time.sleep(randint(1,3))
        next_page_link = page_link[:page_link.find('.org') + 4] + next_page
        return parsedInfoList + parseAllPostsForQueryLink(next_page_link)
    else:
        return parsedInfoList

def getDataForQuery(query_link):
    return pd.DataFrame(parseAllPostsForQueryLink(query_link))

main_link = "https://vancouver.craigslist.org/search/sss?query=macbook+pro+13&sort=rel&min_price=900&max_price=1300"
getDataForQuery(main_link).to_csv('test.csv', index=False)



