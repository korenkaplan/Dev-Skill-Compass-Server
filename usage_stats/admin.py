from django.contrib import admin
from .models import HistoricalTechCounts, MonthlyTechnologiesCounts, AggregatedTechCounts

# Register your models here.
admin.site.register(HistoricalTechCounts)
admin.site.register(MonthlyTechnologiesCounts)
admin.site.register(AggregatedTechCounts)
