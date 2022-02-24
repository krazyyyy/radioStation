from django.shortcuts import render
from django.http import JsonResponse
from django.forms import model_to_dict
import requests
from bs4 import BeautifulSoup

from stations.models import RadioList, RadioHistory, RadioSession, Category, Countries, RssFeed, UserSession, Favourite
# Create your views here.

def getRadios(request, country=1):
    countryOBJ = Countries.objects.get(id=country)
    
    if int(country) == 1:
        radios = RadioList.objects.filter(country=countryOBJ).exclude(popular=True).order_by("?")[:18]
    else:
        radios = RadioList.objects.filter(country=countryOBJ).exclude(popular=True).order_by("?")[:30]
    li = []
    for radio in radios:
        n = model_to_dict(radio)
        n.pop("radio_img", None)
        if radio.radio_img:
            n['img'] = radio.radio_img.url

        li.append(n)
    radio_feed = dict(feed=li)
    return JsonResponse(radio_feed)

def getPopularRadios(request, country=1):
    countryOBJ = Countries.objects.get(id=country)
    radios = RadioList.objects.filter(country=countryOBJ, popular=True).order_by("-id")[:12]
    li = []
    for radio in radios:
        n = model_to_dict(radio)
        n.pop("radio_img", None)
        if radio.radio_img:
            n['img'] = radio.radio_img.url

        li.append(n)
    radio_feed = dict(feed=li)
    return JsonResponse(radio_feed)

def AllRadios(request, country=1):
    countryOBJ = Countries.objects.get(id=country)
    radios = RadioList.objects.filter(country=country).order_by('radio_name')
    li = []
    for radio in radios:
        n = model_to_dict(radio)
        n.pop("radio_img", None)
        if radio.radio_img:
            n['img'] = radio.radio_img.url

        li.append(n)
    radio_feed = dict(feed=li)
    return JsonResponse(radio_feed)

def latest(request, country=1):
    countryOBJ = Countries.objects.get(id=country)
    radios = RadioList.objects.all().order_by('id')
    li = []
    for radio in radios:
        n = model_to_dict(radio)
        n.pop("radio_img", None)
        if radio.radio_img:
            n['img'] = radio.radio_img.url

        li.append(n)
    radio_feed = dict(feed=li)
    return JsonResponse(radio_feed)


def getRandomRadios(request, country):
    countryOBJ = Countries.objects.get(id=country)
    radios = RadioList.objects.filter(country=countryOBJ).order_by("?")[:6]
    li = []
    for radio in radios:
        n = model_to_dict(radio)
        n.pop("radio_img", None)
        if radio.radio_img:
            n['img'] = radio.radio_img.url

        li.append(n)
    radio_feed = dict(feed=li)
    return JsonResponse(radio_feed)

def getCurrentPlaying(request, pk):
    radio = RadioList.objects.get(id=pk)
    if radio.radio_link:
        try:
            r = requests.get(f"{radio.radio_link}currentsong?sid=1")
        except:
            data = dict(playing="", img="")
            return JsonResponse(data)

        cur = r.content.decode()
    else:
        data = dict(playing="", img="")
        return JsonResponse(data)
    try:
        imgg = cur.split("-")
        
        cur_req = f"https://theaudiodb.com/api/v1/json/523532/search.php?s={imgg[0][0:-1]}"

        im = requests.get(cur_req)
       

        cur_img = im.json()['artists'][0]['strArtistThumb']
    except:
        cur_img = ""
    # if not request.session.exists(request.session.session_key):
    #     request.session.create()
    # history = RadioHistory.objects.filter(session=request.session.session_key, radio=radio)
    # if history.exists():
    #    radio_history = history[0]
    # else:
    #     radio_history = RadioHistory(session=request.session.session_key, radio=radio)
    #     radio_history.save()
    # allPlaying = RadioSession.objects.filter(name=cur, history=radio_history)
    # if not allPlaying.exists():
    #     new_record = RadioSession(name=cur, img_link=cur_img, history=radio_history)
    #     new_record.save()
    
    data = dict(playing=cur, img=cur_img)
    return JsonResponse(data)

def addFavourite(request, pk):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    session = UserSession.objects.filter(session=request.session.session_key)
    if session.exists():
        session = session[0]
    else:
        session = UserSession(session=request.session.session_key)
        session.save()
    radio = RadioList.objects.get(id=pk)
    fav = Favourite.objects.filter(radio=radio, session=session)
    if not fav.exists():
        f = Favourite(radio=radio, session=session)
        f.save()
    return JsonResponse({"message" : "Radio Added"})

def removeFavourite(request, pk):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    session = UserSession.objects.filter(session=request.session.session_key)
    if session.exists():
        session = session[0]
    else:
        session = UserSession(session=request.session.session_key)
        session.save()
    radio = RadioList.objects.get(id=pk)
    fav = Favourite.objects.filter(radio=radio, session=session)
    fav[0].delete()
    return JsonResponse({"message" : "Radio Added"})

