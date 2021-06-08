from django import forms
from django.forms.models import ModelForm

from .models import Comment, Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group', 'image']

    def clean_text(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError('Впишите текст!')
        return data


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
