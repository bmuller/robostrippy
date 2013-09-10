from robostrippy.resource import attr, attrList, Resource


class YellowPage(Resource):
    phone = attr("p.phone strong")
    street = attr("span.street-address")
    city = attr("span.locality")
    state = attr("span.region")
    zip = attr("span.postal-code")

    @property
    def address(self):
        return " ".join([self.street, self.city, self.state, self.zip])


class YellowPagesListItem(Resource):
    name = attr("h3.business-name a")
    url = attr("h3.business-name a", attribute = 'href')

    @property
    def details(self):
        return YellowPage(self.url)


class YellowPagesList(Resource):
    businesses = attrList("div.result", YellowPagesListItem)

    def __init__(self, city, name):
        city = city.replace(',', '').replace(' ', '-')
        name = name.replace(' ', '-')
        Resource.__init__(self, "http://www.yellowpages.com/%s/%s" % (city, name))


if __name__ == "__main__":
    ypl = YellowPagesList("Washington, DC", "Quarry House Tavern")
    business = ypl.businesses[0]
    # print name from list
    print business.name
    # now fetch details page
    details = business.details
    print "lives at %s" % details.address
    print "with phone # %s" % details.phone