def FavouriteList(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    session = UserSession.objects.filter(session=request.session.session_key)
    fav = Favourite.objects.filter(session=session[0])

    li = []

    for radio in fav:
        n = model_to_dict(radio.radio)
        n.pop("radio_img", None)
        if radio.radio.radio_img:
            n['img'] = radio.radio.radio_img.url

        li.append(n)
    radio_feed = dict(feed=li)
    return JsonResponse(radio_feed)

def getRecentPlaying(request, pk):
    radio = RadioList.objects.get(id=pk)
    if not request.session.exists(request.session.session_key):
        request.session.create()
    history = RadioHistory.objects.filter(session=request.session.session_key, radio=radio)
    if history.exists():
        radio_history = history[0]
        radios = radio_history.radio_history_session.all().order_by('-id')[:10]
        li = []
        for i in radios:

            n = model_to_dict(i)
            li.append(n)
        radio_history = dict(history=li)
        return JsonResponse(radio_history)
    return JsonResponse({"message" : "No Histroy Yet"})

def getRecents(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    history = RadioHistory.objects.filter(session=request.session.session_key).order_by('-id')[:10]

    li = []
    if history.exists():
        # radio_history = history[0]
        for h in history:
            for i in h.radio_history_session.all().order_by("-id")[:1]:
               
                n = model_to_dict(i)
                li.append(n)
        radio_history = dict(history=li)
        return JsonResponse(radio_history)
    return JsonResponse({"message" : "No Histroy Yet"})

def getRandomRadio(request, country=1):
    country = Countries.objects.get(id=country)
    radio = RadioList.objects.filter(country=country).order_by('?')[0]
    rad = dict(radio_id=radio.id, radio_name=radio.radio_name, link=radio.play_link)
    return JsonResponse(rad)

def getByCategory(request, pk):
    category = Category.objects.filter(category__iexact=pk)
    li = []
    for i in category:
        n = model_to_dict(i.radio)
        n.pop("radio_img", None)
        if i.radio.radio_img:
            n['img'] = i.radio.radio_img.url
        li.append(n)
    radio = dict(feed=li)
    return JsonResponse(radio)

def getCountries(request):
    countries = Countries.objects.all()
    li = []
    for country in countries:
        n = model_to_dict(country)
        li.append(n)
    data = dict(countries=li)
    return JsonResponse(data)

def getNews(request):
    feeds = RadioList.objects.all()
    li = []
    insert_list = []
    
    links_list = []
    for feed in feeds:
        if not feed.rss_feed:
            continue
        try:
            url = requests.get(feed.rss_feed)
        except:
            continue
        soup = BeautifulSoup(url.content, 'xml')
        entries = soup.find_all('item')
        for i in entries:
            try:
                data = dict()
                chk = RssFeed.objects.filter(link__iexact=i.link.text)
                
                pub_ = i.pubDate.text.replace("+0000", "")
                try:
                    des = i.description.text
                except:
                    des = ""
                if not chk.exists() and i.link.text not in links_list:
                    links_list.append(i.link.text)
                    insert_list.append(RssFeed(title=i.title.text, link=i.link.text, source_id=feed, country=feed.country, source=feed.radio_name, pub_date=pub_, description=des))
                data['title'] = i.title.text
                data['link'] = i.link.text
  
                
                li.append(data)
            except:
                pass
    RssFeed.objects.bulk_create(insert_list)
    # feed = dict(feed=li)
    return JsonResponse({"message" : "success"})

def renderNews(request, pk):
    rd = RadioList.objects.get(id=pk)
    news = rd.source_radio.all().order_by('-id')[:4]
    # news = RssFeed.objects.filter(source__iexact=pk).order_by('-id')[:3]
    li = []
    for i in news:
        n = model_to_dict(i)
        li.append(n)
    feed = dict(feed=li)
    return JsonResponse(feed)

def renderHomeNews(request, country=1):
    countryOBJ = Countries.objects.get(id=country)
    news = RssFeed.objects.filter(country=countryOBJ).order_by('-id')[:12]
    # news = RssFeed.objects.filter(source__iexact=pk).order_by('-id')[:3]
    li = []
    for i in news:
        n = model_to_dict(i)
        li.append(n)
    feed = dict(feed=li)
    return JsonResponse(feed)

def renderRadioNews(request, country):
    countryOBJ = Countries.objects.get(id=country)
    news = RssFeed.objects.filter(country=countryOBJ).order_by('?')[:8]
    # news = RssFeed.objects.filter(source__iexact=pk).order_by('-id')[:3]
    li = []
    for i in news:
        n = model_to_dict(i)
        li.append(n)
    feed = dict(feed=li)
    return JsonResponse(feed)

def getSearches(requests, pk):
    radios = RadioList.objects.filter(radio_name__contains=pk).order_by("?")[:3]
    li = []
    for i in radios:
        n = model_to_dict(i)
        n.pop("radio_img", None)
        li.append(n)
    feed = dict(feed=li)
    return JsonResponse(feed)