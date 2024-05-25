from django.contrib import admin
from .models import HistoricalTopTechnologies, TechnologiesCounts

# Register your models here.
admin.site.register(HistoricalTopTechnologies)
admin.site.register(TechnologiesCounts)
