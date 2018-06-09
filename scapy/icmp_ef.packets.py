import scapy.all as scapy
import sys
import socket
from multiprocessing.dummy import Pool as ThreadPool

def validate_ip(ip):
	a = ip.split('.')
	if len(a) != 4:
		return False

	for octet in a:
		if not octet.isdigit():
			return False
		i = int(octet)
		if i < 0 or i > 255:
			return False

	return True

def format_to_byte(bit6_value):
	return int('{0:08b}'.format(int(bit6_value,2) << 2), 2)

# print(format_to_byte('010010'))

while True:
	print('Check please allowed parameters')
	try:
		COUNTS = int(raw_input('Enter count number [max 99999, default 10]-> '))
	except ValueError:
		print('Taking default value.....')
		COUNTS = 10
	try:
		INTERVAL = float(raw_input('Enter interval [also possible 0.1 = 100ms, default 2s, max 10s]-> '))
	except ValueError:
		print('Taking default value.....')
		INTERVAL = 2

	sys.stdout.write('Enter ip -> ')
	sys.stdout.flush()
	ip = sys.stdin.readline()
	ip = ip.strip()
	if COUNTS <= 99999 and validate_ip(ip) and INTERVAL <= 10:
		break


NUM_THREADS = 4
MAX_PINGS = NUM_THREADS
QoS_classes_selected = []
QoS_classes_available = {'af11': '001010', 'af12': '001100', 'af13': '001110', 'af21': '010010', 
							'af22': '010100', 'af23': '010110', 'af31': '011010', 'af32': '011100',
							'af33': '011110', 'af41': '100010', 'af42': '100100', 'af43': '100110',
							'cs1': '001000', 'cs2': '010000', 'cs3': '011000', 'cs4': '100000',
							'cs5': '101000', 'cs6': '110000', 'cs7': '111000', 'default': '000000', 
							'ef': '101110'}
menu = """
  Available markers
  ------------------------------------------------------
  af11     Match packets with AF11 dscp (001010)
  af12     Match packets with AF12 dscp (001100)
  af13     Match packets with AF13 dscp (001110)
  af21     Match packets with AF21 dscp (010010)
  af22     Match packets with AF22 dscp (010100)
  af23     Match packets with AF23 dscp (010110)
  af31     Match packets with AF31 dscp (011010)
  af32     Match packets with AF32 dscp (011100)
  af33     Match packets with AF33 dscp (011110)
  af41     Match packets with AF41 dscp (100010)
  af42     Match packets with AF42 dscp (100100)
  af43     Match packets with AF43 dscp (100110)
  cs1      Match packets with CS1(precedence 1) dscp (001000)
  cs2      Match packets with CS2(precedence 2) dscp (010000)
  cs3      Match packets with CS3(precedence 3) dscp (011000)
  cs4      Match packets with CS4(precedence 4) dscp (100000)
  cs5      Match packets with CS5(precedence 5) dscp (101000)
  cs6      Match packets with CS6(precedence 6) dscp (110000)
  cs7      Match packets with CS7(precedence 7) dscp (111000)
  default  Match packets with default dscp (000000)
  ef       Match packets with EF dscp (101110)
"""


while MAX_PINGS:
	print(menu)
	QoS_class = raw_input('Enter QoS class you want to check [no QoS is default] or enter exit to start pings [4 class pings max]-> ')

	if QoS_class.strip() == 'exit':
		break
	elif QoS_class not in QoS_classes_available:
		print('No such class available')
	else:
		QoS_classes_selected.append(QoS_class)

	MAX_PINGS -= 1

def ping(tuple):
	QoS_class = tuple[0]
	packet = tuple[1]
	result = scapy.srloop(packet, count=COUNTS, inter=INTERVAL, verbose=True)
	print('--------RESULT FOR QoS CLASS------'),
	print(QoS_class)
	print(result)
	print('----------------------------------')

threads_list = []
for QoS_class in QoS_classes_selected:
	tos_val = format_to_byte(QoS_classes_available[QoS_class])
	threads_list.append((QoS_class,scapy.IP(dst=ip, tos=tos_val)/scapy.ICMP()))

threads = ThreadPool(NUM_THREADS)
results = threads.map(ping, threads_list)

# pings_normal = scapy.IP(dst=ip)/scapy.ICMP()
# pings_with_ef = scapy.IP(dst=ip, tos=184)/scapy.ICMP()

# scapy.srloop(pings_normal, count=COUNTS)
# scapy.srloop(pings_with_ef, count=COUNTS)
