from simplecrypt import encrypt, decrypt
from pprint import pprint
from netmiko import ConnectHandler
import csv
from time import time
import json
#SCRIPT WITHOUT ERROR HANDLING


def read_devices(filename):
    devices = {}

    with open(filename) as devices_file:
        for device_line in devices_file:
            device_info = device_line.strip().split(',')
            device = {
                'ipaddr': device_info[0],
                'type': device_info[1],
                'name': device_info[2]
            }
            devices[device['ipaddr']]  = device

    print('\n---------devices------------')
    pprint(devices)

    return devices

def read_devices_creds(filename, key):
    print('\n......getting credentials.......\n')
    with open(filename, 'rb') as device_creds_file:
        device_creds_json = decrypt(key, device_creds_file.read())

    device_creds_list = json.loads(device_creds_json)
    device_creds = {dev[0]:dev for dev in device_creds_list}
    pprint(device_creds)

    return device_creds


def config_worker(device, creds):
    if device['type'] == 'junos-srx': device_type = 'juniper'
    elif device['type'] == 'cisco-ios': device_type = 'cisco_ios'
    elif device['type'] == 'cisco-xr': device_type = 'cisco_xr'
    else: device_type = 'cisco_ios' 

    print(f'Connecting to {device["ipaddr"]} with {creds[1]} and {creds[2]}')

    session = ConnectHandler(device_type=device_type, ip=device['ipaddr'],
                                username=creds[1], password=creds[2])

    if device_type == 'juniper':
        print('----------Getting info from Junos---------')
        session.send_command('configure terminal')
        config_data = session.send_command('show configuration')
    elif device_type == 'cisco_ios':
        print('----------Getting info from Cisco IOS---------')
        config_data = session.send_command('show run')
    elif device_type == 'cisco_xr':
        print('----------Getting info from Cisco IOS XR---------')
        config_data = session.send_command('show configuration run')

    config_filename = 'config-' + device['ipaddr']
    print('-------Writing configuration file--------' + config_filename)

    with open(config_filename, 'w') as config_out: 
        config_out.write(config_data)

    session.disconnect()

    return



devices = read_devices('devices-file')
creds = read_devices_creds('encrypted-device-creds', 'cisco')

starting_time = time()

print('\n------------begin get config sequentially----------\n')

for ipaddr, device in devices.items():
    print('Getting config for:' + ipaddr)
    config_worker(device, creds[ipaddr])

print('\n ----- End get config, elapsed time = ' + str(time() - starting_time))

