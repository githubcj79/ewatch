#-*- coding: utf-8 -*-

from __future__ import print_function


# import settings
from ewatch.settings import DEBUG
from ewatch.settings import API_PATH
from ewatch.settings import livestatus_host
from ewatch.settings import livestatus_port

import sys
sys.path.insert(0, API_PATH)

# https://pythonhosted.org/kitchen/unicode-frustrations.html (python-kitchen)
from kitchen.text.converters import getwriter
UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

if DEBUG:
	print("sys.path[%s]" % sys.path)

from api import livestatus

# import livestatus

if DEBUG:
	print("DEBUG[%d]" % DEBUG)


def raw_table_lql(query):
	"""
	Retorna la lista asociada al lql recibido como parámetro.
	"""

	if DEBUG:
		print("query[%s]" % query)

	try:
		# Make a socket
		socket_path = "tcp:%s:%s" % (livestatus_host,livestatus_port)
		if DEBUG:
			print("socket_path[%s]" % socket_path)

	except:
		sys.exit(1)

	try:
		# make connection
		conn = livestatus.SingleSiteConnection(socket_path)
		if DEBUG:
			print("conn[%s]", conn)

		a_list = conn.query_table( query )
		return( a_list )

	except Exception, e: # livestatus.MKLivestatusException, e:
		print("Livestatus error: [%s]" % str(e))
		exit (2)


if __name__ == '__main__':
	"""
	Retorna la lista con el resultado de la ejecución del query recibido,
	vía query_table().

	Ejemplos de queries:
		"GET hostsbygroup\nColumns: custom_variable_values display_name"

	Ejemplos de invocación:
		./raw_data.py "GET services\nFilter: host_name = spp36db03r"

	GET services\nFilter: description ~ CPU util\nStats: avg perf_data\nFilter: host_name = spp36db03r
	GET services\nFilter: description ~ CPU load\nStats: avg perf_data\nFilter: host_name = spp36db03r
	"""

	if len(sys.argv) < 2:
		print("Invocación: %s query" % (sys.argv[0]))
		exit(2)

	lql = sys.argv[1].decode("string_escape")

	if DEBUG:
		print("query[%s]" % (lql))

	a_list = raw_table_lql(lql)
	print( a_list )