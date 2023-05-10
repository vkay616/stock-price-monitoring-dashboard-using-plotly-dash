import requests
from bs4 import BeautifulSoup

def getHTML(url):
    return requests.get(url).text

class GFA:
    def __init__(self):
        self.url_prefix = "https://www.google.com/finance/quote/"
        
    def get(self, company, exchange):
        url = self.url_prefix + "%s:%s"%(company, exchange)
        html_document = getHTML(url)
        soup = BeautifulSoup(html_document, 'html.parser')
        div = soup.select('div.YMlKec.fxKbKc')
        price = float(div[0].get_text()[1:].replace(',', ''))
        return price

gfa = GFA()
print(gfa.get('RELIANCE', 'NSE'))