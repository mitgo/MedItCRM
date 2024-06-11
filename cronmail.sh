#!/bin/bash
echo "$(tail -n 40 /var/log/cronmail.log)" > /var/log/cronmail.log
source /opt/MedItCRM/.env && /usr/local/bin/python /opt/MedItCRM/manage.py runcrons &>> /var/log/cronmail.log
