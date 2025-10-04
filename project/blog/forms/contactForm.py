from django import forms
from ..models.contact import Contact


class ContactForm(forms.ModelForm):
    CIVILITY_CHOICES = (
        ('M', 'Monsieur'),
        ('Mme', 'Madame'),
        ('Mlle', 'Mademoiselle'),
    )

    civility = forms.ChoiceField(choices=CIVILITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Contact
        fields = ('civility', 'name', 'email', 'subject', 'message', 'file')

        labels = {
            'civility': 'Civilité',
            'name': 'Nom',
            'email': 'Email',
            'subject': 'Objet',
            'message': 'Message',
            'file': 'Pièce jointe',
        }

        error_messages = {
            'civility': {
                'required': 'La civilité est obligatoire.',
            },
            'name': {
                'required': 'Le nom est obligatoire.',
                'max_length': 'Le nom ne peut pas dépasser 100 caractères.',
            },
            'email': {
                'required': 'L\'email est obligatoire.',
                'invalid': 'Veuillez entrer une adresse email valide.',
            },
            'subject': {
                'required': 'L\'objet est obligatoire.',
                'max_length': 'L\'objet ne peut pas dépasser 200 caractères.',
            },
            'message': {
                'required': 'Le message est obligatoire.',
            },
        }

        widgets = {
            'civility': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.com'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Objet de votre message'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Votre message...'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }