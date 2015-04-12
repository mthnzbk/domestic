from feedparser import parse

def isRSS(link):
    feed = parse(link)
    try:
        if feed.bozo_exception:
            return False
    except AttributeError:
        return True


def feedExtract(link):
    feed = parse(link)
    return feed.feed.title_detail.base, feed.feed.title

