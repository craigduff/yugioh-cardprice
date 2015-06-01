# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from ygoprice.forms import DocumentForm
import requests

import time

def GetCardNameFromCode(code):
    response = (requests.get('http://yugioh.wikia.com/api.php?action=query&redirects=&format=json&titles='+code.zfill(8)))
    name = response.json()['query']['redirects'][0]['to']
    return name

def GetCardPrices(card):
    response = (requests.get('http://yugiohprices.com/api/get_card_prices/'+card))
    low = response.json()['data'][0]['price_data']['data']['prices']['low']
    average = response.json()['data'][0]['price_data']['data']['prices']['average']
    high = response.json()['data'][0]['price_data']['data']['prices']['high']
    return low, average, high

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            decklist = {}
            totals = [0, 0, 0]
            docfile0 = request.FILES['docfile']
            if docfile0.name.endswith('.ydk'):
                input = docfile0.readlines()
                start_time = time.time()
                
                for line in input:
                    if line[0].isdigit():
                        code = line.strip()
                        if code in decklist:
                            (decklist[code])[4] += 1
                        else:
                            try:
                                name = GetCardNameFromCode(code)
                                low, average, high = GetCardPrices(name)
                                decklist[code] = [name, low, average, high, 1]
                            except:
                                print(code)
                        
                print("--- %s seconds ---" % (time.time() - start_time))
                for key, value in decklist.iteritems():
                    totals[0] += value[1]*value[4]
                    totals[1] += value[2]*value[4]
                    totals[2] += value[3]*value[4]

            return render_to_response('ygoprice/index.html', {'form': form, 'deck': decklist, 'totals': totals}, context_instance=RequestContext(request))
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('ygoprice.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    #documents = Document.objects.all()
    #'documents': documents, 
    # Render list page with the documents and the form
    return render_to_response(
        'ygoprice/index.html',
        {'form': form},
        context_instance=RequestContext(request)
    )