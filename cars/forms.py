from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser, Cars, FeedbackMessage


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].empty_label = "Марка не выбрана"

    class Meta:
        model = Cars
        fields = ['title', 'short_content', 'content', 'photo', 'brand']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 слов')
        return title
    
class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    photo = forms.ImageField(label='Фото', required=False)

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'photo')
        model = CustomUser

class EditProfileForm(forms.ModelForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Повторите новый пароль', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'photo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class FeedbackMessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.fields['password'].widget.attrs.update({
        'autocomplete': 'new-password'
        })
        super().__init__(*args, **kwargs)

    class Meta:
        model = FeedbackMessage
        fields = ['short_content', 'content']
        widgets = {
            'short_content': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }
