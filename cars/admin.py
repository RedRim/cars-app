from django.contrib import admin

from .models import *

class CarsAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'time_create', 'photo', 'author','is_published')
  list_display_links = ('id', 'title')
  search_fields = ('title', 'content')
  prepopulated_fields = {"slug": ('title',)}

class BrandAdmin(admin.ModelAdmin):
  list_display = ('id', 'name')
  list_display_links = ('id', 'name')
  search_fields = ('name',)
  prepopulated_fields = {"slug": ('name',)}

class FeedbackMessageAdmin(admin.ModelAdmin):
  list_display = ('id', 'author', 'short_content', 'content')
  list_display_links = ('id', 'author')
  search_fields = ('short_conent', 'auhtor')
  
admin.site.register(Cars, CarsAdmin)
admin.site.register(Brands, BrandAdmin)
admin.site.register(CustomUser)
admin.site.register(FeedbackMessage, FeedbackMessageAdmin)
