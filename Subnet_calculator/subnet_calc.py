import sys
import linecache
import traceback

def printException():
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)
	print(f'EXCEPTION IN ({filename}, LINE {lineno} "{line.strip()}": {exc_obj})')

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
	masks = [255, 254, 252, 248, 240, 224, 192, 128, 0]


	if len(mask_octets) == 1 and 1 <= int(mask_octets[0]) <= 32:
		return True
	elif len(mask_octets) == 4 and (int(mask_octets[0]) in masks and int(mask_octets[1]) in masks \
							and int(mask_octets[2]) in masks and int(mask_octets[3]) in masks \
							and (int(mask_octets[0]) >= int(mask_octets[1]) >= int(mask_octets[2]) >= int(mask_octets[3]))):
		pay_attention_to_next_octet = False

		for octet in mask_octets:

			if pay_attention_to_next_octet and int(octet) > 0:
				return False

			if int(octet) < 255:
				pay_attention_to_next_octet = True

		return True
	else:
		return False

def convertMaskToBinary(maskString):
	mask_octets = maskString.split('.')
	mask_to_return = []

	if len(mask_octets) == 1:
		mask_bits = int(mask_octets[0])
		
		while mask_bits > 8:
			#python represents binary with 'b's
			mask_to_return.append(format(2 ** 8 - 1, '08b'))
			mask_bits -= 8

		mask_to_return.append(format(2 ** 8 - 2 ** (8 - mask_bits), '08b'))

		while len(mask_to_return) < 4:
			mask_to_return.append('0'*8)
	else:
		for octet in mask_octets:
			if int(octet) == 0:
				mask_to_return.append('0'*8)
				continue
			mask_to_return.append(format(int(octet), '08b'))
			# mask_to_return.append(bin(int(octet)).split('b')[1])

	# return tuple(mask_to_return)
	return ''.join(mask_to_return)

def calc_num_hosts(mask):
	return abs(2 ** mask.count('0') - 2)

def convertMaskToWildcardBinary(maskString):
	mask_octets = maskString.split('.')
	mask_to_return = []

	for byte in mask_octets:
		wildcard_octet = format(255 - int(byte), '08b')

		mask_to_return.append(wildcard_octet)

	# return tuple(mask_to_return)
	return ''.join(mask_to_return)

def network_addr_calc(ip_addr, mask):
	ip_octets = ip_addr.split('.')
	ip_octets_binary = []

	for octet in ip_octets:
		ip_octets_binary.append(format(int(octet), '08b'))

	ip_binary = ''.join(ip_octets_binary)
	num_of_ones = mask.count('1')
	num_of_zeros = mask.count('0')

	network_address_binary = ip_binary[:num_of_ones] + '0' * num_of_zeros
	broadcast_address_binary = ip_binary[:num_of_ones] + '1' * num_of_zeros

	net_ip_octets = []
	broadcast_ip_octets = []
	for octet in range(0, len(network_address_binary), 8):
		net_ip_octet = network_address_binary[octet:octet + 8]
		net_ip_octets.append(net_ip_octet)
		broadcast_ip_octet = broadcast_address_binary[octet:octet + 8]
		broadcast_ip_octets.append(broadcast_ip_octet)

	ip_address_subnet = []
	broadcast_ip = []
	for octet, octet2 in zip(net_ip_octets, broadcast_ip_octets):
		ip_address_subnet.append(str(int(octet, 2)))
		broadcast_ip.append(str(int(octet2, 2)))		


	# return tuple(ip_to_return)
	return ('.'.join(ip_address_subnet) + '/' + str(num_of_ones), '.'.join(broadcast_ip))

def subnet_calc():
	try:
		while True:
			ip_addr = input('Enter an IP address: ')

			if if_valid_ip(ip_addr):
				print(f'Ip address {ip_addr} is valid')
				break
			else:
				print('\nThe IP address is INVALID. Retry please!\n')

		while True:
			subnet_mask = input('Enter a subnet mask: ')

			if if_valid_mask(subnet_mask):
				print(f'Mask {subnet_mask} is valid')
				mask_binary = convertMaskToBinary(subnet_mask)
				break
			else:
				print('\nThe mask is INVALID. Retry please!\n')

		# print(ip_addr)
		print('Mask ' + mask_binary)


		print(f'Number of hosts {calc_num_hosts(mask_binary)}')

		# print(f'Mask is {joined_mask}')
		
		wildcard_binary = convertMaskToWildcardBinary(subnet_mask)

		print(f'Wildcard mask {wildcard_binary}')

		# print(f'Wildcard mask is {joined_wildcard_mask}')

		subnet_address, broadcast_address = network_addr_calc(ip_addr, mask_binary)

		print('Subnet mask ' + subnet_address)
		print('Broadcast address ' + broadcast_address)

	except KeyboardInterrupt:
		print('\n\nProgram aborted by user. Exitting...\n')
		sys.exit()
	except Exception as e:
		# printException()
		exc_info = sys.exc_info()
		traceback.print_exception(*exc_info)

subnet_calc()