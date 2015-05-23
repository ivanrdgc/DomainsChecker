#!/usr/bin/python3

def api_check_domains(domains, s_login, s_pw):
	import urllib.parse, urllib.request, urllib.error, sys, os

	base_url = 'https://api.rrpproxy.net/api/call.cgi'
	full_domains_list = list(domains)
	ret = {}

	original_full_domains_list = len(full_domains_list)

	while (len(full_domains_list) > 0):
		domains_list = full_domains_list[:32]
		full_domains_list = full_domains_list[32:]

		post_params = []
		post_params.append(('s_login', s_login))
		post_params.append(('s_pw', s_pw))
		post_params.append(('command', 'checkdomains'))

		for i in range(len(domains_list)):
			post_params.append(('domain%i'%i, domains_list[i]))

		api_request = urllib.request.urlopen(base_url, urllib.parse.urlencode(post_params).encode('utf-8'))
		api_output = api_request.read().decode('utf-8')

		for i in range(len(domains_list)):
			ret[domains_list[i]] = True if ('property[domaincheck][%i] = 210'%i in api_output) else False

		sys.stdout.write(str(round(100-len(full_domains_list)/original_full_domains_list*100, 2)) + '% completed...' + os.linesep)
		sys.stdout.flush()

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
	import sys, os, os.path

	if (hasattr(sys, 'frozen')):
		output_path = os.path.join(os.path.dirname(os.path.realpath(sys.executable)), output)
	else:
		output_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), output)

	os.makedirs(os.path.dirname(output_path), 0o755, True)

	f = open(output_path, 'wt')
	
	f.write('Domain,Extension,Availability%s'%os.linesep)

	for d in domains:
		f.write('%s,%s,%s%s'%(d,d[len(base):],'available' if (domains[d]) else 'not available', os.linesep))

	f.close()

def check_domains(domain_base):
	import configparser, os.path

	config = configparser.ConfigParser()
	config.read('config.ini')
	app_config = config['DEFAULT']

	extensions = read_extensions(app_config['ExtensionsFile'])

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
