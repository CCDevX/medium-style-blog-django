from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        # Configuration username
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Votre nom d\'utilisateur'
        })
        self.fields['username'].label = 'Nom d\'utilisateur'

        # Configuration password
        self.fields['password'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Votre mot de passe'
        })
        self.fields['password'].label = 'Mot de passe'

        # Messages d'erreur personnalisés
        self.fields['username'].error_messages = {
            'required': 'Le nom d\'utilisateur est obligatoire.',
        }

        self.fields['password'].error_messages = {
            'required': 'Le mot de passe est obligatoire.',
        }

    error_messages = {
        'invalid_login': 'Nom d\'utilisateur ou mot de passe incorrect.',
        'inactive': 'Ce compte est inactif.',
    }