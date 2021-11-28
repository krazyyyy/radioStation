from django.shortcuts import render
from django.http import JsonResponse
from django.forms import model_to_dict
import requests
from bs4 import BeautifulSoup

from stations.models import RadioList, RadioHistory, RadioSession, Category, Countries, RssFeed
# Create your views here.

def getRadios(request):
    radios = RadioList.objects.all()
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
    r = requests.get(f"{radio.radio_link}currentsong?sid=1")
    cur = r.content.decode()

    try:
        imgg = cur.split("-")
        
        cur_req = f"https://theaudiodb.com/api/v1/json/523532/search.php?s={imgg[0][0:-1]}"

        im = requests.get(cur_req)
       

        cur_img = im.json()['artists'][0]['strArtistThumb']
    except:
        cur_img = ""
    if not request.session.exists(request.session.session_key):
        request.session.create()
    history = RadioHistory.objects.filter(session=request.session.session_key, radio=radio)
    if history.exists():
       radio_history = history[0]
    else:
        radio_history = RadioHistory(session=request.session.session_key, radio=radio)
        radio_history.save()
    allPlaying = RadioSession.objects.filter(name=cur, history=radio_history)
    if not allPlaying.exists():
        new_record = RadioSession(name=cur, img_link=cur_img, history=radio_history)
        new_record.save()
    
    data = dict(playing=cur, img=cur_img)
    return JsonResponse(data)

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

def getRandomRadio(request):
    radio = RadioList.objects.order_by('?')[0]
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
        url = requests.get(feed.rss_feed)
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
                    insert_list.append(RssFeed(title=i.title.text, link=i.link.text, source=feed.radio_name, pub_date=pub_, description=des))
                data['title'] = i.title.text
                data['link'] = i.link.text
  
                
                li.append(data)
            except:
                pass
    RssFeed.objects.bulk_create(insert_list)
    # feed = dict(feed=li)
    return JsonResponse({"message" : "success"})

def renderNews(request, pk):
    news = RssFeed.objects.filter(source=pk).order_by('-id')[:3]
    li = []
    for i in news:
        n = model_to_dict(i)
        li.append(n)
    feed = dict(feed=li)
    return JsonResponse(feed)