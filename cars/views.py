from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from .models import Cars

menu = [{'title': 'О Сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},
        ]


def index(request):
    posts = Cars.objects.all()
    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Главная страница'
    }
    # return render(request, 'cars/index.html', context=context)
    return HttpResponse("Главная страница")


def about(request):
    # return render(request, 'cars/about.html', {'menu': menu, 'title': 'О сайте'})
    return HttpResponse("О сайте")


def add_page(request):
    return HttpResponse("Тут пользователь может добавить статью")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Тут логинятся")

def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
