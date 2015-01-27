from django import template

register = template.Library()

@register.filter
def field_verbose_name(cls, field):
	return cls._meta.get_field(field).verbose_name

@register.filter
def field_value(model, field):
	if hasattr(model, field):
		return getattr(model, field)
	return ''