import scrapy

from os_scrapy_linkextractor.items import ExampleItem


class SameDomainOnlySpider(scrapy.Spider):
    name = "same-domain-only"

    def start_requests(self):
        yield scrapy.Request(
            url="http://www.example.com",
            meta={
                "extractor.rules": [
                    {
                        "type": "re",
                        "same_domain_only": True,
                        "allow_domains": [],
                        "deny_domains": [],
                    },
                ]
            },
        )

    def parse(self, response):
        return ExampleItem(
            url=response.url,
            request_headers=response.request.headers,
            response_headers=response.headers,
            status=response.status,
            meta=response.meta,
            body=response.body,
        )
