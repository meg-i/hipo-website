from django.contrib import admin
from .models import Recipe, Ingredient
from django_admin_favorite_filters.mixins import FavoriteFilterMixin
from django_admin_favorite_filters.filters import FavoriteFiltersFilter
# Register your models here.


class RecipeAdmin(FavoriteFilterMixin, admin.ModelAdmin):
    fields = ['name', 'image', 'ingredients', 'description', 'difficulty']
    list_filter = (FavoriteFiltersFilter, 'name')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
