import feedparser

main_link = "https://vancouver.craigslist.org/search/sss?query=macbook+pro+13&sort=rel&min_price=900&max_price=1300"

def getRssLink(query_link):
    return query_link.replace("/sss?", "/sss?format=rss&")

NewsFeed = feedparser.parse(getRssLink(main_link))
entry = NewsFeed.entries[1]

print(len(NewsFeed.entries))