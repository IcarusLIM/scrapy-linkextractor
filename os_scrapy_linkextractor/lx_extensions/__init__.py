import logging
from inspect import isawaitable

from scrapy.utils.misc import load_object

from os_scrapy_linkextractor.linkextractors import link_to_str

logger = logging.getLogger(__name__)

DEPTH_LIMIT_KEY = "extractor.depth_limit"


class LxExtensionManager:
    def __init__(self, lx_extensions=[], depth_limit=None):
        self.lx_extensions = lx_extensions
        self.depth_limit = depth_limit

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        lx_extensions_cls = [load_object(p) for p in settings.getlist("LX_EXTENSIONS")]
        lx_extensions = []
        for c in lx_extensions_cls:
            if not issubclass(c, LinkExtractorExtension):
                logger.warning(f"Invalid link extractor extension type {str(c)}")
                continue
            lx_extensions.append(c.from_crawler(crawler))
        depth_limit = crawler.settings.get("DEPTH_LIMIT")
        depth_limit = int(depth_limit) if depth_limit else None
        return cls(lx_extensions=lx_extensions, depth_limit=depth_limit)

    def add_extension(self, lx_extension):
        if not isinstance(lx_extension, LinkExtractorExtension):
            logger.warning(
                f"Invalid link extractor extension type {type(lx_extension)}"
            )
            return
        self.lx_extensions.append(lx_extension)

    def extract_links(self, response):
        rules = response.request.meta.get("extractor.rules", None)
        if rules is None or not isinstance(rules, list):
            return {}
        meta = response.request.meta
        depth = int(meta["depth"]) if "depth" in meta else None
        req_depth_limit = (
            int(meta[DEPTH_LIMIT_KEY]) if DEPTH_LIMIT_KEY in meta else None
        )
        max_depth = self._get_max_depth(req_depth_limit)
        if max_depth and depth and depth >= max_depth:
            return {}
        link_dict = {}
        for lx_extension in self.lx_extensions:
            links = lx_extension.extract_links(response, rules)
            if len(links) == 0:
                continue
            links = [link_to_str(l) for l in links]
            name = lx_extension.name if hasattr(lx_extension, "name") else "default"
            if name not in link_dict:
                link_dict[name] = links
            else:
                link_dict[name].extend(links)
        return link_dict

    # Set extracted links into response.meta["extracted_links"]
    def process_response(self, response):
        link_dict = self.extract_links(response)
        if len(link_dict) > 0:
            assert "extractor.links" not in response.meta
            response.meta["extractor.links"] = link_dict
        return response

    def _get_max_depth(self, req_depth_limit):
        if self.depth_limit is None:
            return req_depth_limit
        if req_depth_limit is None:
            return self.depth_limit
        return min(self.depth_limit, req_depth_limit)


class LinkExtractorExtension:
    def __init__(self, lx_cls):
        self.lx_cls = lx_cls

    def _match_rule(self, rule):
        raise NotImplementedError("")

    def _new_linkextractor(self, rule):
        raise NotImplementedError("")

    def validate_rule(self, rule):
        return isinstance(rule, dict) and rule.get("type", None) is not None

    def extract_links(self, response, rules):
        link_extractors = [
            self._new_linkextractor(rule)
            for rule in rules
            if self.validate_rule(rule) and self._match_rule(rule)
        ]
        links = []
        for lx in link_extractors:
            _links = lx.extract_links(response)
            links.extend(_links)
        return links
