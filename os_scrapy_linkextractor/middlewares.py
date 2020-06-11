# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from os_scrapy_linkextractor.lx_extensions import LxExtensionManager


class LinkExtractorDownloaderMiddleware:
    def _set_lxmanager(self, crawler):
        self.lx_manager = LxExtensionManager.from_crawler(crawler)

    def process_response(self, request, response, spider):
        response.request = request
        return self.lx_manager.process_response(response)

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        middleware._set_lxmanager(crawler)
        return middleware
