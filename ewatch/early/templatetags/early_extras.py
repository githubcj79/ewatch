from django import template

register = template.Library()

@register.filter
def lookup(d, key):
    return d[key]

# ----------------------------

@register.filter
def alert_color( str_alert ):

	if 'CRITICAL' in str_alert:
		return '#F2D3D6'
	elif 'WARNING' in str_alert:
		return '#F5F5E6'
	else:
		return '#C6E0C5'

