import scrapy, json

from os_scrapy_linkextractor.items import ExampleItem


class SameDomainOnlySpider(scrapy.Spider):
    name = "drop-anchor"

    def start_requests(self):
        yield scrapy.Request(
            url="https://ghamster0.github.io/2019/09/20/Java%E6%BA%90%E7%A0%81%E4%B9%8B%E6%8E%92%E5%BA%8F%E7%AE%97%E6%B3%95/",
            # meta={"extractor.rules": [{"type": "re"}], "extractor.drop_anchor": True},
            meta={"extractor.rules": [{"type": "re"}]},
        )

    def parse(self, response):
        print(json.dumps(response.meta, indent=2))
        pass
