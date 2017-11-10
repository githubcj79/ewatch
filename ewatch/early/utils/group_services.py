#-*- coding: utf-8 -*-

from __future__ import print_function


# import settings
from ewatch.settings import DEBUG


from early.utils.raw_data import raw_table_lql
# from utils.testing import a_function


import sys
# sys.path.insert(0, API_PATH)

import re

# https://pythonhosted.org/kitchen/unicode-frustrations.html (python-kitchen)
from kitchen.text.converters import getwriter
UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

if DEBUG:
	print("sys.path[%s]" % sys.path)

# import livestatus

if DEBUG:
	print("DEBUG[%d]" % DEBUG)

def show_host( str_host ):
	print( "host[%s]" % (str_host))

def get_item( input_str, pattern ):
	compiled_pattern = re.compile( pattern )
	search = compiled_pattern.search( input_str )
	if search:
		groups = search.groups()
		return( ' '.join( groups ) )
	else:
		return( 'No Data' )

def show_cpu_load( str_cpu ):
	pattern = r'^.*(load15=\d+\.\d+)\D+.*$'
	print( "\tcpu_load[%s]" % ( get_item( str_cpu, pattern ) ))
	if DEBUG:
		print( "\tstr_cpu[%s]" % ( str_cpu ))

def show_disk( str_disk ):
	pattern = r'^.*(disk_utilization=\d+\.\d+)\D+.*$'
	print( "\tstr_disk[%s]" % ( get_item( str_disk, pattern ) ))
	if DEBUG:
		print( "\tstr_disk[%s]" % ( str_disk ))

def show_memory( str_memory ):
	pattern = r'^.*(mem_total=\d+\.\d+)\D+(mem_used=\d+\.\d+)\D+.*$'
	print( "\tstr_memory[%s]" % ( get_item( str_memory, pattern ) ))
	if DEBUG:
		print( "\tstr_memory[%s]" % ( str_memory ))

def show_group_services_data( host_services_list ):

	_host	= 0
	_cpu	= 1
	_disk	= 2
	_memory	= 3

	for sublist in host_services_list:
		show_host( sublist[_host] )
		show_cpu_load( sublist[_cpu] )
		show_disk( sublist[_disk] )
		show_memory( sublist[_memory] )

def group_services( group ):
	'''
		Recibe group y retorna una lista, con 4 sublistas:
		- la primera con los hosts
		- la segunda con el uso de cpu
		- la tercera con el uso de disco
		- la cuarta con el uso de memoria

		Ejemplos de invocación: 
			group_services( 'CL_HUB_PAGOS_PARIS' )
			group_services( 'CL_FACTURA_ELECTRONICA' )
	'''

	if DEBUG:
		print("group[%s]" % (group))


	lql = "GET hostsbygroup\nColumns: custom_variable_values display_name"
	a_list = raw_table_lql(lql)

	if DEBUG:
		print( a_list )

	"Se detectan los hosts asociados al grupo de servicios recibido."
	hosts_list = []
	for sublist in a_list:
		if str( sublist ).find(group) != -1:
			hosts_list.append( sublist[1] )

	if DEBUG:
		print( hosts_list )

	lql_list =	[	
				"GET services\nStats: avg perf_data\nFilter: description ~ CPU load\nFilter: host_name = %s",
				"GET services\nFilter: description ~ Disk IO SUMMARY\nStats: avg perf_data\nFilter: host_name = %s",
				"GET services\nFilter: description ~ Memory\nStats: avg perf_data\nFilter: host_name = %s"
				]

	"Para cada host obtener sus servicios"
	host_services_list = []
	for host in hosts_list:
		host_services_sub_list = []

		"Se agrega el host a la sub lista"
		host_services_sub_list.append( host )

		for command in lql_list:
			lql = command % (host)
			if DEBUG:
				print("lql[%s]" % (lql))
			a_list = raw_table_lql(lql)
			if DEBUG:
				print( a_list )
			info = a_list[0][0]

			"Se agrega información a la sub lista"
			host_services_sub_list.append( info )

		"Se agrega la sub lista a la lista principal"
		host_services_list.append( host_services_sub_list )

	return host_services_list


if __name__ == '__main__':
	"""
	Ejemplos de invocación: 
	
	./group_services.py "CL_HUB_PAGOS_PARIS"
	./group_services.py "CL_FACTURA_ELECTRONICA"
	"""

	if len(sys.argv) < 2:
		print("Invocación: %s group" % (sys.argv[0]))
		exit(2)

	group = sys.argv[1].decode("string_escape")

	if DEBUG:
		print("group[%s]" % (group))

	show_group_services_data( group_services( group ) )
	exit(0)
