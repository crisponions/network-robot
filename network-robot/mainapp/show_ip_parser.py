from napalm import get_network_driver
import base64
from jinja2 import Environment, FileSystemLoader
import os
import re


# work magic on data
#vlan_info = list(switch_vlans.values())[0].split('\n')
#print(vlan_info)
def parse_ip_addr(address_dict):
    vlan_ips = dict()
    loopback_ips = dict()
    other_ips = dict()
    for key,value in address_dict.items():
        if re.match('Loopback', key):
            for k,v in value['ipv4'].items():
                LOOPBACK_NUM = re.match('loopback(\d+)',key.lower())
                if LOOPBACK_NUM is not None:
                    loopback_ips[LOOPBACK_NUM.group(1)] = [k, v['prefix_length']]
        elif re.match('[V,v]lan', key):
            for k,v in value['ipv4'].items():
                VLAN_ID = re.match('[V,v]lan(\d+)', key)
                if VLAN_ID is not None:
                    vlan_ips[VLAN_ID.group(1)] = [k, v['prefix_length']]
        else:
            for k,v in value['ipv4'].items():
                other_ips['other'] = [k, v['prefix_length']]


    #print(ips)
    #THIS_DIR = os.path.dirname(os.path.abspath(__file__))

    #j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
    #                                trim_blocks=True)
    #print(j2_env.get_template('templates/vlan_template.j2').render(ips=vlan_ips, loopbacks=loopback_ips))
    return {'vlan_ips': vlan_ips, 'loopback_ips': loopback_ips, 'other_ips': other_ips}

def parse_switch_ips(hostname, username, password):
    driver = get_network_driver('ios')
    device = driver(hostname=hostname, username=base64.b64decode(username), password=base64.b64decode(password))
    device.open()
    facts = device.get_interfaces_ip()
    device.close()
    return parse_ip_addr(facts)
    