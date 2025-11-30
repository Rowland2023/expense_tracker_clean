from django import template
register = template.Library()

@register.filter
def pluck(queryset, key):
    return [row[key] for row in queryset]
