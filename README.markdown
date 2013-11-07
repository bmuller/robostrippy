# RoboStrippy
### Python lib to strip websites. Like a robot.

BeautifulSoup and other Python libs make parsing easy - but they don't make it easy to encapsulate that logic in ways that let you treat web resources like objects.  RoboStrippy does.

## Installation

```
easy_install robostrippy
```

## Usage
Let’s say you want to pull down information about a business from the Yellow Pages website.

### Single Item
For the first example, let’s pretend you want a single business’ information and you already have the URL.

First, create a class and then describe one of the items on the page that you want to pull out (in this case, the business details):

```python
#!/usr/bin/env python
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
```

In the class definition, I’ve described the attributes that I want to pull out and the query necessary to pull that information out. For each attribute, you can give a CSS selector code (potentially as an array if there are multiple steps).

It is then trivial to pull information from the page:

```python
url = "http://www.yellowpages.com/silver-spring-md/mip/quarry-house-tavern-3342829"
yp = YellowPage(url)
print yp.phone
print yp.address
```

### Pages with Lists
For the second example, let’s say you want to be able to search the Yellow Pages website and then get the details for each matching business.

First, let’s define our listing class.

```python
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
```

This allows us to create an object that represents the list of businesses based on city and business name, and then get the details per business.

```python
ypl = YellowPagesList("Washington, DC", "Quarry House Tavern")
business = ypl.businesses[0]

# print name from list
print business.name

# now fetch details page
details = business.details
print "lives at %s" % details.address
print "with phone # %s" % details.phone
```
###Missing elements
What if the element you are looking for is missing? You can specify an alternative element to use thanks to the attrCoalesce class:

```python
title = attrCoalesce(('meta[property="og:title"]', {'attribute': 'content'}),
                     ('meta[name="twitter:title"]', {'attribute': 'content'}),
                     ('title'))
```

See the examples folder for other examples.