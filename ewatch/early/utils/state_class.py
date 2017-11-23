# -*- coding: iso-8859-15 -*-

from __future__ import unicode_literals
from __future__ import print_function

from early.utils.live_utils import ServiceStateHist, HostWarningAndCriticalAlerts

# ---------------------------------------------------------
class GroupState(object):
	"""Almacena el estado de un grupo, en base al análisis de los estados de los hosts contituyentes."""

	def __init__(self, groupname):
		super(GroupState, self).__init__()
		self.groupname = groupname
		self.state = 'OK'
		self.color = 'green'

	def check_host_state(self, host_state):
		if self.state == 'CRITICAL':
			self.color = 'red'
			return

		if  host_state == 'CRITICAL':
			self.state = 'CRITICAL'
			self.color = 'red'
			return

		if host_state == 'WARNING':
			self.state = 'WARNING'
			# self.color = 'yellow'
			self.color = '#cccc00'
			return

# ---------------------------------------------------------


class HostState(object):
	"""Almacena el estado de un host, en base al análisis de la alertas vía Livestatus."""

	def __init__(self, hostname):
		super(HostState, self).__init__()
		self.hostname = hostname
		self.state = 'OK'
		self.color = 'green'

	def check_service(self, conn, desc):
		a_list = ServiceStateHist( conn, self.hostname, desc )
		if len(a_list):
			a_list = a_list[0]
			info = "%s %.1f%% OK %.1f%% WARNING %.1f%% CRITICAL" % (desc, 100 * float(a_list[-3]), 100 * float(a_list[-2]), 100 * float(a_list[-1]))
		else:
			info = "No data"
		return info

	def check_cpu(self, conn):
		desc = 'CPU load'
		# self.cpu = self.check_service(conn, desc)

	def check_disk(self, conn):
		desc = 'Disk IO SUMMARY'
		# self.disk = self.check_service(conn, desc)

	def check_memory(self, conn):
		desc = 'Memory'
		# self.memory = self.check_service(conn, desc)

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

	def check_alerts(self, conn):
		alerts_to_process = HostWarningAndCriticalAlerts( conn, self.hostname )
		self.alerts = []
		for alert in alerts_to_process:
			alert_str = ' '.join( map( str,alert ) )
			self.alerts.append( alert_str )
			self.check_alert( alert_str )

	def check_state(self):
		return self.state

	def check_color(self):
		return self.color

	def __str__(self):
		return "%s: %s" % (self.hostname, self.state)