import logging
from inspect import isawaitable

from scrapy.utils.misc import load_object

from os_scrapy_linkextractor.linkextractors import link_to_str
from os_scrapy_linkextractor.utils import as_deferred

logger = logging.getLogger(__name__)


class LxExtensionManager:
    def __init__(self, lx_extensions=[]):
        self.lx_extensions = lx_extensions

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
        return cls(lx_extensions)

    def add_extension(self, lx_extension):
        if not isinstance(lx_extension, LinkExtractorExtension):
            logger.warning(
                f"Invalid link extractor extension type {type(lx_extension)}"
            )
            return
        self.lx_extensions.append(lx_extension)

    async def extract_links(self, response):
        rules = response.request.meta.get("_link_rules_", None)
        if rules is None or not isinstance(rules, list):
            return []
        link_dict = {}
        for lx_extension in self.lx_extensions:
            links = await lx_extension.extract_links(response, rules)
            if len(links) == 0:
                continue
            links = [link_to_str(l) for l in links]
            name = lx_extension.name if hasattr(lx_extension, "name") else "default"
            if name not in link_dict:
                link_dict[name] = links
            else:
                link_dict[name].extend(links)
        return link_dict

    # Set extracted links into response.mete["extracted_links"]
    # return Deferred of response
    def process_response(self, response):
        d = as_deferred(self.extract_links(response))

        def _on_success(link_dict):
            if len(link_dict) > 0:
                assert "extracted_links" not in response.meta
                response.meta["extracted_links"] = link_dict

        d.addCallback(_on_success)
        d.addBoth(lambda _: response)

        return d


class LinkExtractorExtension:
    def __init__(self, lx_cls):
        self.lx_cls = lx_cls

    def _match_rule(self, rule):
        raise NotImplementedError("")

    def _new_linkextractor(self, rule):
        raise NotImplementedError("")

    def validate_rule(self, rule):
        return isinstance(rule, dict) and rule.get("type", None) is not None

    async def extract_links(self, response, rules):
        link_extractors = [
            self._new_linkextractor(rule)
            for rule in rules
            if self.validate_rule(rule) and self._match_rule(rule)
        ]
        links = []
        for lx in link_extractors:
            _links = lx.extract_links(response)
            if isawaitable(_links):
                _links = await _links
            links.extend(_links)
        return links