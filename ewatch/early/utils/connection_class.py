#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from __future__ import unicode_literals
from __future__ import print_function

import re

# from early.utils.live_utils import _LV_Connect, PrefixOfGroup

# Para pruebas
from live_utils import _LV_Connect, PrefixOfGroup, LV_Execute, ServiceStateHist, HostWarningAndCriticalAlerts

class Group(object):
	"""Almacena el estado de un grupo, en base al análisis de los estados de los hosts contituyentes."""

	def __init__(self, groupname, lv_server, conn):
		super(Group, self).__init__()
		self.groupname = groupname
		self.state = 'OK'
		self.color = 'green'
		self.lv_server = lv_server
		self.conn = conn

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

	def __str__(self):
		return "%s %s %s" % (self.groupname, self.lv_server, self.conn)

	def __eq__(self, other): 
		return self.groupname == other.groupname

	def __ne__(self, other): 
		return self.groupname != other.groupname

	def __hash__(self): 
		return hash(self.groupname)

	def __cmp__(self, other):
		return cmp(self.groupname, other.groupname)

class Host(object):
	"""Almacena el estado de un host, en base al análisis de la alertas vía Livestatus."""

	def __init__(self, hostname):
		super(Host, self).__init__()
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
		self.cpu = self.check_service(conn, desc)

	def check_disk(self, conn):
		desc = 'Disk IO SUMMARY'
		self.disk = self.check_service(conn, desc)

	def check_memory(self, conn):
		desc = 'Memory'
		self.memory = self.check_service(conn, desc)

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


class Connection(object):
	"""
	Almacenará todo lo relativo a las conecciones.

	Esto es :
		- el set de ips para livestaus
		- un diccionario de key[prefijo de pais] value[ Group ]

	Aparte:

		lv_ip_set <--
		loaded <--
		diccionario_grupos <--


		- Group
			- nombre
			- estado
			debiera almacenar el set de Hosts contituyente
		- Host
			- nombre
			- estado
			- lv_ip_set

			....
		- en live_utils.py:def HostsGroup( conn, name_group ):
			retorna la lista de hosts asociados al name_group 
	"""

	def __init__(self ):
		super(Connection, self).__init__()
		self.lv_server_ip_set	= {	'172.17.29.175', '172.17.29.254','172.20.177.130', 
									'172.18.171.130', '172.18.171.189', '172.20.5.100', 
									'172.21.35.246',}
		self.lv_server_port		= 6557
		self.LoadDictionary()


	def LoadDictionary( self ):
		self.groups_dict	= dict()

		lql = "GET hostsbygroup\nColumns: custom_variable_values display_name"
		pattern = r'^.*CAPA_LOGICA\s+(\S+)\D+.*$'
		compiled_pattern = re.compile( pattern )

		for lv_server in self.lv_server_ip_set:
			conn = _LV_Connect( lv_server, self.lv_server_port )
			# print( lv_server )
			a_list = LV_Execute( conn, lql )

			for sublist in a_list:
				search = compiled_pattern.search( str( sublist ) )
				if search:
					group = Group( search.groups()[0], lv_server, conn )
					# print( group.groupname )
					country = PrefixOfGroup( group.groupname )
					if country:
						if country in self.groups_dict:
							key_set = self.groups_dict[ country ]
						else:
							key_set = set()
						key_set.add( group ) # ohhh sólo hay que insertar objetos que no tengan el mismo nombre ...
						self.groups_dict[ country ] = key_set

	def GetGroup( self, groupname ):
		'''
		Retorna Group o None, sino se encuentra un Group con nombre groupname
		'''
		for prefix in self.groups_dict:
			for group in self.groups_dict[ prefix ]:
				if groupname == group.groupname:
					return group

		return None


def ShowSetAsOrderedList( a_set ):
	a_list = sorted(list( a_set ))
	for elem in a_list:
		print( elem )


def main():
	connection = Connection() # It takes a 0m1.338s, to load it.

	for key in connection.groups_dict:
		print( "\n\n%s\n\n" % (key) )
		ShowSetAsOrderedList( connection.groups_dict[ key ] )

	group = raw_input("\nGRUPO_A_BUSCAR : ")

	print( "Grupo hallado[%s]" % (connection.GetGroup( group )))

if __name__ == '__main__':
	main()