import xml.etree.ElementTree as ET
import requests


class GoogleNews(object):

    def __init__(self):
        pass

    @staticmethod
    def get_url(place):
        return 'https://news.google.com/news/section?geo=%s&output=rss' \
               % ('+'.join(place.split()))

    @staticmethod
    def get_rss_xml(url):
        return requests.get(url).text

    @staticmethod
    def get_news_title(rss_xml):
        root = ET.fromstring(rss_xml)
        return [item.find('title').text for item in root.iter('item')][:5]

    def main(self, place):
        url = self.get_url(place)
        rss_xml = self.get_rss_xml(url).encode('utf-8')
        return self.get_news_title(rss_xml)
