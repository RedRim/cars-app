from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.inclusion_tag('cars/includes/post_item.html')
def post_item(post, oreintation):
    return {'post': post, 'oreintation': oreintation}
