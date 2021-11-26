from django.shortcuts import render

from stations.models import RadioList

# Create your views here.
def index(requests):
    return render(requests, 'frontend/index.html')

def genrePage(requests, pk):
    return render(requests, 'frontend/genre.html', {
        "main" : pk
    })

def radioPage(requests, pk):
    radio = RadioList.objects.get(id=pk)
    return render(requests, 'frontend/radio.html', {
        "radio" : radio
    })