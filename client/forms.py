from django import forms
from .models import UserSolicitation
from django.utils import timezone

class UserSolicitationForm(forms.ModelForm):
    class Meta:
        model = UserSolicitation
        fields = ['title', 'description', 'occurred_at', 'evidence_url', 'estimated_loss']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Claim title...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'rows': 4,
                'placeholder': 'Describe what happened...'
            }),
            'occurred_at': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control mb-3'
            }),
            'evidence_url': forms.URLInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'https://example.com/photo.jpg'
            }),
            'estimated_loss': forms.NumberInput(attrs={
                'class': 'form-control mb-3',
                'step': '0.01',
                'placeholder': 'Estimated loss in USD'
            }),
        }
