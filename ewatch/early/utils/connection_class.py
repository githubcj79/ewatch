#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from __future__ import unicode_literals
from __future__ import print_function

import re

from live_utils import _LV_Connect, LV_Execute, GroupInCountry

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
		self.groups_dict	= dict()

		lql = "GET hostsbygroup\nColumns: custom_variables display_name"
		pattern = r'^.*CAPA_LOGICA\s+(\S+)\D+.*$'
		compiled_pattern = re.compile( pattern )

		for lv_server in self.lv_server_ip_set:
			print("LoadDictionary: lv_server[%s]" % (lv_server))

			conn = _LV_Connect( lv_server, self.lv_server_port )
			a_list = LV_Execute( conn, lql )
			for sublist in a_list:
				a_dict = sublist[ 0 ]
				if u'TAGS' in a_dict:
					search = compiled_pattern.search( a_dict[u'TAGS'] )
					if search:
						group_name = search.groups()[0]
						if GroupInCountry( group_name ):
							host_name = sublist[ 1 ]
							print("LoadDictionary: group_name[%s] host_name[%s]" % (group_name, host_name))
			conn.disconnect()

def main():
	connection_obj = Connection()

if __name__ == '__main__':
	main()