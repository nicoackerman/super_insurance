from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def get_home_url(context):
    user = context['request'].user
    if user.is_authenticated:
        if user.is_superuser:
            return reverse('company:home')
        else:
            return reverse('client:home')
    return reverse('home')
