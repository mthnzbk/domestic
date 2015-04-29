from setuptools import setup, find_packages


setup(
    name = "domestic-reader",
    packages = find_packages(),
    package_data = {"parcala" : ["resim/*", "language/*"]},
    py_modules = ["resource", "domestic"],
    scripts = ["domestic-reader"],
    version = "0.0.6.4",
    license = "GPL v3",
    description = u"""Free RSS Reader.""",
    author = "Metehan Özbek",
    author_email = "metehan@metehan.us",
    url = "http://www.metehan.us/",
    download_url = "",
    keywords = ["PyQt5","feedparser", "python3", "feed reader", "feed parser"],
    classifiers = [
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],

)