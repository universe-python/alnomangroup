from atexit import register
from django import template

register = template.Library()


@register.filter
def zero_counter(value):
    return f"{value:02}"
