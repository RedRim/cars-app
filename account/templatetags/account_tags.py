from django import template

register = template.Library()

@register.inclusion_tag('account/includes/subscribe_button.html')
def subscribe_button(user_to):
    return {'user': user_to}

