from django import forms
from ..models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'categories', 'tags', 'is_published', 'image')

        labels = {
            'title': 'Titre',
            'content': 'Contenu',
            'categories': 'Catégorie',
            'tags': 'Tags',
            'is_published': 'Publier l\'article',
            'image': 'Illustration',
        }

        error_messages = {
            'title': {
                'required': 'Le titre est obligatoire.',
                'max_length': 'Le titre ne peut pas dépasser 60 caractères.',
            },
            'content': {
                'required': 'Le contenu est obligatoire.',
            },
            'categories': {
                'required': 'La catégorie est obligatoire.',
            },
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de votre article'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Écrivez votre article ici...'
            }),
            'categories': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }