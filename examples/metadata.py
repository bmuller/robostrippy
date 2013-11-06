from robostrippy.resource import attr, attrList, Resource

class GenericScraper(Resource):
    image       = attr('meta[name="twitter:image"]', attribute='content').otherwise(attr('meta[name="twitter:image:src"]', attribute='content')).otherwise(attr('meta[name="twitter:image0:src"]', attribute='content')).otherwise(attr('meta[property="og:image"]', attribute='content'))
    title       = attr('meta[property="og:title"]', attribute='content').otherwise(attr('meta[name="twitter:title"]', attribute='content')).otherwise(attr('title'))
    description = attr('meta[property="og:description"]', attribute='content').otherwise(attr('meta[name="twitter:description"]', attribute='content'))

    def __init__(self, url):
    	Resource.__init__(self, url)
        print("Scraping page %s ... ... ..." % url)
        
if __name__ == '__main__' : 
    scraper = GenericScraper("http://seen.co/event/new-york-tech-meetup-new-york-ny-2013-3250")
    print(scraper.title)
    print(scraper.image)
    print(scraper.description)
