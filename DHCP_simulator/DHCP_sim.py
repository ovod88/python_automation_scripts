import subprocess
import logging
import random
import sys

logging.getLogger('scapy.runtime').setLevel(logging. ERROR)
logging.getLogger('scapy.interactive').setLevel(logging. ERROR)
logging.getLogger('scapy.loading').setLevel(logging. ERROR)


import scapy.all as scapy

print('\n Run this script as root \n')

interface = input('Enter interface for sniffing ---> ')

# subprocess.call(['ifconfig', interface, 'promisc'], stdout=None, stderr=None, shell=False)

# print('Interface ' + interface + ' was set to promiscous mode \n')

scapy.conf.checkIPaddr = False#Allows scapy to ignore source IP address (for DHCP it is different with packet sent to DHCP server)

all_given_leases = []
server_id = []
client_mac = []

def generate_DHCP():
	global all_given_leases

	x_id = random.randrange(1, 1000000)
	hw = "00:00:5e" + str(scapy.RandMAC())[8:]
	hw_str = scapy.mac2str(hw)
	# print(hw)
	# print(hw_str)
	dhcp_discover_pkt = scapy.Ether(dst='ff:ff:ff:ff:ff:ff', src=hw) / scapy.IP(src='0.0.0.0', dst='255.255.255.255') / scapy.UDP(sport=68, dport=67) / scapy.BOOTP(op=1, xid=x_id, chaddr=hw_str) / scapy.DHCP(options=[('message-type', 'discover'), ('end')])
	ans, unans = scapy.srp(dhcp_discover_pkt, iface=interface, timeout=2.5, verbose=0)

	# print(ans)
	# print(unans)
	# print(ans.summary())
	# print(ans[0][1][scapy.BOOTP].yiaddr)

	offered_ip = ans[0][1][scapy.BOOTP].yiaddr

	dhcp_request_pkt = scapy.Ether(dst='ff:ff:ff:ff:ff:ff', src=hw) / scapy.IP(src='0.0.0.0', dst='255.255.255.255') / scapy.UDP(sport=68, dport=67) / scapy.BOOTP(op=1, xid=x_id, chaddr=hw_str) / scapy.DHCP(options=[('message-type', 'request'),('requested_addr', offered_ip), ('end')])
	ans, unans = scapy.srp(dhcp_discover_pkt, iface=interface, timeout=2.5, verbose=0)

	# print(ans)
	# print(unans)
	# print(ans.summary())
	# print(ans[0][1][scapy.BOOTP].yiaddr)
	# print(ans[0][1][scapy.IP].src)

	offered_ack_ip = ans[0][1][scapy.BOOTP].yiaddr
	server_ip = ans[0][1][scapy.IP].src

	all_given_leases.append(offered_ack_ip)
	server_id.append(server_ip)
	client_mac.append(hw)

	return all_given_leases, server_id, client_mac

def dhcp_release(ip, hw, server):
	x_id = random.randrange(1, 1000000)
	hw_str = scapy.mac2str(hw)

	dhcp_release_pkt = scapy.IP(src=ip, dst=server) / scapy.UDP(sport=68, dport=67) / scapy.BOOTP(ciaddr=ip, xid=x_id, chaddr=hw_str) / scapy.DHCP(options=[('message-type', 'release'),('server_id', server), ('end')])

	scapy.send(dhcp_release_pkt, verbose=0)

# dhcp_release('10.11.12.12', '00:00:5e:bd:f8:91', '10.11.12.1')

try:
	print('\n Use this tool to: \ns - Simulate DHCP clients\nr - Simulate DHCP release\ne - Exit program\n')
	user_option = input('Enter your choice ')

	if user_option == 's':
		pkt_num = input('\n Enter number of packets to simulate')
		try:
			for _ in range(0, int(pkt_num)):
				generate_DHCP()[0]
		except IndexError:
			print('Error occured. NO DHCP server detected. Check your network settings... ')
			sys.exit()
	elif user_option == 'r':
		try:
			print(all_given_leases)
			print(client_mac)
			print(server_ip)
			for index, ip in enumerate(all_given_leases):
				dhcp_release(ip, client_mac[index], server_ip[index])
		except IndexError:
			print('Release process has failed')
			sys.exit()
	
except KeyboardInterrupt:
	sys.exit(0)
