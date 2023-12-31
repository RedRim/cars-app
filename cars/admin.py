from django.contrib import admin

from .models import *

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'time_create', 'time_update', 'photo', 'author', 'is_published')
  list_display_links = ('id', 'title')
  #Атрибуты, по которым можно фильтровать в админке (справа)
  list_filter = ['is_published', 'time_create']
  search_fields = ('title', 'content')
  prepopulated_fields = {"slug": ('title',)}
  #Добавляет ссылки для навигации по иерархии дат.
  date_hierarchy = 'time_create'
  #Выбор автора по id (с возможностью поиска)
  raw_id_fields = ['author']

@admin.register(Brands)
class BrandAdmin(admin.ModelAdmin):
  list_display = ('id', 'name')
  list_display_links = ('id', 'name')
  search_fields = ('name',)
  prepopulated_fields = {"slug": ('name',)}

@admin.register(FeedbackMessage)
class FeedbackMessageAdmin(admin.ModelAdmin):
  list_display = ('id', 'author', 'short_content', 'content')
  list_display_links = ('id', 'author')
  search_fields = ('short_conent', 'auhtor')

@admin.register(Comment)
class ComentAdmin(admin.ModelAdmin):
  list_display = ('id', 'time_create', 'content')