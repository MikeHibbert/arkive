from django import template

register = template.Library()


@register.filter(name='addcss')
def addcss(value, arg):
    css_classes = value.field.widget.attrs.get('class', '').split(' ')
    if css_classes and arg not in css_classes:
        css_classes = '%s %s' % (" ".join(css_classes), arg)
    return value.as_widget(attrs={'class': css_classes})


@register.filter(name='to_comma_separated_string')
def to_comma_separated_string(value):
    output = ", ".join(value)

    return output