from django.db import models

# Create your models here.
class Countries(models.Model):
    country_name = models.CharField(max_length=200)
    country_flag = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.country_name}"

class RadioList(models.Model):
    radio_name = models.CharField(max_length=200)
    radio_link = models.CharField(max_length=200, null=True, blank=True)
    play_link = models.CharField(max_length=200, null=True, blank=True)
    rss_feed = models.CharField(max_length=200, null=True, blank=True)
    radio_img = models.ImageField(upload_to="radiobanner", null=True, blank=True)
    country = models.ForeignKey('Countries', on_delete=models.CASCADE, related_name="radio_country", null=True, blank=True)

class Genre(models.Model):
    genre = models.CharField(max_length=200)
    radio = models.ForeignKey('RadioList', on_delete=models.CASCADE, related_name="radio_genre")

class Category(models.Model):
    category = models.CharField(max_length=200)
    radio = models.ForeignKey('RadioList', on_delete=models.CASCADE, related_name="radio_category")

class RadioHistory(models.Model):
    session = models.CharField(max_length=200)
    radio = models.ForeignKey(RadioList, related_name="radio", on_delete=models.CASCADE)

class RadioSession(models.Model):
    name = models.CharField(max_length=200)
    img_link = models.CharField(max_length=200, null=True, blank=True)
    history = models.ForeignKey('RadioHistory', related_name="radio_history_session", on_delete=models.CASCADE)

class RssFeed(models.Model):
    source = models.CharField(max_length=200)
    link = models.CharField(max_length=500)
    title = models.CharField(max_length=200)
    pub_date = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)