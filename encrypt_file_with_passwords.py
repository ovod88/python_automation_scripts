from simplecrypt import encrypt, decrypt
from pprint import pprint
import csv
import json

dc_in_filename = input('\nInput CSV filename (device-creds.txt): ') or 'device-creds.txt'
key = input('Encryption key (cisco): ') or 'cisco'

with open(dc_in_filename, 'r') as dc_in:
    device_creds_reader = csv.reader(dc_in)
    device_creds_list = [device for device in device_creds_reader]

print('\n--------device_creds--------------------')
pprint(device_creds_list)

encrypted_dc_out_file = input('\nOutput encrypted file (encrypted-device-creds): ') or 'encrypted-device-creds'

with open(encrypted_dc_out_file, 'wb') as dc_out:
    dc_out.write(encrypt(key, json.dumps(device_creds_list)))

print('Credentials encrypted')

with open(encrypted_dc_out_file, 'rb') as dc_in:
    device_creds_in = json.loads(decrypt(key, dc_in.read()))

print('\n-------------credentials decrypted--------')
pprint(device_creds_in)
