from .models import CustomUser, Follow

from django.contrib import admin
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('slug', 'first_name', 'last_name', 'is_moder')
    list_display_links = ('slug',)
    search_fields = ('login', 'first_name', 'last_name')

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user_from', 'user_to', 'created')
