#!/usr/bin/python3

from netmiko import ConnectHandler

iosv_l2_s1 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.122.151',
    'username': 'ovod88',
    'password': 'taon88',
}

iosv_l2_s2 = {
    'device_type': 'cisco_ios',
    'ip': '10.1.1.2',
    'username': 'ovod88',
    'password': 'taon88',
}

iosv_l2_s3 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.2.254',
    'username': 'ovod88',
    'password': 'taon88',
}

with open('test-commands.txt') as f:
    lines = f.read().splitlines()
print(lines)

all_devices = [iosv_l2_s1, iosv_l2_s2, iosv_l2_s3] 

for device in all_devices:
    net_connect = ConnectHandler(**device)
    # output = net_connect.send_config_set(lines)
    output = net_connect.send_command('write mem')
print(output) 