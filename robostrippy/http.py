import requests

USERAGENT_HEADER = """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) \
AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.101 Safari/537.11"""
ACCEPT_HEADER = """text/html,application/xhtml+xml,application/xml;q=0.9,\
*/*;q=0.8"""


class Fetcher:
    @classmethod
    def get(self, url, headers=None):
        default_headers = {
            'Accept': ACCEPT_HEADER,
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': USERAGENT_HEADER
            }
        default_headers.update(headers or {})
        req = requests.get(url, headers=default_headers)
        return req.text
