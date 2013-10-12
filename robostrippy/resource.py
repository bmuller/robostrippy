from bs4 import BeautifulSoup
from compiler.ast import flatten
from urlparse import urlparse

from robostrippy.http import Fetcher


class attr(object):
    def __init__(self, selectors, attribute=None, all=False):
        self.selectors = selectors
        if not isinstance(self.selectors, list):
            self.selectors = [self.selectors]
        self.attribute = attribute
        self.all = all

    def text(self, elem):
        return "".join([s.strip() for s in elem.strings])

    def __get__(self, obj, objtype):
        matches = obj._content.select(self.selectors[0])
        for selector in self.selectors[1:]:
            matches = flatten([match.select(selector) for match in matches])
        if len(matches) == 0:
            return None
        if self.attribute is not None:
            if self.all:
                return [match.get(self.attribute) for match in matches]
            return matches[0].get(self.attribute)
        if self.all:
            return [self.text(elem) for elem in matches]
        return self.text(matches[0])


class attrList(object):
    def __init__(self, selector, klass):
        self.selector = selector
        self.klass = klass

    def __get__(self, obj, objtype):
        matches = obj._content.select(self.selector)
        return [self.klass(None, match) for match in matches]


class Resource:
    def __init__(self, url, content=None, headers=None):
        self._url = url
        self._content = content
        if self._content is None:
            html = Fetcher.get(self._url)
            self._content = BeautifulSoup(html)
        elif type(self._content) is str:
            self._content = BeautifulSoup(self._content)

    def __str__(self):
        props = []
        for key in dir(self):
            if not key.startswith("_"):
                props.append("%s='%s'" % (key, getattr(self, key)))
        return "<%s %s>" % (self.__class__.__name__, ", ".join(props))

    def absoluteURL(self, url):
        if url.startswith('http://') or url.startswith('https://'):
            return url

        parsed = urlparse(self._url)
        scheme = parsed.scheme or 'http'
        if url.startswith('//'):
            return "%s:%s" % (scheme, url)

        # absolute
        if url.startswith('/'):
            return "%s://%s%s" % (parsed.scheme, parsed.netloc, url)

        # relative, but source ends in '/', as in http://something.com/blah/blah
        if parsed.path.endswith('/'):
            return "%s://%s%s%s" % (parsed.scheme, parsed.netloc, parsed.path, url)

        # relative, but url source has crap after /
        parts = parsed.path.split('/')[:-1]
        path = "/".join(parts) + "/"
        return "%s://%s%s%s" % (parsed.scheme, parsed.netloc, path, url)

    __repr__ = __str__
