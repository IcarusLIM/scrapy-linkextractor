from scrapy.utils.url import parse_url
from scrapy.utils.python import unique


def get_url_domain(url):
    return parse_url(url).netloc.lower()


def drop_anchor(urls):
    us = []
    for url in urls:
        i = url.find("#")
        us.append(url if i == -1 else url[:i])
    return unique(us)
