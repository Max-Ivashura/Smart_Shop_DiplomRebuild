# apps/accounts/templatetags/phone_filters.py
from django import template

register = template.Library()

@register.filter(name='phone_format')  # Явное указание имени
def phone_format(value):
    if not value:
        return value
    numbers = ''.join(filter(str.isdigit, str(value)))
    if len(numbers) == 11:
        return f'+7 ({numbers[1:4]}) {numbers[4:7]}-{numbers[7:9]}-{numbers[9:11]}'
    return value