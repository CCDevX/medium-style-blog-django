from django import forms
from blog.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'description')

        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Email',
            'description': 'Biographie',
        }

        error_messages = {
            'first_name': {
                'max_length': 'Le prénom ne peut pas dépasser 100 caractères.',
            },
            'last_name': {
                'max_length': 'Le nom ne peut pas dépasser 100 caractères.',
            },
            'email': {
                'invalid': 'Veuillez entrer une adresse email valide.',
            },
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Votre prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Votre nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'votre@email.com'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'rows': 6,
                'placeholder': 'Parlez-nous de vous...'
            }),
        }