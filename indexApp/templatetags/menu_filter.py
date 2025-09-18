from atexit import register
from django import template
from indexApp.models import Menu

register = template.Library()

@register.filter
def menu_filter(request):
    menus = Menu.objects.filter(parent=None)
    return menus