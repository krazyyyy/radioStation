from django.db import models

# Create your models here.
class Countries(models.Model):
    country_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.country_name}"

class RadioList(models.Model):
    radio_name = models.CharField(max_length=200)
    radio_link = models.CharField(max_length=200, null=True, blank=True)
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
    history = models.ForeignKey('RadioHistory', related_name="radio_history_session", on_delete=models.CASCADE)