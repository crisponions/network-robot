import re
import pdb

def parse_cdp_neighbors(cdp_neigh):
    cdp_neighbors = dict()
    for line in cdp_neigh['show cdp neighbors | exc SEP'].split('\n'):
        neighbor = re.match('^(?:([A-Z,a-z]{3,4}\d.*)|([A-Z,a-z]{3,4}cap.*))\.ohsu\.edu\s+([G,F]\w+\s+\d+\/\d+\/\d+).*([G,F].*)', line)
        if neighbor:
            #print(neighbor.group(3), neighbor.group(1), neighbor.group(4))
            cdp_neighbors[neighbor.group(3)] = [neighbor.group(1), neighbor.group(4)]
    return cdp_neighbors

def parse_cdp_wap_neighbors(cdp_neigh):
    cdp_neighbors = dict()
    wap = None
    for line in cdp_neigh['show cdp neighbors | exc SEP'].split('\n'):
        wap_match = re.match('^([A-Z,a-z]{3,4}cap.*)\.ohsu\.edu.*', line)
        wap_match_port = re.match('\s*([G,F]\w+\s+\d+\/\d+\/\d+).*([G,F].*)', line)
        if wap_match:
            #print(neighbor.group(3), neighbor.group(1), neighbor.group(4))
            #cdp_neighbors[neighbor.group(3)] = [neighbor.group(1), neighbor.group(4)]
            wap = wap_match.group(1)
        elif wap_match_port and wap is not None:
            cdp_neighbors[wap_match_port.group(1)] = [wap, wap_match_port.group(2)]
            wap = None
    return cdp_neighbors

def parse_arp_table(arp_table_output):
    ip_and_mac = dict()
    for line in arp_table_output['show ip arp vrf MAIN'].split('\n'):
        host_match = re.match('^Internet\s+(\d+\.\d+\.\d+\.\d+).*([A-Za-z0-9]{4}\.[A-Za-z0-9]{4}\.[A-Za-z0-9]{4}|Incomplete)\s+ARPA\s+(?:Vlan(\d+))?',line)
        if host_match:
            ip_and_mac[host_match.group(1)] = {'mac': host_match.group(2)}
            if host_match.group(2).lower() != "incomplete":
                ip_and_mac[host_match.group(1)]['vlan'] =  host_match.group(3)
    return ip_and_mac

def parse_switch_stack_count(stack_output):
    member_count = 0
    for line in stack_output['show switch | inc \d'].split('\n'):
        temp_count = re.match('(?:\s|\*)(\d)\s*', line)
        if temp_count:
            if int(temp_count.group(1)) >= member_count:
                
                member_count = int(temp_count.group(1))
    return member_count

def parse_location(location_output):
    closet = re.match('snmp-server\slocation\s(.*)', location_output['sh run | inc snmp-server location'])
    if closet:
        return closet.group(1)
    else:
        return None
def parse_onoff_hill(helper_output):
    NS1 = '137.53.223.44'
    NS2 = '137.53.223.36'
    for line in helper_output['show run | inc helper-address'].split('\n'):
        ns = re.match('.*\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
        if ns:
            if ns.group(1) == NS1:
                return 'NS1'
            else:
                return 'NS2'


def parse_show_run_interface(interface_output):
    interfaces = {}
    for line in interface_output['sh run | inc Ethernet|^ switchport access vlan|^ switchport voice vlan'].split('\n'):
        interface_match = re.match('^interface\s(.*Ethernet)(\d+\/\d+\/\d+)',line)
        vlan_match = re.match('\sswitchport\saccess\svlan\s(\d+)',line)
        voice_match = re.match('\sswitchport\svoice\svlan\s(\d+)',line)

        if interface_match:
            interface_name = interface_match.group(1) + interface_match.group(2)
            interfaces[interface_name] = dict()
        elif vlan_match:
            interfaces[interface_name]['vlan'] = vlan_match.group(1)
        elif voice_match:
            interfaces[interface_name]['voice'] = voice_match.group(1)
            
    return interfaces