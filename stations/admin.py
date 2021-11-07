from django.contrib import admin

from .models import RadioList
# Register your models here.

class RadioListAdmin(admin.ModelAdmin):
    list_display = ("radio_name", "radio_link",)

admin.site.register(RadioList, RadioListAdmin)
