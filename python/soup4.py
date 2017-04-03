#!/usr/local/bin/env python3
from beautifulscraper import BeautifulScraper
scraper = BeautifulScraper()

body = scraper.go("https://github.com/adregner/beautifulscraper")
body.select(".repository-meta-content")[0].text
