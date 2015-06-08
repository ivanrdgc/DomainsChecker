#!/usr/bin/python3

import common

def api_check_domains(domains, s_login, s_pw):
	import urllib.parse, http.client, sys, os

	full_domains_list = list(domains)
	ret = {}

	original_full_domains_list = len(full_domains_list)

	https_connection = http.client.HTTPSConnection('api.rrpproxy.net')

	try:
		while (len(full_domains_list) > 0):
			domains_list = full_domains_list[:32]
			full_domains_list = full_domains_list[32:]

			post_params = []
			post_params.append(('s_login', s_login))
			post_params.append(('s_pw', s_pw))
			post_params.append(('command', 'checkdomains'))

			for i in range(len(domains_list)):
				post_params.append(('domain%i'%i, domains_list[i]))

			https_connection.request('POST', '/api/call.cgi', urllib.parse.urlencode(post_params).encode('utf-8'))
			api_request = https_connection.getresponse()
			api_output = api_request.read().decode('utf-8')

			for i in range(len(domains_list)):
				if ('property[domaincheck][%i] = 210'%i in api_output):
					domainAvailable = True
				elif ('property[domaincheck][%i] = 211'%i in api_output):
					domainAvailable = False
				else:
					# Try to call API for this single domain
					post_params = []
					post_params.append(('s_login', s_login))
					post_params.append(('s_pw', s_pw))
					post_params.append(('command', 'checkdomain'))
					post_params.append(('domain', domains_list[i]))
					
					https_connection.request('POST', '/api/call.cgi', urllib.parse.urlencode(post_params).encode('utf-8'))
					api_request = https_connection.getresponse()
					new_api_output = api_request.read().decode('utf-8')

					if ('code = 210' in new_api_output):
						domainAvailable = True
					elif ('code = 211' in new_api_output):
						domainAvailable = False
					else:
						domainAvailable = 'ERROR ' + new_api_output.split('code = ', 1)[1].split('\n')[0] + ': ' + new_api_output.split('description = ', 1)[1].split('\n')[0]
				ret[domains_list[i]] = domainAvailable

			sys.stdout.write(str(round(100-len(full_domains_list)/original_full_domains_list*100, 2)) + '% completed...' + os.linesep)
			sys.stdout.flush()
	finally:
		https_connection.close()

	return(ret)

def read_extensions(file_name):
	ret = set()

	f = open(file_name, 'rt')
	lines = f.readlines()
	f.close()

	for l in lines:
		ret.add(l.strip())

	return(ret)

def write_csv(domains, base, output):
	import os, os.path

	output_path = common.get_full_path(output)
	os.makedirs(os.path.dirname(output_path), 0o755, True)

	f = open(output_path, 'wt')
	
	f.write('sep=,\nDomain,Extension,Availability\n')

	for d in domains:
		if (isinstance(domains[d], str)):
			f.write('%s,%s,%s\n'%(d,d[len(base):],domains[d]))
		else:
			f.write('%s,%s,%s\n'%(d,d[len(base):],'available' if (domains[d]) else 'not available'))

	f.close()

def check_domains(domain_base):
	import os.path

	app_config = common.read_config()

	extensions = read_extensions(common.get_full_path(app_config['ExtensionsFile']))

	domains_to_check = set()

	for e in extensions:
		domains_to_check.add(domain_base+'.'+e)

	domains_info = api_check_domains(domains_to_check, app_config['RrpproxyLogin'], app_config['RrpproxyPw'])

	write_csv(domains_info, domain_base, os.path.join(app_config['OutputPath'], domain_base+'.csv'))

if (__name__ == '__main__'):
	import sys

	if (len(sys.argv) >= 2):
		#TODO Exceptions
		check_domains(sys.argv[1])
	else:
		print('Usage: %s <domain_to_check>'%sys.argv[0])
