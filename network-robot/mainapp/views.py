from flask import Flask, url_for, render_template, json, request, flash, redirect
import base64
from .form import SwitchForm, ConfigForm, CustomConfigForm
from mainapp import app
from mainapp.qip_dns_query import get_switch_ips
from mainapp.make_config import rename_cisco_to_junos, create_template
from mainapp.gather_old_info import gather_old_switch_info, gather_dist_info
from datetime import date,datetime
import re

import pdb

DATE = date.today().strftime('%m/%d/%Y')

@app.route('/', methods=['GET','POST'])
@app.route('/home')
def call_find_device():
    form = SwitchForm()
    if form.validate_on_submit():
        hostname = form.hostname.data
        username = base64.b64encode(form.username.data.encode())
        password = base64.b64encode(form.password.data.encode())
        if re.match('^[A-Z,a-z]{3,4}[D,d,C,c]\d.*', hostname):
            return render_template('dist_core.html')
        else:
            old = gather_old_switch_info(hostname, username, password)
            if old == "ERROR":
                return render_template('404.html', error="Error connecting to", hostname=hostname)
              #ips = get_switch_ips(hostname, username, password)
            else:
                new = rename_cisco_to_junos(old)
                ips = get_switch_ips(hostname, username, password)
                return render_template('old_info.html', old=old, new=new, hostname=hostname, ips=ips)
    return render_template('index.html', form=form)

@app.route('/config', methods=['GET','POST'])
def call_config_device():
    form = ConfigForm()
    if form.validate_on_submit():
        hostname = form.hostname.data
        username = base64.b64encode(form.username.data.encode())
        password = base64.b64encode(form.password.data.encode())
        engineer = form.engineer.data
        uplink = form.uplink.data
        license1 = form.license1.data
        old = gather_old_switch_info(hostname, username, password)
        if old == "ERROR":
                return render_template('404.html', error="Error connecting to", hostname=hostname)
        ips = get_switch_ips(hostname, username, password)
        new = rename_cisco_to_junos(old)
        switch = create_template(old, ips)
        data = {'switch': switch, 'date': DATE,
                'engineer': engineer, 'uplink': uplink,
                'license1': license1}
        return render_template('juniper.j2', **data)
    return render_template('config.html', form=form)

@app.route('/vlans', methods=['GET','POST'])
def show_custom_info():
    formy = SwitchForm()
    if formy.validate_on_submit():
        vlans = [{'vlan_id':'948', 'vlan_name':'PTUBE'},{'vlan_id':'603', 'vlan_name':'KRNTRM'},
                {'vlan_id':'876', 'vlan_name':'GLUCOMETERS'},{'vlan_id':'943', 'vlan_name':'HVAC'},
                {'vlan_id':'1', 'vlan_name':'default'},{'vlan_id':'929', 'vlan_name':'Dead-Ports-Society'},
                {'vlan_id':'100', 'vlan_name':'PRODUCTION'}]
        form = CustomConfigForm(vlans=vlans)
        return render_template('vlans.html', form=form)

    return render_template('index.html', form=formy)
