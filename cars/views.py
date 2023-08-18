from .utils import *
from .forms import *
from .models import *
from account.models import CustomUser

from typing import Any, Dict
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.core.paginator import Paginator

class CarsHome(DataMixin, ListView):
    model = Post
    template_name = 'cars/index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        brands = Brands.objects.all()
        authors = CustomUser.objects.all()
        context['brands'] = brands
        context['authors'] = authors
        brand_filter = self.request.GET.get('brand')
        sort_filter = self.request.GET.get('sort')
        author_filter = self.request.GET.get('author')
        context['brand_filter'] = brand_filter if brand_filter else ''
        context['sort_filter'] = sort_filter if sort_filter else ''
        context['author_filter'] = author_filter if author_filter else ''           

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        queryset = super().get_queryset()

        brand_slug = self.request.GET.get('brand')
        if brand_slug:
            queryset = queryset.filter(brand__slug=brand_slug)
        
        queryset = queryset.filter(is_published=True)
        sort = self.request.GET.get('sort')
        if sort == 'latest':
            queryset = queryset.order_by('-time_create')  # Сортировка по новизне
        elif sort == 'oldest':
            queryset = queryset.order_by('time_create')  # Сортировка по старым

        author_slug = self.request.GET.get('author')
        if author_slug:
            queryset = queryset.filter(author__slug=author_slug)

        return queryset


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
    model = Post
    template_name = "cars/post.html"
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    
    @require_POST
    def image_like(request):
        post_slug = request.POST.get('post_slug')
        action = request.POST.get('action')
        if post_slug and action:
            try:
                post = Post.objects.get(slug=post_slug)
                if action == 'like':
                    post.users_like.add(request.user)
                else:
                    post.users_like.remove(request.user)
                return JsonResponse({'status': 'ok'})
            except Post.DoesNotExist:
                pass
        return JsonResponse({'status': 'error'})

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'].title, form=AddCommentForm, comments=Comment.objects.filter(post__slug=context['post'].slug))
        return dict(list(context.items()) + list(c_def.items()))

class CarsBrand(DataMixin, ListView):
    model = Post
    template_name = "cars/index.html"
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Категория - " + str(context['posts'][0].brand),
                                      brand_selected=context['posts'][0].brand_id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Post.objects.filter(brand__slug=self.kwargs['brand_slug'], is_published=True)

class Modering(DataMixin, ListView):
    model = Post
    template_name = "cars/moder.html"
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Проверка статей")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Post.objects.filter(is_published=False)

def toggle_is_published(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    post.is_published = True
    post.save()
    return redirect('post', post_slug=post.slug)

@require_POST
def create_comment(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, is_published=True)
    form = AddCommentForm(request.POST)
    if form.is_valid():
        form.instance.author = request.user
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect('post', post_slug=post.slug)
    return redirect('post', post_slug=post.slug)

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

def about(request):
    return render(request, 'cars/about.html', {'menu': menu, 'title': 'О сайте'})

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")