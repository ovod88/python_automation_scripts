from pysnmp.entity.rfc3413.oneliner import cmdgen

def snmp_get(ip):

	print('SNMP GET to -> ' + ip)

	cmdGen = cmdgen.CommandGenerator()

	# errorIndication, errorStatus, errorIndex, varBindNbrTable = cmdGen.nextCmd(cmdgen.CommunityData('public'),
	# 																	cmdgen.UdpTransportTarget((ip, '161')),
	# 																	'1.3.6.1.2.1.14.10.1.3')
	# print(varBindNbrTable)

	# errorIndication, errorStatus, errorIndex, varBindNbrIpTable = cmdGen.nextCmd(cmdgen.CommunityData('public'),
	# 																	cmdgen.UdpTransportTarget((ip, '161')),
	# 																	'1.3.6.1.2.1.14.10.1.1')
	# print(varBindNbrIpTable)

	# errorIndication, errorStatus, errorIndex, varBindHostTable = cmdGen.nextCmd(cmdgen.CommunityData('public'),
	# 																	cmdgen.UdpTransportTarget((ip, '161')),
	# 																	'1.3.6.1.4.1.9.2.1.3')
	# print(varBindHostTable)

	errorIndication, errorStatus, errorIndex, varHostIdTable = cmdGen.nextCmd(cmdgen.CommunityData('public'),
																		cmdgen.UdpTransportTarget((ip, '161')),
																		'1.3.6.1.2.1.14.1.1')
	print(varHostIdTable)

snmp_get('192.168.122.151')