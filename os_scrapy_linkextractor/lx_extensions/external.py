from os_scrapy_linkextractor.linkextractors.external import ExternalLinkExtractor
from os_scrapy_linkextractor.lx_extensions import LinkExtractorExtension


class ExternalLinkExtractorExtension(LinkExtractorExtension):
    def __init__(self):
        self.name = "external"
        super(ExternalLinkExtractorExtension, self).__init__(ExternalLinkExtractor)

    def _match_rule(self, rule):
        return rule.get("type", None) == "external"

    def _new_linkextractor(self, rule):
        lx_kwargs = {}
        for key in ["api", "method"]:
            v = rule.get(key, None)
            if v is not None and isinstance(v, str):
                lx_kwargs[key] = v
        return self.lx_cls(**lx_kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        return cls()
