from django.shortcuts import render
from django.http import HttpResponseRedirect

from stations.models import RadioList, Countries, UserSession, Favourite, RssFeed

# Create your views here.

def index(request):
    return render(request, 'frontend/index.html', {
        "country" : Countries.objects.get(id=1)
    })

def redirect(request, pk, title, country=1):
    country = Countries.objects.get(id=country)
    news = RssFeed.objects.get(id=pk)
    return render(request, 'frontend/redirect.html', {
        "news" : news,
        "country" : country
    })

def latest(request):
    return render(request, 'frontend/latest.html', {
        "country" : Countries.objects.get(id=1)
    })
def search(request):
    country = request.POST.get("country_id")
    pk = request.POST.get("keyword")
    countryOBJ = Countries.objects.get(id=country)
    radios = RadioList.objects.filter(radio_name__contains=pk, country=countryOBJ)

    return render(request, 'frontend/search.html', {
        'radios' : radios,
        'country' : countryOBJ
    })

def countryPage(request, pk):
    try:
        country = Countries.objects.get(country_code__iexact=pk)
    except:
        return HttpResponseRedirect("/")
    return render(request, 'frontend/country.html', {
        "country" : country
    })
    

def radios(request, country=1):
    country = Countries.objects.get(id=country)
    return render(request, 'frontend/radios.html', {
        "country" : country
    })

def popular(request, country=1):
    country = Countries.objects.get(id=country)
    return render(request, 'frontend/popular.html', {
        "country" : country
    })

def favouritePage(request, country=1):
    country = Countries.objects.get(id=country)
    return render(request, 'frontend/favourite.html', {
        "country" : country
    })

def genrePage(request, pk):
    return render(request, 'frontend/genre.html', {
        "main" : pk
    })

def radioPage(request, pk, title):
    radio = RadioList.objects.get(id=pk)
    if not request.session.exists(request.session.session_key):
        request.session.create()
    try:
        session = UserSession.objects.get(session=request.session.session_key)
    except:
        session = UserSession(session=request.session.session_key)
        session.save()
    try:
        Favourite.objects.get(radio=radio, session=session)
        fav = True
    except:
        fav = False
    return render(request, 'frontend/radio.html', {
        "radio" : radio,
        "country" : radio.country,
        "fav" : fav
        })


def radioPlayerPage(request, pk, title):
    radio = RadioList.objects.get(id=pk)
    return render(request, 'frontend/radioPlayer.html', {
        "radio" : radio,
        "country" : radio.country
    })