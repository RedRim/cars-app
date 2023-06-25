from .models import *

menu = [{'title': 'О Сайте', 'url_name': 'about'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        ]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        brands = Brands.objects.all()
        context['menu'] = menu
        context['brands'] = brands
        if 'brand_selected' not in kwargs:
            context['brand_selected'] = 0
        return context
    
