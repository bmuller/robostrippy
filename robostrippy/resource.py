from itertools import chain

from bs4 import BeautifulSoup

from robostrippy.http import get
from robostrippy import utils


def _text(elem):
    return "".join([s.strip() for s in elem.strings])


# pylint: disable=invalid-name,protected-access
class attr:
    def __init__(self, selectors, attribute=None,
                 all_matches=False, elems=False):
        """
        @param attribute Get attribute from element (default is cdata text)
        @param all_matches Return all matches (not just first)
        @param elems Return BeautifulSoup elements that match (will return
        list)
        """
        self.selectors = selectors
        if not isinstance(self.selectors, list):
            self.selectors = [self.selectors]
        self.attribute = attribute
        self.all_matches = all_matches
        self.elems = elems

    def __get__(self, obj, objtype):
        matches = obj._content.select(self.selectors[0])
        for selector in self.selectors[1:]:
            selected = [match.select(selector) for match in matches]
            matches = list(chain.from_iterable(selected))
        if self.elems:
            return matches
        if len(matches) == 0:
            return None
        if self.attribute is not None:
            if self.all_matches:
                return [match.get(self.attribute) for match in matches]
            return matches[0].get(self.attribute)
        if self.all_matches:
            return [_text(elem) for elem in matches]
        return _text(matches[0])


class attrCoalesce:
    def __init__(self, *args):
        self.selectors = args

    def __get__(self, obj, objtype):
        for sargs in self.selectors:
            if not isinstance(sargs, tuple):
                alt = attr(sargs)
            elif len(sargs) < 2:
                alt = attr(sargs[0])
            else:
                alt = attr(sargs[0], **sargs[1])
            result = alt.__get__(obj, objtype)
            if result is not None:
                return result
        return None


class attrList:
    def __init__(self, selector, klass):
        self.selector = selector
        self.klass = klass

    def __get__(self, obj, objtype):
        matches = obj._content.select(self.selector)
        return [self.klass(obj._url, match) for match in matches]


class Resource:
    def __init__(self, url, content=None):
        self._url = url
        self._content = content
        if self._content is None:
            html = get(self._url)
            self._content = BeautifulSoup(html, "lxml")
        elif isinstance(self._content, str):
            self._content = BeautifulSoup(self._content, "lxml")

    def __str__(self):
        props = []
        for key in dir(self):
            if not key.startswith("_") and not key == "absolute_url":
                props.append("%s='%s'" % (key, getattr(self, key)))
        return "<%s %s>" % (self.__class__.__name__, ", ".join(props))

    def absolute_url(self, url):
        return utils.absolute_url(self._url, url)

    __repr__ = __str__
