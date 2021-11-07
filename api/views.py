from django.shortcuts import render
from django.http import JsonResponse
from django.forms import model_to_dict
import requests


from stations.models import RadioList, RadioHistory, RadioSession
# Create your views here.

def getRadios(request):
    radios = RadioList.objects.all()
    li = []
    for radio in radios:
        n = model_to_dict(radio)
        li.append(n)
    radio_feed = dict(feed=li)
    return JsonResponse(radio_feed)

def getCurrentPlaying(request, pk):
    radio = RadioList.objects.get(id=pk)
    r = requests.get(f"{radio.radio_link}currentsong?sid=1")
    cur = r.content.decode()
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
        new_record = RadioSession(name=cur, history=radio_history)
        new_record.save()
    
    data = dict(playing=cur)
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