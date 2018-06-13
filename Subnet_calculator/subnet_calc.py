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

def convertMaskToBinaryTuple(maskString):
	mask_octets = maskString.split('.')
	mask_to_return = []

	if len(mask_octets) == 1:
		mask_bits = int(mask_octets[0])
		
		while mask_bits > 8:
			#python represents binary with 'b's
			mask_to_return.append(bin(2 ** 8 - 1).split('b')[1])
			mask_bits -= 8

		mask_to_return.append(bin(2 ** 8 - 2 ** (8 - mask_bits)).split('b')[1])
		while len(mask_to_return) < 4:
			mask_to_return.append('0'*8)
	else:
		for octet in mask_octets:
			if int(octet) == 0:
				mask_to_return.append('0'*8)
				continue
			mask_to_return.append(bin(int(octet)).split('b')[1])

	return tuple(mask_to_return)

def calc_num_hosts(mask):
	num_of_zeros = mask.count('0')
	num_of_ones = 32 - num_of_zeros

	return abs(2 ** num_of_zeros - 2)


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
				mask_binary_octets = convertMaskToBinaryTuple(subnet_mask)
				break
			else:
				print('\nThe mask is INVALID. Retry please!\n')

		print(ip_addr)
		print(mask_binary_octets)
		
		joined_mask = ''.join(mask_binary_octets)


		print(f'Number of hosts {calc_num_hosts(joined_mask)}')

	except KeyboardInterrupt:
		print('\n\nProgram aborted by user. Exitting...\n')
		sys.exit()
	except Exception as e:
		# printException()
		exc_info = sys.exc_info()
		traceback.print_exception(*exc_info)

subnet_calc()