from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

def index(request):
    return HttpResponse("Главная страница cars")

def models(request, model):
    return HttpResponse(f"<h1>Статьи по моделям</h1><p>{model}")

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

