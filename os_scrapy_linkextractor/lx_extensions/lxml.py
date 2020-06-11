from expiringdict import ExpiringDict

from os_scrapy_linkextractor.linkextractors.lxmlhtml import ReCachedLinkExtractor
from os_scrapy_linkextractor.lx_extensions import LinkExtractorExtension


class LxmlLinkExtractorExtension(LinkExtractorExtension):
    def __init__(self, cache_size, cache_expire):
        self.name = "lxml"
        self.re_cache = None
        if cache_size > 0:
            self.re_cache = ExpiringDict(
                max_len=cache_size, max_age_seconds=cache_expire
            )
        super(LxmlLinkExtractorExtension, self).__init__(ReCachedLinkExtractor)

    def _match_rule(self, rule):
        return rule.get("type", None) == "lxml"

    def _new_linkextractor(self, rule):
        lx_kwargs = {}
        for key in [
            "allow",
            "deny",
            "allow_domains",
            "deny_domains",
            "restrict_xpaths",
            "tags",
            "attrs",
            "restrict_css",
        ]:
            v = rule.get(key, None)
            if v is not None and (
                isinstance(v, str)
                or (isinstance(v, (list, tuple)) and all(isinstance(i, str) for i in v))
            ):
                lx_kwargs[key] = v
        return self.lx_cls(re_cache=self.re_cache, **lx_kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        cache_size = settings.getint("LX_RECACHE_SIZE", 5000)
        cache_expire = settings.getint("LX_RECACHE_EXPIRE", 7 * 24 * 60 * 60)
        if not settings.getbool("LX_RECACHE_ENABLED"):
            cache_size = 0
        return cls(cache_size, cache_expire)
