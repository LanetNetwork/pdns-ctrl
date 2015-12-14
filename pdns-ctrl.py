#!/usr/bin/env python2.7

import BaseHTTPServer
import ConfigParser
import ipaddress
import re
import subprocess
import urlparse

PC_CONF="pdns-ctrl.ini"

def pc_conf(_file, _section, _key):
	config = ConfigParser.ConfigParser()
	config.read(_file)
	return config.get(_section, _key, 0)

def make_response(_s, _code, _msg):
	_s.send_response(_code);
	_s.send_header("Content-type", "text/html")
	_s.end_headers()
	_s.wfile.write(_msg)

def is_valid_hostname(hostname):
	if len(hostname) > 255:
		return False
	if hostname[-1] == ".":
		hostname = hostname[:-1]
	allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
	return all(allowed.match(x) for x in hostname.split("."))

class pc_handler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(s):
		query = {}
		if "?" in s.path:
			location, params = s.path.split("?", 1)
			query = urlparse.parse_qs(params)
			if location == "/wipe-cache":
				if "id" in query and "token" in query and "host" in query:
					id = query["id"][0]
					token = query["token"][0]
					host = query["host"][0]
					ip = s.client_address[0]
					if is_valid_hostname(host):
						if ipaddress.ip_address(unicode(ip)) in ipaddress.ip_network(unicode(pc_conf(PC_CONF, id, "ip"))):
							if token == pc_conf(PC_CONF, id, "token"):
								ret = subprocess.check_output([pc_conf(PC_CONF, "global", "helper"), "wipe-cache", host])
								success = re.compile("^wiped [0-9]+ records, [0-9]+ negative records$")
								if success.match(ret):
									make_response(s, 200, "OK")
								else:
									make_response(s, 500, "NOT-OK")
							else:
								make_response(s, 401, "NOT-OK")
						else:
							make_response(s, 401, "NOT-OK")
					else:
						make_response(s, 400, "NOT-OK")
				else:
					make_response(s, 400, "NOT-OK")
			else:
				make_response(s, 404, "NOT-OK")
		else:
			make_response(s, 404, "NOT-OK")

if __name__ == '__main__':
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((pc_conf(PC_CONF, "global", "host"), int(pc_conf(PC_CONF, "global", "port"))), pc_handler)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()

# vim: set tabstop=4:softtabstop=4:shiftwidth=4:noexpandtab

