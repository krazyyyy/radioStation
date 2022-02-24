from django.contrib import admin

from .models import RadioList, Countries, Category, Genre, RssFeed, AD_Zones
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
    list_display = ("radio_name", "radio_link", "country",)
    inlines = [InLineCategory, InLineGenre]

admin.site.register(RadioList, RadioListAdmin)

class CountriesAdmin(admin.ModelAdmin):
    search_fields = ("country_name",)



def addWinId(modeladmin, request, queryset):
    for query in queryset:
        query.country = query.source_id.country
        
        query.save()

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'source',)
    search_fields = ['title', 'source',]
    actions = [addWinId]
    class Meta:
        verbose_name_plural = "News"

admin.site.register(Countries, CountriesAdmin)
admin.site.register(RssFeed, NewsAdmin)
admin.site.register(AD_Zones)

