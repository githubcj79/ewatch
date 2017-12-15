#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from __future__ import unicode_literals
from __future__ import print_function

import re

from live_utils import _LV_Connect, LV_Execute, PrefixOfGroup

class Country(object):
	'''Almacena en un diccionario los grupos del pais'''

	def __init__(self, countryname):
		super(Country, self).__init__()
		self.countryname = countryname
		self.group_dict	= dict()

	def __str__(self):
		return "%s" % (self.countryname)

	'''
	def __eq__(self, other): 
		return self.countryname == other.countryname

	def __ne__(self, other): 
		return self.countryname != other.countryname

	def __hash__(self): 
		return hash(self.countryname)

	def __cmp__(self, other):
		return cmp(self.countryname, other.countryname)
	'''

class Group(object):
	"""Almacena el estado de un grupo, en base al análisis de los estados de los hosts contituyentes."""

	def __init__(self, groupname):
		super(Group, self).__init__()
		self.groupname = groupname
		self.state = 'OK'
		self.color = 'green'
		self.host_dict	= dict()

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
		return "%s" % (self.groupname)

	'''
	def __eq__(self, other): 
		return self.groupname == other.groupname

	def __ne__(self, other): 
		return self.groupname != other.groupname

	def __hash__(self): 
		return hash(self.groupname)

	def __cmp__(self, other):
		return cmp(self.groupname, other.groupname)
	'''

class Host(object):
	"""Almacena el estado de un host, en base al análisis de la alertas vía Livestatus."""

	def __init__(self, hostname, conn):
		super(Host, self).__init__()
		self.hostname = hostname
		self.conn = conn
		self.state = 'OK'
		self.color = 'green'

	def check_service(self, desc):
		a_list = ServiceStateHist( self.conn, self.hostname, desc )
		if len(a_list):
			a_list = a_list[0]
			info = "%s %.1f%% OK %.1f%% WARNING %.1f%% CRITICAL" % (desc, 100 * float(a_list[-3]), 100 * float(a_list[-2]), 100 * float(a_list[-1]))
		else:
			info = "No data"
		return info

	def check_cpu(self):
		desc = 'CPU load'
		self.cpu = self.check_service(self.conn, desc)

	def check_disk(self):
		desc = 'Disk IO SUMMARY'
		self.disk = self.check_service(self.conn, desc)

	def check_memory(self):
		desc = 'Memory'
		self.memory = self.check_service(self.conn, desc)

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

	def check_alerts(self):
		alerts_to_process = HostWarningAndCriticalAlerts( self.conn, self.hostname )
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
		return "%s" % (self.hostname)

	# agrego estos metodos
	'''
	def __eq__(self, other): 
		return self.hostname == other.hostname

	def __ne__(self, other): 
		return self.hostname != other.hostname

	def __hash__(self): 
		return hash(self.hostname)

	def __cmp__(self, other):
		return cmp(self.hostname, other.hostname)
	'''

class Connection(object):

	def __init__(self ):
		super(Connection, self).__init__()
		self.lv_server_ip_set	= {	'172.17.29.175', '172.17.29.254','172.20.177.130', 
									'172.18.171.130', '172.18.171.189', '172.20.5.100', 
									'172.21.35.246',}
		self.lv_server_port		= 6557
		self.LoadDictionary()

	def LoadDictionary( self ):
		'''
		Idea:
			Moverse por todas las ips
				Hacer query sobre hostsbygroup, por todas las columnas
					buscando host y tratar de determinar a que grupo aparece asociado
		'''
		self.country_dict	= dict()

		lql = "GET hostsbygroup\nColumns: custom_variables display_name"
		pattern = r'^.*CAPA_LOGICA\s+(\S+)\D+.*$'
		compiled_pattern = re.compile( pattern )

		for lv_server in self.lv_server_ip_set:
			# print("LoadDictionary: lv_server[%s]" % (lv_server))

			conn = _LV_Connect( lv_server, self.lv_server_port )
			a_list = LV_Execute( conn, lql )
			for sublist in a_list:
				a_dict = sublist[ 0 ]
				if u'TAGS' in a_dict:
					search = compiled_pattern.search( a_dict[u'TAGS'] )
					if search:
						group_name = search.groups()[0]
						country_prefix = PrefixOfGroup( group_name )
						if country_prefix:
							host_name = sublist[ 1 ]
							# print("LoadDictionary: group_name[%s] host_name[%s]" % (group_name, host_name))

							''' Esta versión funciona correctamente también ...
							if country_prefix not in self.country_dict:
								self.country_dict[country_prefix] = Country( country_prefix )

							if group_name not in self.country_dict[country_prefix].group_dict:
								self.country_dict[country_prefix].group_dict[group_name] = Group( group_name )

							if host_name not in self.country_dict[country_prefix].group_dict[group_name].host_dict:
								self.country_dict[country_prefix].group_dict[group_name].host_dict[host_name] = Host( host_name, conn )
							'''

							if country_prefix in self.country_dict:
								country_obj = self.country_dict[country_prefix]
							else:
								country_obj = Country( country_prefix )

							if group_name in country_obj.group_dict:
								group_obj = country_obj.group_dict[group_name]
							else:
								group_obj = Group( group_name )

							if host_name in group_obj.host_dict:
								host_obj = group_obj.host_dict[host_name]
							else:
								host_obj = Host( host_name, conn )


							group_obj.host_dict[host_name] = host_obj
							country_obj.group_dict[group_name] = group_obj
							self.country_dict[country_prefix] = country_obj

			# conn.disconnect() # dado que lo guardé en el objeto Host

	def show(self):
		for country_prefix in self.country_dict:
			print("country_prefix[%s]" % (self.country_dict[country_prefix].countryname))
			for group_name in self.country_dict[country_prefix].group_dict:
				print("\tgroup_name[%s]" % (self.country_dict[country_prefix].group_dict[group_name].groupname))
				for host_name in self.country_dict[country_prefix].group_dict[group_name].host_dict:
					print("\t\thost_name[%s]" % (self.country_dict[country_prefix].group_dict[group_name].host_dict[host_name].hostname))

def main():
	connection_obj = Connection()

if __name__ == '__main__':
	main()