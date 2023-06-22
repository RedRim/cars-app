from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from .forms import *

menu = [{'title': 'О Сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'addpage'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},
        ]


def index(request):
    posts = Cars.objects.all()
    #brands = Brands.objects.all()
    context = {
        'posts': posts,
        #'brands': brands,
        'menu': menu,
        'title': 'Главная страница',
        #'brand_selected': 0,
    }
    return render(request, 'cars/index.html', context=context)


def about(request):
    return render(request, 'cars/about.html', {'menu': menu, 'title': 'О сайте'})


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    return render(request, 'cars/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


def contact(request):
    return render(request, 'cars/contact.html', {'menu': menu, 'title': 'Обратная связь'})


def login(request):
    return render(request, 'cars/login.html', {'menu': menu, 'title': 'Вход'})


def show_post(request, post_id):
    post = get_object_or_404(Cars, pk=post_id)

    context = {
        'post': post,
        'menu': menu,
        'title': 'Главная страница',
        'brand_selected': post.brand_id,
    }

    return render(request, 'cats/post.html', context=context)


def show_brand(request, brand_id):
    posts = Cars.objects.filter(brand_id=brand_id)
    brands = Brands.objects.all()
    context = {
        'posts': posts,
        'brands': brands,
        'menu': menu,
        'title': 'Главная страница',
        'brand_selected': brand_id,
    }
    return render(request, 'cars/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
