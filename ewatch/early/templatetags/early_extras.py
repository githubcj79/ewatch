from django import template

register = template.Library()

@register.filter
def lookup(d, key):
    return d[key]

# ----------------------------

@register.filter
def alert_color( str_alert ):

	if 'CRITICAL' in str_alert:
		return 'red'
	elif 'WARNING' in str_alert:
		return '#cccc00'
	else:
		return 'green'

