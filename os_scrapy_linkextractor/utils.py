from scrapy.utils.url import parse_url


def get_url_domain(url):
    return parse_url(url).netloc.lower()
