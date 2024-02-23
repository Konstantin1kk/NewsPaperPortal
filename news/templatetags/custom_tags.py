from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    current_param = context['request'].GET.copy()
    for k, v in kwargs.items():
        current_param[k] = v
    return current_param.urlencode()
