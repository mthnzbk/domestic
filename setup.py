from setuptools import setup, find_packages

setup(
    name = "domestic-reader",
    packages = find_packages(),
    package_data = {"domestic" : ["languages/*", "images/icons/*" ,"images/*.png"]},
    scripts = ["domestic-reader"],
    version = "0.1.2.9",
    license = "GPL v3",
    description = u"""""",
    author = "Metehan Özbek",
    author_email = "metehan@metehan.us",
    url = "http://www.metehan.us/",
    download_url = "",
    keywords = ["PyQt5","feedparser", "sqlite", "bs4", "reader"],
    classifiers = [
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],

)