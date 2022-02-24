from stations.models import AD_Zones

def management(request):
    try:
        options = AD_Zones.objects.get(access_name="admin")
    except:
        options = None
    return {
        'options': options,
       
    }