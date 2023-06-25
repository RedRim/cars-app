from .utils import *
from .forms import *
from .models import *

from typing import Any, Dict
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin


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

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))

class ShowPost(DataMixin, DetailView):
    model = Cars
    template_name = "cars/post.html"
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

class CarsBrand(DataMixin, ListView):
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

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'cars/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.photo = self.request.FILES.get('photo')
        user = form.save()
        login(self.request, user)
        return redirect('home')
    
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'cars/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_success_url(self):
        return reverse_lazy('home')
    
class Profile(DataMixin, ListView):
    model = Cars
    template_name = "cars/profile.html"
    context_object_name = 'posts'
    slug_url_kwarg = 'profile_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        author = f"{self.object_list.first().author.last_name} {self.object_list.first().author.first_name}"
        c_def = self.get_user_context(title=author)
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_queryset(self):
        if self.request.user.slug == self.kwargs['profile_slug']:
            return Cars.objects.filter(author__slug=self.kwargs['profile_slug'])
        return Cars.objects.filter(author__slug=self.kwargs['profile_slug'], is_published=True)
    
class Modering(DataMixin, ListView):
    model = Cars
    template_name = "cars/moder.html"
    context_object_name = 'posts'
    slug_url_kwarg = 'moder_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Проверка статей")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Cars.objects.filter(author__slug=self.kwargs['profile_slug'], is_published=False)

def logout_user(request):
    logout(request)
    return redirect('login')

def contact(request):
    if (request.method == 'POST'):
        form = FeedbackMessageForm(request.POST)
        if form.is_valid():
            try:
                form.instance.author = request.user
                form.save()
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = FeedbackMessageForm()
    return render(request, 'cars/contact.html', {'form': form, 'menu': menu, 'title': 'Обратная связь'})

def add_like(request, post_slug):
    post = get_object_or_404(Cars, slug=post_slug)
    post.likes_amount += 1
    post.save()
    return redirect('post', post_slug=post.slug)

def about(request):
    return render(request, 'cars/about.html', {'menu': menu, 'title': 'О сайте'})

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
