from django import template

register = template.Library()

@register.simple_tag
def get_order_status_icon(status):
    icons = {
        'pending': 'bi-hourglass-split',
        'processing': 'bi-gear-wide-connected',
        'shipped': 'bi-truck',
        'completed': 'bi-check2-circle',
        'canceled': 'bi-x-circle'
    }
    return icons.get(status, 'bi-question-circle')