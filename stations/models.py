from django.db import models

# Create your models here.
class RadioList(models.Model):
    radio_name = models.CharField(max_length=200)
    radio_link = models.CharField(max_length=200, null=True, blank=True)
    radio_host = models.CharField(max_length=200, null=True, blank=True)

class RadioHistory(models.Model):
    session = models.CharField(max_length=200)
    radio = models.ForeignKey(RadioList, related_name="radio", on_delete=models.CASCADE)

class RadioSession(models.Model):
    name = models.CharField(max_length=200)
    history = models.ForeignKey('RadioHistory', related_name="radio_history_session", on_delete=models.CASCADE)