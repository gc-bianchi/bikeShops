import logging
import os
import pandas as pd
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from googlesearch import search

logging.getLogger("scrapy").propagate = False

list = [
    "http://www.wiss-cycles.com",
    "https://www.wolvertonsbikes.com/",
]
