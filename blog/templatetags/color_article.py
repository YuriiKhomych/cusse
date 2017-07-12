from django import template

register = template.Library()


def color(value):
    if "ao" in value:
        return "red"
    else:
        return "green"

register.filter("color", color)
