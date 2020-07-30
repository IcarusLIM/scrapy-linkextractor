import logging
from os_scrapy_linkextractor.lx_extensions import LxExtensionManager
from typing import Type

from scrapy.crawler import Crawler
from scrapy import signals
from scrapy.utils.response import get_base_url
from scrapy.spiders import Spider
from scrapy.http.response.html import HtmlResponse
from scrapy.http.request import Request

class LinkExtractorExtension:
    def __init__(self, crawler: Type[Crawler]):
        self.lx_manager=LxExtensionManager.from_crawler(crawler)
        crawler.signals.connect(
            self._response_received, signal=signals.response_received
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _response_received(self, request: Type[Request], response: Type[HtmlResponse], spider):
        response.request = request
        self.lx_manager.process_response(response)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)