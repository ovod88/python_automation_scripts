#!/usr/bin/python3
#THIS SCRIPT IS NOT WORKING!!!!!

import json
from napalm import get_network_driver

driver = get_network_driver('ios')
iosl3 = driver('192.168.122.151', 'ovod88', 'taon88')
iosl3.open()

iosl3.load_merge_candidate(filename='ACL.cfg')
iosl3.commit_config()

# iosl3_output = iosl3.get_interfaces()
# print(json.dumps(iosl3_output, sort_keys=True, indent=4))

# iosl3_output = iosl3.get_interfaces_counters()
# print(json.dumps(iosl3_output, sort_keys=True, indent=4))

iosl3.close()