from django import template
# Вверх по дереву папок
from ..models import CustomUser
from django.utils.safestring import mark_safe
from django.db.models import Count

register = template.Library()

@register.simple_tag
def get_all_users():
    return CustomUser.objects.all()