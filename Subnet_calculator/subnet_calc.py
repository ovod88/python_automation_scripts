import sys

def if_valid_ip(ip):
	ip_addr_octets = ip.split('.')
	first_octet = int(ip_addr_octets[0])
	second_octet = int(ip_addr_octets[1])
	third_octet = int(ip_addr_octets[2])
	last_octet = int(ip_addr_octets[3])

	return len(ip_addr_octets) == 4 and (0 <= first_octet <= 223) \
		and first_octet != 127 and (first_octet != 169 or second_octet != 254) \
		and (0 <= second_octet <= 255 and 0 <= third_octet <= 255 and 0 <= last_octet <= 255)


def if_valid_mask(mask):
	mask_octets = mask.split('.')
	
	if len(mask_octets) == 1 and 1 <= mask_octets[0] <= 32:
		return True
	elif 

def subnet_calc():
	try:
		while True:
			ip_addr = input('Enter an IP address: ')

			if if_valid_ip(ip_addr):
				print(f'Ip address {ip_addr} is valid')
				break
			else:
				print('\nThe IP address is INVALID. Retry please!\n')

		# print(f'Ip address {ip_addr} is valid')
		while True:
			subnet_mask = input('Enter a subnet mask: ')

			if if_valid_mask(subnet_mask):
				print(f'Mask {subnet_mask} is valid')
				break
			else:
				print('\nThe mask is INVALID. Retry please!\n')
			

	except KeyboardInterrupt:
		print('\n\nProgram aborted by user. Exitting...\n')
		sys.exit()
	except Exception as e:
		print('Error happened -> ' + str(e))


subnet_calc()