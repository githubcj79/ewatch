#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import livestatus
import sys
import re


from early.utils.date_time_utils import Seconds
# from early.utils.raw_data import raw_table_lql

from ewatch.settings import livestatus_host, livestatus_port, days_to_review, SECONDS_BEFORE


# cmk_livestatus_nagios_server = livestatus_host
# cmk_livestatus_tcp_port = livestatus_port

DAYS_AGO = days_to_review

def _LV_Connect( lv_server, lv_server_port ):

	try:
		# Creamos el socket
	    socket_path = "tcp:%s:%s" % (lv_server,lv_server_port)
	except Exception, e:
		print "Livestatus error: %s" % str(e)
		sys.exit(1)

	try:
	    # Creamos la conexión con MK Livestatus usando el socket
		return livestatus.SingleSiteConnection(socket_path)
	except Exception, e: # livestatus.MKLivestatusException, e:
		print "Livestatus error: %s" % str(e)
		exit (2)


def LV_Connect():

	try:
		# Creamos el socket
	    socket_path = "tcp:%s:%s" % (cmk_livestatus_nagios_server,cmk_livestatus_tcp_port)
	except Exception, e:
		print "Livestatus error: %s" % str(e)
		sys.exit(1)

	try:
	    # Creamos la conexión con MK Livestatus usando el socket
		return livestatus.SingleSiteConnection(socket_path)
	except Exception, e: # livestatus.MKLivestatusException, e:
		print "Livestatus error: %s" % str(e)
		exit (2)


def LV_Execute( conn, lql ):
	return conn.query_table(lql)


def HostsGroup( conn, group ):
	lql = "GET hostsbygroup\nColumns: custom_variable_values display_name"
	a_list = LV_Execute( conn, lql )

	# Se detectan los hosts asociados al grupo de servicios recibido.
	hosts_list = []
	for sublist in a_list:
		if str( sublist ).find(group) != -1:
			hosts_list.append( sublist[1] )

	return hosts_list

def GroupInCountry( group ):
	'''
	Retorna True si group comienza con uno de los prefijos de pais aquí definidos.
	'''
	prefix_list = [ r'CL_', r'AR_', r'PE_', r'CO_', r'BR_', ]

	for prefix in prefix_list:
		if re.match( prefix, group, re.M|re.I):
			return True

	return None

def GroupsSet( conn ):
	'''
	Retorna un set con todos los grupos detectados.

	See patterns in https://www.tutorialspoint.com/python/python_reg_expressions.htm
	'''

	lql = "GET hostsbygroup\nColumns: custom_variable_values display_name"
	a_list = LV_Execute( conn, lql )

	pattern = r'^.*CAPA_LOGICA\s+(\S+)\D+.*$'
	compiled_pattern = re.compile( pattern )

	group_set = set()
	for sublist in a_list:
		search = compiled_pattern.search( str( sublist ) )
		if search:
			group = search.groups()[0]
			# print( group )
			if GroupInCountry( group ):
				group_set.add( group )

	return group_set

def PrefixOfGroup( group ):
	'''
	Retorna el prefijo del pais del grupo.
	Si no tiene un prefijo conocido, retorna None.
	'''
	prefix_list = [ r'CL_', r'AR_', r'PE_', r'CO_', r'BR_', ]

	for prefix in prefix_list:
		if re.match( prefix, group, re.M|re.I):
			return prefix

	return None

def GroupsDictionary( conn ):
	'''
	Retorna un dictionario en que las key son los prefijos de los paises,
	y los values son sets con los grupos detectados de cada pais.

	See patterns in https://www.tutorialspoint.com/python/python_reg_expressions.htm
	See dictionary en https://stackoverflow.com/questions/1024847/add-new-keys-to-a-dictionary
	'''

	lql = "GET hostsbygroup\nColumns: custom_variable_values display_name"
	a_list = LV_Execute( conn, lql )

	pattern = r'^.*CAPA_LOGICA\s+(\S+)\D+.*$'
	compiled_pattern = re.compile( pattern )

	# group_set = set()
	group_dict = dict()
	for sublist in a_list:
		search = compiled_pattern.search( str( sublist ) )
		if search:
			group = search.groups()[0]
			# print( group )
			country = PrefixOfGroup( group )
			if country:
				if country in group_dict:
					key_set = group_dict[ country ]
				else:
					key_set = set()
				key_set.add( group )
				group_dict[ country ] = key_set

	return group_dict
	

