from cars.models import Post
from .forms import *
from cars.utils import DataMixin

from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'account/register.html'
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


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

class EditProfile(DataMixin, LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = EditProfileForm
    template_name = 'account/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = EditProfileForm(instance=self.request.user)
        c_def = self.get_user_context(title="Редактирование профиля", form=form)
        context.update(c_def)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.photo = self.request.FILES.get('photo')
        self.object = form.save()
        
        return response
    
class EditPassword(LoginRequiredMixin, FormView):
    template_name = 'account/edit_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return super().form_valid(form)
    
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'account/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_success_url(self):
        return reverse_lazy('home')
    
class Profile(DataMixin, ListView):
    model = Post
    template_name = "account/profile.html"
    context_object_name = 'posts'
    # slug_url_kwarg = 'profile_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.get(slug=self.kwargs['profile_slug'])
        if not self.object_list:
            context['empty_message'] = "Список статей пуст"
            author = f"{user.first_name} {user.last_name}"
        else:
            author = f"{user.first_name} {user.last_name}"
        c_def = self.get_user_context(title=author)
        context.update(c_def)
        return context
    
    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.slug == self.kwargs['profile_slug']:
            return Post.objects.filter(author__slug=self.kwargs['profile_slug'])
        return Post.objects.filter(author__slug=self.kwargs['profile_slug'], is_published=True)

class AuthorsList(DataMixin, ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name = "account/authors_list.html"
    paginate_by = 20

    def get_queryset(self):
        if(self.request.user.is_authenticated):
            return CustomUser.objects.all().exclude(slug=self.request.user.slug)
        return CustomUser.objects.all()
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторы')
        return dict(list(context.items()) + list(c_def.items()))

@login_required
def follow_user(request):
    user_slug = request.POST.get('user_slug')
    action = request.POST.get('action')
    if user_slug and action:
        try:
            post = CustomUser.objects.get(slug=user_slug)
            if action == 'follow':
                post.followers.add(request.user)
            else:
                post.followers.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except CustomUser.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


def logout_user(request):
    logout(request)
    return redirect('login')

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")