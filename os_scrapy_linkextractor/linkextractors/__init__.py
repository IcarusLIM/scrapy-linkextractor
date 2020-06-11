from scrapy.link import Link


def link_to_str(link):
    if isinstance(link, Link):
        return link.url
    return str(link)
