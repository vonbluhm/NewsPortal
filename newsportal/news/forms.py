from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'type',
            'categories',
            'header',
            'text',
            'postAuthor',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        header = cleaned_data.get('header')
        if text == header:
            raise ValidationError(
                "Title and text cannot be identical"
            )
        return cleaned_data
