import re

from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.utils.misc import arg_to_iter

_re_type = type(re.compile("", 0))


class ReCachedLinkExtractor(LxmlLinkExtractor):
    def __init__(
        self,
        allow=(),
        deny=(),
        allow_domains=(),
        deny_domains=(),
        restrict_xpaths=(),
        tags=("a", "area"),
        attrs=("href",),
        canonicalize=False,
        unique=True,
        process_value=None,
        deny_extensions=None,
        restrict_css=(),
        strip=True,
        restrict_text=None,
        re_cache=None,
    ):
        self.re_cache = re_cache if isinstance(re_cache, dict) else None
        allow = [
            x if isinstance(x, _re_type) else self.text_to_re(x)
            for x in arg_to_iter(allow)
        ]
        deny = [
            x if isinstance(x, _re_type) else self.text_to_re(x)
            for x in arg_to_iter(deny)
        ]
        restrict_text = [
            x if isinstance(x, _re_type) else self.text_to_re(x)
            for x in arg_to_iter(restrict_text)
        ]
        super(ReCachedLinkExtractor, self).__init__(
            allow=allow,
            deny=deny,
            allow_domains=allow_domains,
            deny_domains=deny_domains,
            restrict_xpaths=restrict_xpaths,
            tags=tags,
            attrs=attrs,
            canonicalize=canonicalize,
            unique=unique,
            process_value=process_value,
            deny_extensions=deny_extensions,
            restrict_css=restrict_css,
            strip=strip,
            restrict_text=restrict_text,
        )

    def text_to_re(self, re_text):
        if self.re_cache is not None and re_text in self.re_cache:
            return self.re_cache[re_text]

        compiled_re = re.compile(re_text)
        if self.re_cache is not None:
            self.re_cache[re_text] = compiled_re
        return compiled_re
