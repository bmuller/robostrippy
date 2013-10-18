from bs4 import BeautifulSoup
from compiler.ast import flatten

from robostrippy.http import Fetcher
from robostrippy import utils


class attr(object):
    def __init__(self, selectors, attribute=None, all=False, elems=False):
        """
        @param attribute Get attribute from element (default is cdata text)
        @param all Return all matches (not just first)
        @param elems Return BeautifulSoup elements that match (will return
        list)
        """
        self.selectors = selectors
        if not isinstance(self.selectors, list):
            self.selectors = [self.selectors]
        self.attribute = attribute
        self.all = all
        self.elems = elems

    def text(self, elem):
        return "".join([s.strip() for s in elem.strings])

    def __get__(self, obj, objtype):
        matches = obj._content.select(self.selectors[0])
        for selector in self.selectors[1:]:
            matches = flatten([match.select(selector) for match in matches])
        if self.elems:
            return matches
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
            self._content = BeautifulSoup(html, "lxml")
        elif isinstance(self._content, str):
            self._content = BeautifulSoup(self._content, "lxml")

    def __str__(self):
        props = []
        for key in dir(self):
            if not key.startswith("_"):
                props.append("%s='%s'" % (key, getattr(self, key)))
        return "<%s %s>" % (self.__class__.__name__, ", ".join(props))

    def absoluteURL(self, url):
        return utils.absoluteURL(self._url, url)

    __repr__ = __str__
