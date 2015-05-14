from setuptools import setup, find_packages

setup(
    name = "domestic-reader",
    packages = find_packages(),
    package_data = {"domestic" : ["languages/*", "images/icons/*" ,"images/*.png", "media/*"]},
    scripts = ["domestic-reader"],
    version = "0.1.8.0",
    license = "GPL v3",
    description = "Free RSS/Atom Reader.",
    author = "Metehan Özbek",
    author_email = "metehan@metehan.us",
    url = "https://github.com/mthnzbk/domestic",
    #download_url = "https://github.com/mthnzbk/domestic",
    keywords = ["PyQt5","feedparser", "sqlite", "bs4", "reader", "rss reader", "BeautifulSoup"],
    classifiers = [
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],

)