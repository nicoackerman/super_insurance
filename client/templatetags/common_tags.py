from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def get_home_url(context):
    user = context['request'].user
    if user.is_authenticated and user.is_superuser:
        return reverse('company:home')
    return reverse('client:home')

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
