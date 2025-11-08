from django import forms
from .models import UserSolicitation
from django.utils.translation import gettext_lazy as _

class UserSolicitationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserSolicitationForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['policy_id'].queryset = user.user_policies.all()

    class Meta:
        model = UserSolicitation
        fields = [
            'title', 'description', 'policy_id', 'occurred_at', 'evidence_url', 
            'estimated_loss', 'claim_location', 'witnesses', 'police_report_number'
        ]
        
        base_attrs = {'class': 'form-control mb-3'}
        
        widgets = {
            'title': forms.TextInput(attrs={
                **base_attrs,
                'placeholder': _('Claim title...')
            }),
            'description': forms.Textarea(attrs={
                **base_attrs,
                'rows': 4,
                'placeholder': _('Describe what happened...')
            }),
            'policy_id': forms.Select(attrs={
                'class': 'form-select mb-3'
            }),
            'occurred_at': forms.DateTimeInput(attrs={
                **base_attrs,
                'type': 'datetime-local',
            }),
            'evidence_url': forms.URLInput(attrs={
                **base_attrs,
                'placeholder': _('https://example.com/photo.jpg')
            }),
            'estimated_loss': forms.NumberInput(attrs={
                **base_attrs,
                'step': '0.01',
                'placeholder': _('Estimated loss in USD')
            }),
            'claim_location': forms.TextInput(attrs={
                **base_attrs,
                'placeholder': _('Location of the incident')
            }),
            'witnesses': forms.Textarea(attrs={
                **base_attrs,
                'rows': 2,
                'placeholder': _('Names or contacts of witnesses')
            }),
            'police_report_number': forms.TextInput(attrs={
                **base_attrs,
                'placeholder': _('Police report number')
            }),
        }
