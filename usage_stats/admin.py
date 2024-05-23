from django.contrib import admin
from .models import HistoricalTopTechnologies, TechnologyCount

# Register your models here.
admin.site.register(HistoricalTopTechnologies)
admin.site.register(TechnologyCount)
