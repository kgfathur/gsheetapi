#!/usr/bin/python3

import os
import sys
import requests
import urllib3
import json
import time
from configparser import ConfigParser
from distutils.util import strtobool

from pveapi.connection import ProxmoxAPI

pve = ProxmoxAPI(configFile = 'conf.d/01-private.conf')
pve.login()
endpoint = '/api2/json/nodes/pve'
response = pve.get(endpoint = endpoint, debug = True)

print('Code:', response['status_code'])

if ( response['status_code'] == 200):
    data = response['data']
    print(json.dumps(data, indent=2))
                
elif (response['status_code'] == 401):
    data = response['data']
    print(json.dumps(data, indent=2))
    # if 'error' in json_response.keys():
    #     print(json_response['error']['reason'])
else:
    data = response['data']
    print(json.dumps(data, indent=2))
