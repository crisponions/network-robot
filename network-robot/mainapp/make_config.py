from mainapp.qip_dns_query import get_switch_ips
import base64
from mainapp.show_ip_parser import parse_switch_ips
from mainapp.gather_old_info import gather_old_switch_info
from mainapp.show_command_parsers import parse_show_run_interface
from mainapp.rename_interfaces import rename_vlan_port_list, rename_interface
from mainapp.qip_dns_query import get_switch_ips
from datetime import date
import re
import pdb

hostname = ""
CLOSET = ""
ONHILL = ""
BUILDENGINEER = ""
BUILDDATE = ""
MEMBERS = ""
LOOPBACK = ""

AGG_INT_NAME = ""

V100_VRRP = ""
V100_GW = ""
V300_VRRP = ""
V200_GW = ""
V555_VRRP = ""
V555_GW = ""
V701_VRRP = ""
V701_GW = ""
V702_VRRP = ""
V702_GW = ""
V703_VRRP = ""
V703_GW = ""
VLAN_INDEX = ""
UPLINK_1_IP = ""
UPLINK_2_IP = ""
INTER_REG = ""

LICENSE_KEY_1 = ""
LICENSE_KEY_2 = ""
DATE = date.today().strftime('%m\%d\%Y')

def rename_cisco_to_junos(cisco_switch):
    juniper_interfaces = dict()
    for k,v in cisco_switch['interfaces'].items():
        j = rename_interface(k)
        juniper_interfaces[j] = {'vlan': '', 'voice': ''}
        if k in cisco_switch['descriptions'].keys():
            juniper_interfaces[j]['description'] = cisco_switch['descriptions'][k]
        if v:
            if 'voice' in v and 'vlan' in v:
                juniper_interfaces[j]['vlan'] = cisco_switch['vlans'][v['vlan']]['name'].upper()
                juniper_interfaces[j]['voice'] = cisco_switch['vlans'][v['voice']]['name'].upper()
            elif 'vlan' in v:
                juniper_interfaces[j]['vlan'] = cisco_switch['vlans'][v['vlan']]['name'].upper()
                juniper_interfaces[j]['voice'] = None
    return juniper_interfaces

def create_template(old_switch_info, dns_records):
    new_switch = dict()
    new_switch['loopback'] = find_new_loopback(old_switch_info['hostname'], dns_records)
    new_switch['nameserver'] = old_switch_info['nameserver']
    new_switch['members'] = old_switch_info['members']
    new_switch['vlans'] = old_switch_info['vlans']
    if new_switch['members'] > 1:
        new_switch['mgmt_range_end'] = 1
    else:
        new_switch['mgmt_range_end'] = 0
    new_switch['vlan_ips'] = old_switch_info['ips']['vlan_ips']
    new_switch['vrrp'] = find_vrrp_addresses(old_switch_info['vlans'], old_switch_info['ips']['vlan_ips'], dns_records)
    return new_switch
    
def find_new_loopback(hostname, dns_records):
    for item in dns_records:
        if item['name'].lower() == '{}-new.ohsu.edu'.format(hostname.lower()):
            return item['address']

def find_vrrp_addresses(vlans, vlan_ips, dns_records):
    vrrp = dict()
    for item in dns_records:
        is_vlan = re.match('.*(vlan|vl)(\d{2,4})\..*',item['name'].lower())
        is_vrrp = re.match('.*-old-(vlan|vl)(\d{2,4}).*vrrp.*',item['name'].lower())
        if is_vlan:
            if is_vlan.group(2) in vlans.keys():
                subnet = vlan_ips[is_vlan.group(2)][1]
                vrrp[is_vlan.group(2)] = {'ip': '', 'vrrp': ''}
                vrrp[is_vlan.group(2)]['ip'] = "{}/{}".format(item['address'],subnet)
        if is_vrrp:
            if is_vrrp.group(2) in vlans.keys():
                subnet = vlan_ips[is_vrrp.group(2)][1]
                vrrp[is_vrrp.group(2)]['vrrp'] = "{}/{}".format(item['address'],subnet)
    return vrrp

def main(hostname, username, password):
    new_swicth = dict()
    #hostname = 'ceia6c1'
    hostname = hostname
    #tmp = hash_stuff()
    username = username
    password = password
    #ips = get_switch_ips(hostname,username,password)
    #print(ips)
    #print(parse_switch_ips(hostname,username,password))
    #old = gather_old_switch_info(hostname,username,password)
    #print(f'Getting DNS information for {hostname}')
    dns_info = get_switch_ips(hostname,username,password)
    print(find_new_loopback(dns_info))
    '''#rename_vlan_port_list(old['vlans'])
    
    print('LOCATION')
    print(old['location'])
    print('\nVLAN IP ADDRESSes')
    for k, v in old['ips']['vlan_ips'].items():
        print(f"Vlan{k},{v[0]}\{v[1]}")
    print('\nLOOPBACK IPs')
    for k, v in old['ips']['loopback_ips'].items():
        print(f"Loopback{k},{v[0]}\{v[1]}")
    print('\nVLAN INFO')
    print('Vlan ID,Vlan Name')
    for k, v in old['vlans'].items():
        print(f"{k},{v['name'].upper()}")
    print('\nPort,Description,Vlan,Voice Vlan')
    for k, v in juniper_interfaces.items():
        print(f"{k},{juniper_interfaces[k]['description']},{juniper_interfaces[k]['vlan']},{juniper_interfaces[k]['voice']}")
        #if 'xe' not in k:
        #    if juniper_interfaces[k]['description'] is not None:
        #        print(f"set interfaces {k} description \"{juniper_interfaces[k]['description']}\"")
        #    if juniper_interfaces[k]['vlan'] != "PRODUCTION":
        #        print(f"delete interfaces {k} unit 0 family ethernet-switching vlan members")
        #        print(f"set interfaces {k} unit 0 family ethernet-switching vlan members {juniper_interfaces[k]['vlan']}")
            #else:
            #    print(f"{k},{juniper_interfaces[k]['description']},{juniper_interfaces[k]['vlan']},{juniper_interfaces[k]['voice']}")
    print('\nQIP INFO\n')
    for k, v in dns_info.items():
        print(k)
        for key,value in v.items():
            print(f"{key}: {value['ip']} {value['subnet']}")
    print('\nCDP\n')
    print(old['cdp'])'''
if __name__ == "__main__":
    main()