def HostWarningAndCriticalAlerts( conn, host ):
	
	seconds_now	=	Seconds( 0 )
	print("HostWarningAndCriticalAlerts: seconds_now[%s]" % (seconds_now))

	# seconds_before	=	Seconds( DAYS_AGO )

	seconds_before	= seconds_now - SECONDS_BEFORE
	print("HostWarningAndCriticalAlerts: seconds_before[%s]" % (seconds_before))

	lql = ("GET log\n" +
		# "Columns: time type options state\n" +
		"Columns: time type options\n" +
		("Filter: host_name = %s\n" % host) +
		("Filter: time >= %s\n" % seconds_before) +
		("Filter: time <= %s\n" % seconds_now) +
		'Filter: state    = 1 \n' + # WARNING
		'Filter: state    = 2 \n' + # CRITICAL
		'Or: 2 \n' +
		"Filter: class = 1\n") # 1 - host and service alerts

	return LV_Execute( conn, lql )

def ServiceStateHist( conn, host, service_description ):
	seconds_now	=	Seconds( 0 )
	print("ServiceStateHist: seconds_now[%s]" % (seconds_now))

	# seconds_before	=	Seconds( DAYS_AGO )

	seconds_before	= seconds_now - SECONDS_BEFORE
	print("ServiceStateHist: seconds_before[%s]" % (seconds_before))

	lql = ("GET statehist\n" +
		"Columns: host_name service_description\n" +
		("Filter: host_name = %s\n" % host) +
		("Filter: service_description = %s\n" % service_description) +
		("Filter: time >= %s\n" % seconds_before) +
		("Filter: time <= %s\n" % seconds_now) +
		"Stats: sum duration_ok\n" +
		"Stats: sum duration_warning\n" +
		"Stats: sum duration_critical\n" +
		"Stats: sum duration_part_ok\n" +
		"Stats: sum duration_part_warning\n" +
		"Stats: sum duration_part_critical\n")

	return LV_Execute( conn, lql )

# def AlertState( state, str_alert ):
# 	state_list = [ 'ok', 'warn', 'crit' ]

# 	if state not in state_list:
# 		raise Exception("AlertState: state[%s] no es valido." % (state)) 



def main( group ):
	'''
	Probar con:

	(alerts) ~/Projects/alerts$ ./live_utils.py
	GRUPO: CL_POS_REGIONAL 1
	'''
	print "main: GRUPO[%s]" % ( group, )

	conn = LV_Connect()

	hosts_list = HostsGroup( conn, group )
	print( hosts_list )
	print(' ')

	# Idea invocar a función que retorna set con todos los grupos
	# CL_xxx  --> grupo de Chile, etc

	group_set = GroupsSet( conn )
	print( group_set )
	print(' ')

	# --> aqui voy
	group_dict = GroupsDictionary( conn )
	print( group_dict )
	print(' ')








	# service_description_list = ['CPU load', 'Memory', 'Disk IO SUMMARY']

	# for host in hosts_list:
	# 	print host
	# 	alert_list = HostCriticalAlerts( conn, host )
	# 	for alert in alert_list:
	# 		print alert
	# 	for desc in service_description_list:
	# 		a_list = ServiceStateHist( conn, host, desc )
	# 		if len(a_list):
	# 			a_list = ServiceStateHist( conn, host, desc )[0]
	# 			print a_list
	# 			print "%s %.1f%% OK %.1f%% WARNING %.1f%% CRITICAL" % (desc, 100 * float(a_list[-3]), 100 * float(a_list[-2]), 100 * float(a_list[-1]))


if __name__ == '__main__':
	# group, dias = raw_input("GRUPO DIAS_A_REVISAR : ").split(' ')

	# Sólo para acelerar las pruebas
	# group = 'CL_POS_REGIONAL'
	group = 'CL_MANHATTAN'

	
	dias = 1

	DAYS_AGO = int(dias)
	main( group )