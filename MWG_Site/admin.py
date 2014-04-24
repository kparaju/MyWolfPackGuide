from django.contrib import admin
from MWG_Site import models

# Register your models here.
admin.site.register(models.MWGUser)
admin.site.register(models.MWGAdmin)
admin.site.register(models.Event)
admin.site.register(models.Address)


