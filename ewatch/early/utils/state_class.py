# -*- coding: iso-8859-15 -*-

from __future__ import unicode_literals
from __future__ import print_function

class HostState(object):
	"""Almacena el estado de un host, en base al análisis de la alertas vía Livestatus."""

	state_list = [ 'OK', 'WARNING', 'CRITICAL' ]

	def __init__(self, hostname):
		super(HostState, self).__init__()
		self.hostname = hostname
		self.state = 'OK'
		self.color = 'green'

	def check_alert(self, str_alert):
		if self.state == 'CRITICAL':
			self.color = 'red'
			return

		if 'CRITICAL' in str_alert:
			self.state = 'CRITICAL'
			self.color = 'red'
			return

		if 'WARNING' in str_alert:
			self.state = 'WARNING'
			# self.color = 'yellow'
			self.color = '#cccc00'
			return

	def check_state(self):
		return self.state

	def check_color(self):
		return self.color

	def __str__(self):
		return "%s: %s" % (self.hostname, self.state)