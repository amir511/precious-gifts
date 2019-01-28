from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_website_name():
    return settings.WEBSITE_NAME

@register.inclusion_tag('custom_tags/bootstrap.html')
def get_bootstrap():
    theme = settings.BOOTSTRAP_THEME
    return {'theme':theme}