from napalm import get_network_driver
import base64
import re
import pdb
from datetime import datetime

from mainapp.show_ip_parser import parse_ip_addr
from mainapp.show_vlan_parser import parse_vlan_output
import mainapp.show_command_parsers as parser

def parse_interface_desc(int_desc_output):
    int_desc = dict()
    for line in int_desc_output['show interface description'].split('\n'):
        line_match = re.match('(\w+|\w{1,2}\d\/\d\/\d+)\s+(up|(admin )?down)\s+(up|down)\s*(\S.*)?', line)
        if line_match:
            port = line_match.group(1).replace('Fa','FastEthernet').replace('Gi','GigabitEthernet')
            int_desc[port] = line_match.group(5)
    return int_desc



def gather_old_switch_info(hostname, username, password):
    driver = get_network_driver('ios')
    # Connect to the switch and get data
    device = driver(hostname=hostname, username=base64.b64decode(username), password=base64.b64decode(password))
    start = datetime.now()
    try:
        device.open()
    except:
        return "ERROR"
    # get necessary info from switch
    print(f'Getting info from {hostname}\n')
    old_switch_facts = device.cli(['show interface description','sh run | inc snmp-server location', 'show vlan',
                                   'show cdp neighbors | exc SEP', 
                                   'sh run | inc Ethernet|^ switchport access vlan|^ switchport voice vlan',
                                   'show switch | inc \d', 'show run | inc helper-address'])

    old_ip_facts = device.get_interfaces_ip()
    device.close()
    end = datetime.now()
    print(end - start)

   

    old_vlans = parse_vlan_output(old_switch_facts)
    old_location = parser.parse_location(old_switch_facts)
    old_ips = parse_ip_addr(old_ip_facts)
    old_int_desc = parse_interface_desc(old_switch_facts)
    old_cdp_wap = parser.parse_cdp_wap_neighbors(old_switch_facts)
    old_cdp = parser.parse_cdp_neighbors(old_switch_facts)
    old_cdp_neigh = {**old_cdp_wap, **old_cdp}
    old_interfaces = parser.parse_show_run_interface(old_switch_facts)
    old_member_count = parser.parse_switch_stack_count(old_switch_facts)
    old_nameserver = parser.parse_onoff_hill(old_switch_facts)
    for key in old_vlans.keys():
        if int(key) > 2200:
            vlan_index = key[-2:]
    old_switch = {'ips': old_ips, 'descriptions': old_int_desc,
        'vlans': old_vlans, 'cdp': old_cdp_neigh, 'interfaces': old_interfaces, 
        'location': old_location, 'members': old_member_count, 
        'nameserver': old_nameserver, 'hostname': hostname, 'vlan_index': vlan_index}

    #print(old_ips)
    #print(old_int_desc)
    print(old_switch)
    return (old_switch)

def gather_dist_info(hostname, username, password):
    driver = get_network_driver('ios')
    # Connect to the switch and get data
    device = driver(hostname=hostname, username=base64.b64decode(username), password=base64.b64decode(password))
    device.open()
    
    # get necessary info from switch
    print(f'Getting info from {hostname}\n')
    old_switch_facts = device.cli(['show interface description','sh run | inc snmp-server location', 'show vlan',
                                   'show cdp neighbors | exc SEP', 
                                   'sh run | inc Ethernet|^ switchport access vlan|^ switchport voice vlan'])

    old_ip_facts = device.get_interfaces_ip()
    device.close()
    old_vlans = parse_vlan_output(old_switch_facts)
    old_location = parser.parse_location(old_switch_facts)
    old_ips = parse_ip_addr(old_ip_facts)
    old_int_desc = parse_interface_desc(old_switch_facts)
    old_cdp_wap = parser.parse_cdp_wap_neighbors(old_switch_facts)
    old_cdp = parser.parse_cdp_neighbors(old_switch_facts)
    old_cdp_neigh = {**old_cdp_wap, **old_cdp}
    print(old_cdp_neigh)
    old_interfaces = parser.parse_show_run_interface(old_switch_facts)
    old_switch = {'ips': old_ips, 'descriptions': old_int_desc,
        'vlans': old_vlans, 'cdp': old_cdp_neigh, 'interfaces': old_interfaces, 
        'location': old_location, 'hostname': hostname}
    return (old_switch)