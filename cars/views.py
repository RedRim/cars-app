from typing import Any, Dict
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView


from .models import *
from .forms import *

menu = [{'title': 'О Сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'addpage'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},
        ]

class CarsHome(ListView):
    model = Cars
    template_name = "cars/index.html"
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        # context['cat_selected'] = 0
        return context
    
    def get_queryset(self):
        return Cars.objects.filter(is_published=True)


# def index(request):
#     posts = Cars.objects.all()
#     # brands = Brands.objects.all()
#     context = {
#         'posts': posts,
#         # 'brands': brands,
#         'menu': menu,
#         'title': 'Главная страница',
#         #'brand_selected': 0,
#     }
#     return render(request, 'cars/index.html', context=context)

class AddPage(CreateView):
    form_class = AddPostForm
    template_name = "cars/post.html"

    def get_context_data(self, *, object_list=None, **kwargs):
         context = super().get_context_data(**kwargs)
         context['title'] = 'Добавление статьи'
         context['menu'] = menu
         return context

# def add_page(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         else:
#             form = AddPostForm()
#     return render(request, 'cars/addpage.html', {'menu': menu, 'title': 'Добавление статьи'})

class ShowPost(DetailView):
    model = Cars
    template_name = "cars/post.html"
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context

# def show_post(request, post_id):
#     post = get_object_or_404(Cars, pk=post_id)

#     context = {
#         'post': post,
#         'menu': menu,
#         'title': 'Главная страница',
#         'brand_selected': post.brand_id,
#     }

#     return render(request, 'cats/post.html', context=context)

class CarsBrand(ListView):
    model = Cars
    template_name = "cars/index.html"
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Фирма - ' + str(context['posts'][0].brand)
        # context['cat_selected'] = context['posts'][0].brand_id
        return context
    
    def get_queryset(self):
        return Cars.objects.filter(brand__slug=self.kwargs['brand_slug'], is_published=True)

# def show_brand(request, brand_id):
#     posts = Cars.objects.filter(brand_id=brand_id)
#     brands = Brands.objects.all()
#     context = {
#         'posts': posts,
#         'brands': brands,
#         'menu': menu,
#         'title': 'Главная страница',
#         'brand_selected': brand_id,
#     }
#     return render(request, 'cars/index.html', context=context)

def contact(request):
    return render(request, 'cars/contact.html', {'menu': menu, 'title': 'Обратная связь'})

def login(request):
    return render(request, 'cars/login.html', {'menu': menu, 'title': 'Вход'})

def about(request):
    return render(request, 'cars/about.html', {'menu': menu, 'title': 'О сайте'})

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
