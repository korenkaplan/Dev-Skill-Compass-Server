from django.contrib import admin
from .models import Technologies, Roles, Categories, Synonyms, RoleListingsCount

# Register your models here.
admin.site.register(Technologies)
admin.site.register(Roles)
admin.site.register(Categories)
admin.site.register(Synonyms)
admin.site.register(RoleListingsCount)
