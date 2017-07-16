from django import template

register = template.Library()

def rating(value):
    if value < 10:
        return "Hot"
    elif value > 50:
        return "Best"
    else:
        return "Popular"

register.filter('rating', rating)
