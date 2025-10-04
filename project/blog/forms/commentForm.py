from django import forms
from ..models.comment import Comment


class CommentForm(forms.ModelForm):
    NOTE_CHOICES = (
        (1, '1 étoile'),
        (2, '2 étoiles'),
        (3, '3 étoiles'),
        (4, '4 étoiles'),
        (5, '5 étoiles'),
    )

    note = forms.ChoiceField(
        choices=NOTE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Note'
    )

    class Meta:
        model = Comment
        fields = ('note', 'content')

        labels = {
            'note': 'Note',
            'content': 'Votre commentaire',
        }

        error_messages = {
            'note': {
                'required': 'La note est obligatoire.',
            },
            'content': {
                'required': 'Le commentaire est obligatoire.',
            },
        }

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Partagez votre avis...'
            }),
        }