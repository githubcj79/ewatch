#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import livestatus
import sys

from early.utils.date_time_utils import Seconds
# from early.utils.raw_data import raw_table_lql

from ewatch.settings import livestatus_host, livestatus_port, days_to_review


cmk_livestatus_nagios_server = livestatus_host
cmk_livestatus_tcp_port = livestatus_port

DAYS_AGO = days_to_review

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


def HostWarningAndCriticalAlerts( conn, host ):
	
	seconds_now	=	Seconds( 0 )
	seconds_before	=	Seconds( DAYS_AGO )

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
	seconds_before	=	Seconds( DAYS_AGO )

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


def main( group ):
	'''
	Probar con:

	(alerts) ~/Projects/alerts$ ./live_utils.py
	GRUPO: CL_POS_REGIONAL 1
	'''
	print "main: GRUPO[%s]" % ( group, )

	conn = LV_Connect()

	hosts_list = HostsGroup( conn, group )
	# print( hosts_list )

	service_description_list = ['CPU load', 'Memory', 'Disk IO SUMMARY']

	for host in hosts_list:
		print host
		alert_list = HostCriticalAlerts( conn, host )
		for alert in alert_list:
			print alert
		for desc in service_description_list:
			a_list = ServiceStateHist( conn, host, desc )
			if len(a_list):
				a_list = ServiceStateHist( conn, host, desc )[0]
				print a_list
				print "%s %.1f%% OK %.1f%% WARNING %.1f%% CRITICAL" % (desc, 100 * float(a_list[-3]), 100 * float(a_list[-2]), 100 * float(a_list[-1]))


if __name__ == '__main__':
	group, dias = raw_input("GRUPO DIAS_A_REVISAR : ").split(' ')
	DAYS_AGO = int(dias)
	main( group )