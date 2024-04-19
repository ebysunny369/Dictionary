from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# Create your views here.

def index(request):
    return render(request, 'index.html')

def search(request):
    word = request.GET['word']
    res = requests.get('https://www.dictionary.com/browse/' + word)
    res2 = requests.get('https://www.thesaurus.com/browse/' + word)

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')
        meaning = soup.find_all('div', {'value': '1'})
        if meaning:
            meaning1 = meaning[0].getText()
        else:
            meaning1 = 'Sorry, ' + word + ' Is Not Found In Our Database'
    else:
        meaning1 = 'Error fetching the meaning for ' + word

    if res2.status_code == 200:
        soup2 = BeautifulSoup(res2.text, 'lxml')

        synonyms = soup2.find_all('a', {'class': 'css-r5sw71-ItemAnchor etbu2a31'})
        se = [b.text.strip() for b in synonyms]

        antonyms = soup2.find_all('a', {'class': 'css-lqr09m-ItemAnchor etbu2a31'})
        ae = [c.text.strip() for c in antonyms]
    else:
        se = []
        ae = []

    results = {
        'word': word,
        'meaning': meaning1,
    }

    return render(request, 'search.html', {'se': se, 'ae': ae, 'results': results})
