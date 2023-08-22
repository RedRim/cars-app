from .models import Post, FeedbackMessage, Comment

from django import forms
from django.core.exceptions import ValidationError

class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].empty_label = "Марка не выбрана"

    class Meta:
        model = Post
        fields = ['title', 'short_content', 'content', 'photo', 'brand']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 75 символов')
        return title

class FeedbackMessageForm(forms.ModelForm):
    class Meta:
        model = FeedbackMessage
        fields = ['short_content', 'content']
        widgets = {
            'short_content': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }