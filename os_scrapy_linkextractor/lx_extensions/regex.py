from os_scrapy_linkextractor.linkextractors.regex import RegexLinkExtractor
from os_scrapy_linkextractor.lx_extensions import LinkExtractorExtension


class ReLinkExtractorExtension(LinkExtractorExtension):
    def __init__(self):
        self.name = "re"
        super(ReLinkExtractorExtension, self).__init__(RegexLinkExtractor)

    def _match_rule(self, rule):
        return rule.get("type", None) == "re"

    def _new_linkextractor(self, rule):
        lx_kwargs = {}
        for key in ["allow_domains", "deny_domains"]:
            v = rule.get(key, None)
            if v is not None and (
                isinstance(v, str)
                or (isinstance(v, (list, tuple)) and all(isinstance(i, str) for i in v))
            ):
                lx_kwargs[key] = v
        lx_kwargs["same_domain_only"] = rule.get("same_domain_only", None)
        return self.lx_cls(**lx_kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        return cls()
