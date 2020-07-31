# -*- coding: utf-8 -*-
import scrapy

from os_scrapy_linkextractor.items import ExampleItem


class ExtractInExtensionSpider(scrapy.Spider):
    name = "extract-in-extension"

    def start_requests(self):
        yield scrapy.Request(
            url="http://www.example.com",
            meta={
                "depth": "5",
                "extractor.depth_limit":7,
                "extractor.rules": [
                    {"type": "re", "allow_domains": [], "deny_domains": []},
                    {
                        "type": "lxml",
                        "allow": [],
                        "deny": [],
                        "allow_domains": [],
                        "deny_domains": [],
                        "restrict_xpaths": [],
                        "tags": ["a", "area"],
                        "attrs": ["href"],
                        "restrict_css": [],
                    }
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