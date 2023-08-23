from django import template

register = template.Library()

@register.inclusion_tag('account/includes/subscribe_button.html')
def subscribe_button(request, user_to):
    return {'request': request, 'user': user_to}

