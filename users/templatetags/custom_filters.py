from django import template

register = template.Library()

@register.filter
def get(dictionary, key):
    """Custom filter to retrieve a value from a dictionary by key."""
    return dictionary.get(key)
@register.filter
def times(value, arg):
    return value * arg