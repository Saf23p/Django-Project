from django import template
import tfcargo.views as views
from tfcargo.models import Category, TagPost
from tfcargo.utils import menu

register = template.Library()

@register.simple_tag
def get_menu():
    return menu

@register.inclusion_tag('tfcargo/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('tfcargo/list_tags.html')
def show_all_tags():
    cats = Category.objects.all()
    return {'tags': TagPost.objects.all()}
