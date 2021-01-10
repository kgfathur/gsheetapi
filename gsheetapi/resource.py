endpoint = '/api2/json/nodes/{}/qemu/{}/config'.format(pve.node, '405')
response = pve.get(endpoint = endpoint)

print('Code:', response['status_code'])

if ( response['status_code'] == 200):
    data = response['data']
    print(json.dumps(data, indent=2))
    
    for dati in data:
        print('{:>6} {:<36} {:<10} {:>8} {}'.format(dati['vmid'], dati['name'], dati['status'], dati['uptime'], dati['disk']))
                
elif (response['status_code'] == 401):
    data = response['data']
    print(json.dumps(data, indent=2))
    # if 'error' in json_response.keys():
    #     print(json_response['error']['reason'])
else:
    data = response['data']
    print(json.dumps(data, indent=2))