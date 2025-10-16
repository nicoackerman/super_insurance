from django import forms
from django.contrib.auth.models import User
from client.models import Policy

class UserPolicyForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    policy = forms.ModelChoiceField(queryset=Policy.objects.all(), empty_label="Select a policy")
