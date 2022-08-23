from typing import Optional

from bs4 import BeautifulSoup
from lxml.html import HTMLParser

from algernon.parser.abc import ParserABC
from algernon.parser.exc import ParserError


class ParserSimple(ParserABC):

    def parse(self, content: bytes, mime_type: str, encoding: Optional[str] = None) -> bool:
        self.error = None
        try:
            if mime_type == 'text/html':
                self._parse_html(content, encoding)
            else:
                raise ParserError(f'Parsing of mime type "{mime_type}" is not implemented')
            return True
        except ParserError as e:
            self.error = e
            self.lgg.error('{}: {}'.format(type(e), str(e)))
            return False

    def _parse_html(self, content: bytes, encoding: Optional[str]):
        self.lang, self.title, self.description, self.tags, self.meta = None, None, None, [], {}

        try:
            soup = BeautifulSoup(content, 'html.parser', from_encoding=encoding)
        except HTMLParser.HTMLParseError as e:
            raise ParserError() from e

        html = soup.html
        if html:
            self.lang = html.attrs.get('lang')

        head = soup.head
        if head:
            for e in head.find_all('meta'):
                # If the meta tag has attribute "content", we expect it to have one other attribute that tells the type
                # of content; basically, "content" and the other attribute are key-value pairs.
                mc = e.attrs.get('content')
                if mc:
                    # Get the "other" attribute. If we have more than one "other" attribute, we arbitrarily just take
                    # the first one. Although, this should not happen(tm).
                    aa = [a for a in e.attrs.keys() if a != 'content']
                    k = e[aa[0]].strip().lower()
                    # Just in case. Although, they should be unique.
                    while k in self.meta:
                        k += '_'
                    self.meta[k] = mc.strip()
                else:
                    # Not all meta tags have "content", they simply have one attribute that is the single
                    # key-value pair
                    for k, v in e.attrs.items():
                        k = k.lower()
                        while k in self.meta:
                            k += '_'
                        self.meta[k] = v.strip()
            if head.title:
                self.title = head.title.string.strip()
            if not self.title:
                self.title = self.meta.get('og:title', self.meta.get('twitter:title'))
            self.description = self.meta.get('description', self.meta.get('og:description',
                                                                          self.meta.get('twitter:description')))
