#!/usr/bin/python3

import os
import sys
import requests
import urllib3
import json
import time
from configparser import ConfigParser
from distutils.util import strtobool

from pveapi import ProxmoxAPI
from easyconfig import EasyConfig

def get_vmid(e):
    return e.get('vmid')

workdir = os.getcwd() + '/gsheetapi'

default_config = ConfigParser()
default_config.read_string("""
[PVE_CONFIG]
pve_node = pve
pve_host = https://localhost
pve_port = 8006
pve_user = root
pve_pass = admin
pve_realm = pam
pve_cacert = certs/pve-root-ca.pem
pve_endpoint = /api2/json/access/ticket
verify_ssl = True

[GOOGLE_SHEET]
SPREADSHEET_ID = 0123456789AbCdEfGhIjKlMnOpQrStUvWxyz
SHEET_ID = 1234567890
RANGE_NAME = Sheet1!A2:A3
""")

ec = EasyConfig(default_config = default_config, debug = True)

os.sys.exit()

pve = ProxmoxAPI(configFile = 'conf.d/01-private.conf')
pve.login()
endpoint = '/api2/json/nodes/{}/qemu'.format(pve.node)
response = pve.get(endpoint = endpoint)

print('Code:', response['status_code'])

if ( response['status_code'] == 200):
    data = response['data']
    # print(json.dumps(data, indent=2))
    data.sort(key=get_vmid)

    for dati in data:
        print('{:>6} {:<36} {:<10} {:>8.2f} {:>8.2f} {:>10.2f}'.format(dati['vmid'], dati['name'], dati['status'], dati['maxdisk']/(1024*1024*1024), dati['maxmem']/(1024*1024*1024), dati['uptime']/3600))
                
elif (response['status_code'] == 401):
    data = response['data']
    print(json.dumps(data, indent=2))
    # if 'error' in json_response.keys():
    #     print(json_response['error']['reason'])
else:
    data = response['data']
    print(json.dumps(data, indent=2))