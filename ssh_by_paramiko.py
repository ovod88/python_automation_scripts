#!/usr/bin/python3

import paramiko
import time

ip_address = "192.168.122.151"
username = "ovod88"
password = "taon88"

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip_address,username=username,password=password)

print("Successful connection " + ip_address)

remote_connection = ssh_client.invoke_shell()


remote_connection.send("terminal length 0\n")
remote_connection.send("sh ver\n")
# remote_connection.send("end\n")
time.sleep(3)

output = remote_connection.recv(65535)
print(output.decode('ascii'))

ssh_client.close
