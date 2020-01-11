from napalm import get_network_driver
import base64
from jinja2 import Environment, FileSystemLoader
import os
import re
from show_command_parsers import parse_arp_table
from show_vlan_parser import parse_vlan_output
from b64_encode import hash_stuff



driver = get_network_driver('ios')

creds = hash_stuff()
switchname = input("enter switch to pull data from: ")
# Connect to the switch and get data
device = driver(hostname=switchname, username=base64.b64decode(creds[0]), password=base64.b64decode(creds[1]))
device.open()
#device_ips = device.get_interfaces_ip()
#device_vlans = device.cli(['show ip arp vrf MAIN'])
arp = device.get_facts()
device.close()
#arp = parse_arp_table(device_vlans)
print(arp)

