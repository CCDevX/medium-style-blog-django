from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'votre@email.com'
        }),
        label='Email'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nom d\'utilisateur ',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Votre nom d\'utilisateur '
            }),
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        # --- Password 1
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Minimum 8 caractères '
        })
        self.fields['password1'].label = 'Mot de passe '
        self.fields['password1'].help_text = None
        self.fields['password1'].error_messages = {
            'required': 'Le mot de passe est obligatoire. ',
        }

        # --- Password 2
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Confirmez votre mot de passe '
        })
        self.fields['password2'].label = 'Confirmation du mot de passe '
        self.fields['password2'].help_text = None
        self.fields['password2'].error_messages = {
            'required': 'La confirmation du mot de passe est obligatoire. ',
            'password_mismatch': 'Les deux mots de passe ne correspondent pas. ',
        }

        # --- Username
        self.fields['username'].error_messages = {
            'required': 'Le nom d\'utilisateur est obligatoire. ',
            'unique': 'Ce nom d\'utilisateur est déjà utilisé. ',
            'invalid': 'Ce nom d\'utilisateur contient des caractères non autorisés. ',
            'max_length': 'Le nom d\'utilisateur est trop long. ',
        }

        # --- Email
        self.fields['email'].error_messages = {
            'required': 'L\'email est obligatoire. ',
            'invalid': 'Veuillez entrer une adresse email valide. ',
            'unique': 'Cet email est déjà utilisé. ',
        }

    # ✅ Validation personnalisée pour les messages “trop courant” et “numérique”
    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        try:
            validate_password(password)
        except ValidationError as e:
            messages = []
            for msg in e.messages:
                if "too common" in msg.lower():
                    messages.append("Ce mot de passe est trop courant. ")
                elif "entirely numeric" in msg.lower():
                    messages.append("Le mot de passe ne peut pas être uniquement numérique. ")
                else:
                    messages.append(msg)
            raise ValidationError(messages)

        return password
