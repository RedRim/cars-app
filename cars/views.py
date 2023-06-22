from typing import Any, Dict
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin


from .models import *
from .forms import *
from .utils import *

class CarsHome(DataMixin, ListView):
    model = Cars
    template_name = "cars/index.html"
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_queryset(self):
        return Cars.objects.filter(is_published=True)
    

class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "cars/addpage.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))
    

# class ShowPost(DetailView):
#     model = Cars
#     template_name = "cars/post.html"
#     slug_url_kwarg = 'post_slug'
#     context_object_name = 'post'

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title=context['post'])
#         return dict(list(context.items()) + list(c_def.items()))

class CarsBrand(ListView):
    model = Cars
    template_name = "cars/index.html"
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Категория - " + str(context['posts'][0].brand),
                                      brand_selected=context['posts'][0].brand_id)
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_queryset(self):
        return Cars.objects.filter(brand__slug=self.kwargs['brand_slug'], is_published=True)
    

def contact(request):
    return render(request, 'cars/contact.html', {'menu': menu, 'title': 'Обратная связь'})

def login(request):
    return render(request, 'cars/login.html', {'menu': menu, 'title': 'Вход'})

def about(request):
    return render(request, 'cars/about.html', {'menu': menu, 'title': 'О сайте'})

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
