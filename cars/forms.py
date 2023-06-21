from django import forms
from django.core.exceptions import ValidationError

from .models import *

class AddPostForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].empty_label = "Марка не выбрана"

    class Meta:
        model = Cars
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'brand']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 слов')
        
        return title