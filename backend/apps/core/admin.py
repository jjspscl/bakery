from .models import *
from django.contrib import admin
from django.apps import apps
models = apps.get_models()
excepts = ['Permission', 'Group', 'User',
           'LogEntry', 'ContentType', 'Session', ]


@admin.register(pastry.Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(pastry.Pastry)
class PastryAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(pastry.PastryIngredient)
class PastryIngredientAdmin(admin.ModelAdmin):
    list_display = ('id',)
