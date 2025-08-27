#! /usr/bin/env python

import os
import sys
import time
import subprocess
from . import log


def perform(timeout, toolname, command):
		try:		
			log.log(f'[ StartTool ] Start running {toolname}, timeout is {timeout} minutes.')
			if 'findsub_script' in toolname:
				shcommand = command.split(' ')
				p = subprocess.Popen(shcommand, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			else:
				p = subprocess.Popen(command, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

			code = p.wait(timeout*60)
			if code == 0:
				log.log(f'[ ToolSuccess ] {toolname} perform success.\n')
			else:
				log.log(f"[ ToolError ] {toolname} -> return: {code}, perform error\n")
			if p.stderr.read():
				log.log(f"[ ToolError ] {toolname} -> error information: {p.stderr.read()}\n")
		except Exception as e:
				log.log(f'[ ToolError ] {toolname} {str(e)}\n')


def command_dict(r_path, root_path, o_path, target, git_api, chaos_api, subdict):
	try:
		shell_path = os.path.join(root_path, 'shells')
		# findsub script absolute path
		findsub_pathname = os.path.join(shell_path, 'findsub')

		output_config = f" >> {o_path}/output 2>&1"
		# command dict
		command = {
		'oneforall': f'python /root/subdomain/OneForAll/oneforall.py --port large --brute --path {o_path}/oneforall.csv --target {target} run {output_config}',
		'esd': f'esd -d {target} {output_config}',
		'move_esd_file': 'mv /tmp/esd/.*.esd /root/result',
		# 'ctfr': f'python /root/subdomain/ctfr/ctfr.py -o ${r_path}/ctfr -d {target} ${output_config}',
		'subdomainsbrute': f'python /root/subdomain/subDomainsBrute/subDomainsBrute.py -o {r_path}/subdomainbrute --full {target} {output_config}',
		'aquatone': f'aquatone-discover -t 10 -s 1 --fallback-nameservers 8.8.8.8,223.6.6.6,180.76.76.76,1.1.1.1 -d {target} {output_config}',
		'move_aquatone_file': f'mv /root/aquatone/{target}/hosts.json {r_path}',
		'ksubdomain': f'ksubdomain -full -l 1 -csv -o {r_path}/ksubdomain.csv -d {target} {output_config}',
		'github-subdomains': f'github-subdomains -t {git_api} -o {r_path}/github_subdomains -d {target} {output_config}',
		'chaos': f'chaos -silent -key {chaos_api} -o {r_path}/chaos -d {target} {output_config}',
		'findsub_script': f'{findsub_pathname} -t {target}',
		'fierce': f'fierce --wide --domain {target} >> {r_path}/fierce',
		'dnsub_dns': f'/root/subdomain/dnsub/dnsub --dns 8.8.8.8,223.6.6.6,180.76.76.76,1.1.1.1 --depth 1 -o {r_path}/dnsub_dns.csv -d {target} {output_config}',
		'dnsub_nodns': f'/root/subdomain/dnsub/dnsub --depth 1 -o {r_path}/dnsub_nodns.csv -d {target} {output_config}',
		# bruteforce
		'dnsub_brute': f'/root/subdomain/dnsub/dnsub -f {subdict} --depth 1 -o {r_path}/dnsub_brute.csv -d {target} {output_config}',
		'ksubdomain_brute': f'ksubdomain -l 1 -f {subdict} -csv -filter-wild -o {r_path}/ksubdomain_brute.csv -d {target} {output_config}',
		'findomain': f'findomain --ua /root/subdomain/findomain/ua -w {subdict} --pscan -u {r_path}/findomain_brute -t {target} {output_config}',
		'subdomainsbrute': f'python /root/subdomain/subDomainsBrute/subDomainsBrute.py -o {r_path}/subdomainbrute_brute --full -f {subdict} {target} {output_config}'
		}

		return command
	except Exception as e:
		log.log(f'[ Runtools Error ]  command_dict: {str(e)}\n')



# main
def main(timeout, r_path, o_path, root_path, target, git_api, chaos_api, subdict):
		try:
			c_dict = command_dict(r_path, root_path, o_path, target, git_api, chaos_api, subdict)

			for toolname in c_dict.keys():
				command = c_dict.get(toolname)
				perform(timeout, toolname, command)
		except Exception as e:
				log.log('[ Runtools Error ]  main: ' + str(e))

