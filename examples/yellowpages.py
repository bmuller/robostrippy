from robostrippy.resource import attr, attrList, Resource


class YellowPage(Resource):
    phone = attr("p.phone")
    street = attr("p.street-address")
    citystate = attr("p.city-state")

    @property
    def address(self):
        return self.street + " " + self.citystate


class YellowPagesListItem(Resource):
    name = attr("h3 a.business-name")
    url = attr("h3 a.business-name", attribute = 'href')

    @property
    def details(self):
        return YellowPage(self.absoluteURL(self.url))


class YellowPagesList(Resource):
    businesses = attrList("div.result", YellowPagesListItem)

    def __init__(self, city, name):
        city = city.replace(',', '').replace(' ', '-')
        name = name.replace(' ', '-')
        super().__init__("http://www.yellowpages.com/%s/%s" % (city, name))


if __name__ == "__main__":
    ypl = YellowPagesList("Washington, DC", "Quarry House Tavern")
    business = ypl.businesses[0]
    # print name from list
    print(business.name)
    # now fetch details page
    details = business.details
    print("lives at %s" % details.address)
    print("with phone # %s" % details.phone)
