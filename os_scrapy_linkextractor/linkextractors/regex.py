# Copy from scrapy.linkextractors.regex.py, remove dependence of smgllib

import re
from urllib.parse import urljoin, urlparse

from scrapy.link import Link
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.python import unique as unique_list
from scrapy.utils.response import get_base_url
from scrapy.utils.url import url_is_from_any_domain
from w3lib.html import (
    get_base_url as w3_get_base_url,
    remove_tags,
    replace_entities,
    replace_escape_chars,
)
from w3lib.url import canonicalize_url, to_unicode

from os_scrapy_linkextractor.utils import get_url_domain

linkre = re.compile(
    "<a\s.*?href=(\"[.#]+?\"|'[.#]+?'|[^\s]+?)(>|\s.*?>)(.*?)<[/ ]?a>",
    re.DOTALL | re.IGNORECASE,
)


def clean_link(link_text):
    """Remove leading and trailing whitespace and punctuation"""
    return link_text.strip("\t\r\n '\"\x0c")


class RegexParserLinkExtractor:
    def __init__(self, canonicalized=False):
        if canonicalized:
            self.link_key = lambda link: link.url
        else:
            self.link_key = lambda link: canonicalize_url(link.url, keep_fragments=True)

    def _extract_links(
        self,
        response_text,
        response_url,
        response_encoding,
        base_url=None,
        canonicalized=False,
    ):
        def clean_text(text):
            return replace_escape_chars(remove_tags(text)).strip()

        def clean_url(url):
            clean_url = ""
            try:
                clean_url = urljoin(base_url, replace_entities(clean_link(url)),)
            except ValueError:
                pass
            return clean_url

        if base_url is None:
            base_url = w3_get_base_url(response_text, response_url, response_encoding)
        u_text = to_unicode(response_text, response_encoding)
        links_text = linkre.findall(u_text)
        # links_text = linkre.findall(response_text)
        return [Link(clean_url(url), clean_text(text)) for url, _, text in links_text]

    def _process_links(self, links):
        return unique_list(links, key=self.link_key)


class RegexLinkExtractor:
    def __init__(
        self,
        allow_domains=(),
        deny_domains=(),
        same_domain_only=False,
        canonicalize=False,
    ):
        self.link_extractor = RegexParserLinkExtractor(canonicalized=canonicalize)
        self.allow_domains = set(arg_to_iter(allow_domains))
        self.deny_domains = set(arg_to_iter(deny_domains))
        self.same_domain_only = same_domain_only
        self.canonicalize = canonicalize

    def _link_allowed(self, link):
        parsed_url = urlparse(link.url)
        if self.allow_domains and not url_is_from_any_domain(
            parsed_url, self.allow_domains
        ):
            return False
        if self.deny_domains and url_is_from_any_domain(parsed_url, self.deny_domains):
            return False
        return True

    def _process_links(self, response, links):
        links = [x for x in links if self._link_allowed(x)]
        if self.same_domain_only:
            response_domain = get_url_domain(response.url)
            links = [
                x
                for x in links
                if response_domain and url_is_from_any_domain(x.url, [response_domain])
            ]
        if self.canonicalize:
            for link in links:
                link.url = canonicalize_url(link.url)
        links = self.link_extractor._process_links(links)
        return links

    def _extract_links(self, *args, **kwargs):
        return self.link_extractor._extract_links(*args, **kwargs)

    def extract_links(self, response):
        base_url = get_base_url(response)

        links = self._extract_links(
            response.body, response.url, response.encoding, base_url
        )
        return self._process_links(response, links)
