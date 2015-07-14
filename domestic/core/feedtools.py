import feedparser

def isFeed(link):
    feed = feedparser.parse(link)
    if feed.bozo:
        if type(feed.bozo_exception) == feedparser.CharacterEncodingOverride:
            return True
        if type(feed.bozo_exception) == feedparser.NonXMLContentType:
            return True
        else:
            return False
    else: return True

def feedInfo(link):
    rss = feedparser.parse(link)
    return {"sitelink" : rss.feed.link, "feedlink" : rss.href, "title" : rss.feed.title, "description" : rss.feed.get("subtitle","")}