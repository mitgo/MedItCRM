from django.contrib import admin
from django.apps import apps

# Register your models here.

app_models = apps.get_app_config('ecp').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except Exception:
        pass

# class Persons(admin.ModelAdmin):
#     list_display = ('fam', 'im', 'ot', 'db', 'phone')
#     list_filter = ('fam', 'im', 'ot')
#
#     fieldsets = (
#         (None, {
#             'fields': ('fam', 'im')
#         }),
#         ('Availability', {
#             'fields': ('fam', 'db', 'phone')
#         }),
#     )