from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.apps import apps

# Register your models here.

# class UserAdmin(admin.ModelAdmin):
#     model = User

models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except:
        pass