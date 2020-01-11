from flask import Flask, url_for, render_template, json, request, flash, redirect
import base64
from .form import SwitchForm
from mainapp import app
from mainapp.qip_dns_query import get_switch_ips
from mainapp.make_config import rename_cisco_to_junos, create_template
from mainapp.gather_old_info import gather_old_switch_info, gather_dist_info
from datetime import date,datetime
import re

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
            ips = get_switch_ips(hostname, username, password)
            new = rename_cisco_to_junos(old)
            return render_template('old_info.html', old=old, new=new, hostname=hostname)
    return render_template('index.html', form=form)

@app.route('/config')
def call_config_device():
    form = SwitchForm()
    if form.validate_on_submit():
        hostname = form.hostname.data
        username = base64.b64encode(form.username.data.encode())
        password = base64.b64encode(form.password.data.encode())
        old = gather_old_switch_info(hostname, username, password)
        ips = get_switch_ips(hostname, username, password)
        new = rename_cisco_to_junos(old)
        switch = create_template(old, ips)
        return render_template('juniper.j2', switch=switch, date=DATE)
    return render_template('index.html', form=form)


