from django.contrib import admin
from .models import HistoricalTechCounts, MonthlyTechnologiesCounts

# Register your models here.
admin.site.register(HistoricalTechCounts)
admin.site.register(MonthlyTechnologiesCounts)
