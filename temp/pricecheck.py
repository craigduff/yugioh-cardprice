from lxml import html
from lxml.html import fragment_fromstring
from lxml.etree import tostring
from bs4 import BeautifulSoup
import requests
import urllib2
import json
import re
import time
############################################

def GetCardPrices(card):
    response = (requests.get('http://yugiohprices.com/api/get_card_prices/'+card))
    low = response.json()['data'][0]['price_data']['data']['prices']['low']
    average = response.json()['data'][0]['price_data']['data']['prices']['average']
    high = response.json()['data'][0]['price_data']['data']['prices']['high']
    return low, average, high

def FixName(name):
    name = re.sub(r'D. D.', 'D.D.', name)
    name = re.sub(r'Graverobbers', 'Graverobber\'s', name)
    return name

####### OPEN FILE, GET LIST OF NAMES #######
with open('temp/deck2.ydk', 'r') as input:
    sumLow = 0
    sumAve = 0
    sumHigh = 0
    start_time = time.time()
    
    for line in input:
        if line[0] is not '#':
            code = line.strip()
            url = "http://en.ygo-card.de/result_links.php?htm_gba=%s&htm_langu=us" % code
            
            soup = BeautifulSoup (urllib2.urlopen(url).read())
            
            for elem in soup(text=re.compile(r''+code+'')):
                table = elem.parent.parent.parent.parent
            
            row = table.findAll('td')[2]
            #print row.findAll('a')[0]['href']
            name = row.get_text()
            # code = row.href=asdasd
            name = FixName(name)
            #print name
            
            low, average, high = GetCardPrices(name)
            sumLow += low
            sumHigh += high
            sumAve += average
            
            #print name, low, average, high
    print("--- %s seconds ---" % (time.time() - start_time))
    print 'LOW: ${0}\tAVERAGE: ${1}\tHIGH: ${2}'.format(sumLow, sumAve, sumHigh)
############################################

