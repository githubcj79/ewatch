#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

import datetime

def Seconds( days_ago = 0 ):

	now = datetime.datetime.now()
	epoch = datetime.datetime.utcfromtimestamp(0)
	delta = now - epoch
	total_seconds = int( delta.total_seconds() )
	return total_seconds - days_ago * 86400


def main():

	now = datetime.datetime.now()
	print "now[%s]" % (now)

	epoch = datetime.datetime.utcfromtimestamp(0)
	print "epoch[%s]" % (epoch)

	delta = now - epoch
	total_seconds = int( delta.total_seconds() )
	print "total_seconds[%d]" % (total_seconds)

	total_seconds_seven_days_ago = total_seconds - 7 * 86400
	print "total_seconds_seven_days_ago[%d]" % (total_seconds_seven_days_ago)

	now = datetime.datetime.utcfromtimestamp(total_seconds)
	print "now[%s]" % (now)

	total_seconds = float( raw_input('total_seconds: ') )
	# print (total_seconds)
	now = datetime.datetime.utcfromtimestamp(total_seconds)
	print "now[%s]" % (now)

if __name__ == '__main__':
	main()