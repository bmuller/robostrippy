from robostrippy.resource import attrCoalesce, Resource


class MetadataScraper(Resource):
    image = attrCoalesce(
        ('meta[name="twitter:image"]', {'attribute': 'content'}),
        ('meta[name="twitter:image:src"]', {'attribute': 'content'}),
        ('meta[name="twitter:image0:src"]', {'attribute': 'content'}),
        ('meta[property="og:image"]', {'attribute': 'content'}))
    title = attrCoalesce(
        ('meta[property="og:title"]', {'attribute': 'content'}),
        ('meta[name="twitter:title"]', {'attribute': 'content'}),
        ('title'))
    description = attrCoalesce(('meta[property="og:description"]', {'attribute': 'content'}),
                               ('meta[name="twitter:description"]', {'attribute': 'content'}))

    def __init__(self, url):
        Resource.__init__(self, url)
        print("Scraping page %s ... ... ..." % url)


if __name__ == '__main__':
    scraper = MetadataScraper("http://seen.co/event/twitteripo--2013-5386")
    print(scraper.title)
    print(scraper.image)
    print(scraper.description)
