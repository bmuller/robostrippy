from collections import namedtuple
from robostrippy.resource import attr, attrList, Resource

Post = namedtuple('Post', ['title', 'comments', 'points'])


class HackerNews(Resource):
    titles = attr("table table:nth-of-type(2) tr td.title a", all=True)
    points = attr("table table:nth-of-type(2) tr td.subtext span", all=True)
    comments = attr(["table table:nth-of-type(2) tr td.subtext", "a:nth-of-type(2)"], all=True)

    def __init__(self):
        Resource.__init__(self, "http://news.ycombinator.com")

    @property
    def posts(self):
        posts = zip(self.titles, self.points, self.comments)
        return [ Post(t, c, p) for t, p, c in posts ]


if __name__ == "__main__":
    hn = HackerNews()
    for post in hn.posts:
        print "%s\n\t%s and %s" % (post.title, post.points, post.comments)
