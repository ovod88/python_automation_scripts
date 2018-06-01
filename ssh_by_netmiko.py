#!/usr/bin/python3

from netmiko import ConnectHandler

iosv_l2 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.122.151',
    'username': 'ovod88',
    'password': 'taon88',
}


net_connect = ConnectHandler(**iosv_l2)
#net_connect.find_prompt()
output = net_connect.send_command('show ip int brief')
print(output)

config_commands = ['username test2 password test2']
output = net_connect.send_config_set(config_commands)
print(output)