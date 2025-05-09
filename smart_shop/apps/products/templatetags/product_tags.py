from django import template
from django.utils.html import escape, mark_safe

register = template.Library()


@register.filter
def highlight(text, query):
    if not query:
        return text
    highlighted = escape(text).replace(
        escape(query),
        f'<span class="highlight">{escape(query)}</span>'
    )
    return mark_safe(highlighted)
