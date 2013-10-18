from urlparse import urlparse


def absoluteURL(baseurl, url):
    if url.startswith('http://') or url.startswith('https://'):
        return url

    parsed = urlparse(baseurl)
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
