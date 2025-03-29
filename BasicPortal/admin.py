from django.apps import apps
from django.contrib import admin


# Register your models here.

BasicPortal = apps.get_app_config('BasicPortal').get_models()

for model in BasicPortal:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
