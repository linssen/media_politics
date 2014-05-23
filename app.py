#!/usr/bin/env
import re

import requests
from bs4 import BeautifulSoup

class NewsSite(object):

    parties = {
        'ukip': {
            'mentions': {'headlines': [], 'body': []},
            'terms': ['ukip', 'nigel farage', 'farage'],
        },
        'tory': {
            'mentions': {'headlines': [], 'body': []},
            'terms': ['conservative', 'conservatives', 'tory', 'tories', 'david cameron', 'cameron'],
        },
        'labour': {
            'mentions': {'headlines': [], 'body': []},
            'terms': ['labour', 'ed milliband', 'milliband'],
        },
        'libdem': {
            'mentions': {'headlines': [], 'body': []},
            'terms': ['liberal democrat', 'liberal democrats', 'lib dem', 'libs', 'nick clegg', 'clegg'],
        },
    }
    points = {
        'headline': 2,
        'body': 1,
    }
    politics_url = None
    headline_selector = None
    body_selector = None

    def go(self):
        soup = self.get_page(self.politics_url)
        headlines = self.get_headlines(soup)
        for headline in headlines:
            self.process_headline(headline)

    def process_headline(self, headline):
        text = headline.get_text()
        for name, party in self.parties.items():
            pattern = re.compile('(?i)({0})'.format('|'.join(party['terms'])))
            if (pattern.search(text)):
                party['mentions']['headlines'].append(text)

    def get_page(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib')
        return soup

    def get_headlines(self, soup):
        return soup.select(self.headline_selector)

    def get_body(self, soup):
        return soup.select(self.body_selector).get_text()

class Guardian(NewsSite):

    def __init__(self):
        self.politics_url = 'http://www.theguardian.com/politics?view=mobile'
        self.headline_selector = '.item__title'
        self.body_selector = '[itemprop="articleBody"]'

def main():
   guardian = Guardian();
   guardian.go()
   print guardian.parties


if __name__ == '__main__':
    main()
