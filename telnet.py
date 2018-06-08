#!/usr/bin/python3

import getpass
import sys
import telnetlib
import time
import datetime
#THERE IS A SCRIPT BY UDEMY COURSE WITH TRY/CATCH AND TIMEOUT

user = input("Enter your telnet username: ")
password = getpass.getpass()
now_time = datetime.datetime.now()
now_time_formatted = now_time.strftime('%Y-%m-%d')

with open('valmy-test.txt', 'r') as file:
	for line in file:
		# HOST = '192.168.122.151'
		HOST = line.split(',')[1].strip()
		hostname = line.split(',')[0].strip()
		tn = telnetlib.Telnet(HOST)
		tn.read_until(b"Username: ")
		tn.write((user + "\n").encode('ascii'))

		if password:
			tn.read_until(b"Password: ")
			tn.write((password + "\n").encode('ascii'))

		# tn.write('write\n'.encode('ascii'))
		tn.write('terminal length 0\n'.encode('ascii'))
		tn.write('show run\n'.encode('ascii'))
# 		# tn.write("conf t\n".encode('ascii'))
		# time.sleep(2)
# 		# tn.write("username test3 password test\n".encode('ascii'))
# 		# tn.write("end\n".encode('ascii'))
		tn.write("exit\n".encode('ascii'))

		config = tn.read_all().decode('ascii')
		# print(config)
		switch_config = open(now_time_formatted + '-' + hostname, 'w')
		switch_config.write(config)
		switch_config.close()
		print('Config written for ' + hostname)
