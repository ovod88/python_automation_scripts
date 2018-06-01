#!/usr/bin/python3

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

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
    print('Connecting to ' + device['ip'])
    try:
        net_connect = ConnectHandler(**device)
    except (AuthenticationException):
        print('Authentication error to device ' + device['ip'])
        continue
    except (NetMikoTimeoutException):
        print('Timeout error to device ' + device['ip'])
        continue
    except (EOFError):
        print('End of file error while connecting to device ' + device['ip'])
        continue
    except (SSHException):
        print('SSH error while connecting to device ' + device['ip'])
        continue
    except Exception as unkown_error:
        print('Error while connecting to device ' + device['ip'] + str(unkown_error))
        continue

    output = net_connect.send_config_set(lines)
    # output = net_connect.send_command('write mem')
    print(output) 
    print('Device configured')