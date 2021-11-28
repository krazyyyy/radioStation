from django.contrib import admin

from .models import RadioList, Countries, Category, Genre, RssFeed
# Register your models here.

class InLineCategory(admin.StackedInline):
    model = Category
    classes = ['collapse']
    extra = 0

class InLineGenre(admin.StackedInline):
    model = Genre
    classes = ['collapse']
    extra = 0

class RadioListAdmin(admin.ModelAdmin):
    list_display = ("radio_name", "radio_link",)
    inlines = [InLineCategory, InLineGenre]

admin.site.register(RadioList, RadioListAdmin)

class CountriesAdmin(admin.ModelAdmin):
    search_fields = ("country_name",)

admin.site.register(Countries, CountriesAdmin)
admin.site.register(RssFeed)
