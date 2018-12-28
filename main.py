import cg_page_crawler as crawler
import cg_analysis as analyzer

main_link = "https://vancouver.craigslist.org/search/sss?query=macbook+pro+13&sort=rel&min_price=900&max_price=1300"
print(analyzer.getAveragePrice(crawler.getDataForQuery(main_link)))