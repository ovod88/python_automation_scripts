#!/usr/bin/python3

import json
from napalm import get_network_driver

driver = get_network_driver('ios')
iosl3 = driver('192.168.122.151', 'ovod88', 'taon88')
iosl3.open()

iosl3_output = iosl3.get_facts()

print(iosl3_output['hostname'])
output = json.dumps(iosl3_output, sort_keys=True, indent=4)
print(output)

# iosl3_output = iosl3.get_interfaces()
# print(json.dumps(iosl3_output, sort_keys=True, indent=4))

# iosl3_output = iosl3.get_interfaces_counters()
# print(json.dumps(iosl3_output, sort_keys=True, indent=4))

iosl3.close()