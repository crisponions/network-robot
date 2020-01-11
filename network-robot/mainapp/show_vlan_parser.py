from napalm import get_network_driver
import base64
import re
import pdb


def parse_vlan_output(vlan_output):
    # Global variables
    vlan_dict = {}
    vlan_id = '1'

    for line in vlan_output['show vlan'].split('\n'):
        """
            This function first splits the screen output by newline,
            then uses a regular expression(s) to extract the vlan id, name and ports.
            This data is the stored as a dictionary, by vlan id, in the 'vlan_dict'
            dictionary.
        """

        # search for vlan id and name.  If found, create a dictionary and add to vlan_dict
        find_vlan = re.match('^(\d+)\s(.*)\s(active|suspended)\s+(.*)', line)
        if find_vlan:
            vlan_id = find_vlan.group(1)
            vlan_dict.update({vlan_id:{'name': find_vlan.group(2).strip(), 'ports': [] }})

        # search for ports in line.  If found, add to ports list
        find_ports = re.findall('\s?.?(((Fa|Gi)(\d+\/)?\d\/\d+),?)', line)
        if find_ports:
            for item in find_ports:
                ports.append(item[1])

            # add port list to vlan id entry
            vlan_dict[vlan_id]['ports'].extend(ports)
        # clear temporary port list
        ports = []
    return vlan_dict
    