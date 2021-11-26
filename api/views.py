from django.shortcuts import render
from django.http import JsonResponse
from django.forms import model_to_dict
import requests


from stations.models import RadioList, RadioHistory, RadioSession, Category
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
        cur_req = f"https://theaudiodb.com/api/v1/json/523532/search.php?s={cur}"
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
            for i in h.radio_history_session.all()[:1]:
               
                n = model_to_dict(i)
                li.append(n)
        radio_history = dict(history=li)
        return JsonResponse(radio_history)
    return JsonResponse({"message" : "No Histroy Yet"})

def getRandomRadio(request):
    radio = RadioList.objects.order_by('?')[0]
    rad = dict(radio_id=radio.id, radio_name=radio.radio_name, link=radio.radio_link)
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