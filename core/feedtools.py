from feedparser import parse

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
                l = [feed.feed.title, entry.title_detail.value, entry.author_detail.name, entry.tags[0].term,
                     entry.published_parsed , entry.link, entry.content[0].value]
                fLists.append(l)
        else: pass
    return fLists
