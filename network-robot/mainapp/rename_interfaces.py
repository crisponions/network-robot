from napalm import get_network_driver
import base64
import re
import pdb
'''
driver = get_network_driver('ios')
switch_name = input('Enter switch name: ')
#switch_name = "CEIa6c1"
creds = hash_stuff()

device = driver(hostname=switch_name, username=base64.b64decode(creds[0]), password=base64.b64decode(creds[1]))
device.open()
interfaces = device.get_interfaces()
device.close()

for k, v in interfaces.items():
    if "FastEthernet" in k:
        port = re.match('.+Ethernet(\d)\/0\/(\d*)', k)
        #pdb.set_trace()
        if port:
            swnum = int(port.group(1))    
            portnum = int(port.group(2))
            print('ge-{0}/0/{1}'.format(swnum - 1, portnum - 1))
            if v['description'] is not '':
                print('  description {}'.format(v['description']))

'''
def rename_vlan_port_list(vlans):
    renamed_vlans_list = dict()
    for k, v in vlans.items():
        for ports in v['ports']:
            port = re.match('(Fa|Gi)(\d)\/0\/(\d*)', ports)
            if port:
                swnum = int(port.group(2))    
                portnum = int(port.group(3))
                print('ge-{0}/0/{1} - {2}'.format(swnum - 1, portnum - 1, v['name']))
            else:
                print(v['ports'])

def rename_interface(int_name):
    port = re.match('(Fa.*)(\d)\/0\/(\d*)', int_name)
    if port:
        swnum = int(port.group(2))    
        portnum = int(port.group(3))
        return 'ge-{0}/0/{1}'.format(swnum - 1, portnum - 1)
    else:
        port = re.match('(Gi.*)(\d)\/0\/(\d*)', int_name) 
        if port:
            swnum = int(port.group(2))    
            portnum = int(port.group(3))
            return 'xe-{0}/2/{1}'.format(swnum - 1, portnum - 1)