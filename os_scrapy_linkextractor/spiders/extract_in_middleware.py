# -*- coding: utf-8 -*-
import scrapy

from os_scrapy_linkextractor.items import ExampleItem


class ExtractInMiddlewareSpider(scrapy.Spider):
    name = "extract-in-middleware"

    def start_requests(self):
        yield scrapy.Request(
            url="http://www.example.com",
            meta={
                "_link_rules_": [
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
