#!/usr/bin/env python3
from flask import Flask, render_template, url_for
import socket
import pandas as pd
from sqlalchemy import create_engine

HostName = socket.gethostbyname(socket.gethostname())
app = Flask(__name__)

# Displays pairs of IP addresses and the data flow between them
# Limits rows returned to 3
@app.route('/')
def summary():
  sqlite_engine = create_engine('sqlite:///pcap.db')
  query = ''\
    'select ip_src as Sender_IP, ip_dst as Receiver_IP, sum(length) as TotalBytes from summary '\
    'group by Sender_IP, Receiver_IP '\
    'order by TotalBytes desc '\
    'limit 3'
  totalBytes = pd.read_sql(sql = query, con = sqlite_engine)
  return totalBytes.to_html()
  
# Shows data flow from senders sorted in descending order
@app.route('/topsenders')
def topsenders():
  sqlite_engine = create_engine('sqlite:///capture.db')
  query = ''\
    'select traffic.ip_sender, dns.host_name as host_name_sender, sum(bytes) as total_bytes_sent '\
    'from traffic '\
    'left join dns '\
    'ON traffic.ip_sender = dns.ip_address '\
    'where traffic.ip = 1 '\
    'group by ip_sender '\
    'order by total_bytes_sent desc'
  totalBytes = pd.read_sql(sql = query, con = sqlite_engine)
  return totalBytes.to_html()

# Shows data flow from senders sorted in descending order
@app.route('/topreceivers')
def topreceivers():
  sqlite_engine = create_engine('sqlite:///capture.db')
  query = ''\
    'select traffic.ip_receiver as receiver, dns.host_name as host_name_receiver, sum(bytes) as total_bytes_sent '\
    'from traffic '\
    'left join dns '\
    'ON receiver = dns.ip_address '\
    'where traffic.ip = 1 '\
    'group by receiver '\
    'order by total_bytes_sent desc'
  totalBytes = pd.read_sql(sql = query, con = sqlite_engine)
  return totalBytes.to_html()


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
