from django import forms
from django.contrib.auth.models import User
from client.models import Policy, UserPolicy, UserSolicitation
from django.core.exceptions import ValidationError

class UserPolicyForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    policy = forms.ModelChoiceField(queryset=Policy.objects.all(), empty_label="Select a policy")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise ValidationError("End date cannot be before start date.")
        return cleaned_data

class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'policy_number': forms.TextInput(attrs={'class': 'form-control'}),
            'policy_type': forms.Select(attrs={'class': 'form-control'}),
            'coverage_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'premium_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'monthly_payment': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AddPolicyToUserForm(forms.Form):
    policy = forms.ModelChoiceField(queryset=Policy.objects.all(), label="Select a policy")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Get policies already assigned to the user
            assigned_policies = UserPolicy.objects.filter(user_id=user).values_list('policy_id', flat=True)
            # Filter out policies already assigned
            self.fields['policy'].queryset = Policy.objects.exclude(id__in=assigned_policies)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise ValidationError("End date cannot be before start date.")
        return cleaned_data

class UserPolicyDatesForm(forms.ModelForm):
    class Meta:
        model = UserPolicy
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise ValidationError("End date cannot be before start date.")
        return cleaned_data
