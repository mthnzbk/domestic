from feedparser import parse
import feedparser

def isRSS(link):
    feed = parse(link)
    if feed.bozo:
        if type(feed.bozo_exception) == feedparser.CharacterEncodingOverride:
            return True
        else:
            return False
    else: return True

def feedInfo(link):
    rss = parse(link)
    print(rss.feed.link, rss.href, rss.feed.title, rss.feed.subtitle)
    return {"sitelink" : rss.feed.link, "feedlink" : rss.href, "title" : rss.feed.title, "description" : rss.feed.subtitle}