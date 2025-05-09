from django import template
register = template.Library()

@register.filter
def status_color(order):
    return order.status_color