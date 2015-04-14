from feedparser import parse
import time

def isRSS(link):
    feed = parse(link)
    try:
        if feed.bozo_exception:
            return False
    except AttributeError:
        return True


def feedExtract(link):
    print(link)
    feed = parse(link)
    return feed.feed.title_detail.base, feed.feed.title

def readAllFeedEntries(feedList):
    fLists = [] #site adı, konu başlığı, yazar, kategori, tarih ---> url,  content
    for feedUrl in feedList:
        if isRSS(feedUrl[0]):
            feed = parse(feedUrl[0])
            for entry in feed.entries:
                a = entry.published_parsed
                publish = time.strftime("%d.%m.%Y %H:%M", a)
                l = [entry.link, feed.feed.title, entry.title_detail.value, entry.author_detail.name, entry.tags[0].term,
                     publish, entry.content[0].value]
                fLists.append(l)
            print(fLists)
        else: pass
    return fLists
