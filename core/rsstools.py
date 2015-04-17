from feedparser import parse
import time

def isRSS(link):
    feed = parse(link)
    if feed.bozo:
        return False
    else: return True

def feedInfo(link):
    rss = parse(link)
    print(rss.feed.link, rss.href, rss.feed.title, rss.feed.subtitle)
    return rss.feed.link, rss.href, rss.feed.title, rss.feed.subtitle