#!/usr/bin/env python3
import json
import subprocess
import requests
from local_credentials import jamf_user, jamf_password, jamf_hostname


def main():
    local_hardware_raw = subprocess.check_output(['/usr/sbin/system_profiler', 'SPHardwareDataType', '-json']).decode('utf-8')
    hardware = json.loads(local_hardware_raw)
    local_uuid = hardware['SPHardwareDataType'][0]['platform_UUID']

    jamf_test_url = f'{jamf_hostname}/JSSResource/computers/udid/{local_uuid}'
    headers = {'Accept': 'application/json', }
    response = requests.get(url=jamf_test_url, headers=headers, auth=(jamf_user, jamf_password), timeout=3)

    if response.status_code == 200:
        response_json = response.json()
        local_jamf_id = response_json['computer']['general']['id']
        print(f"JAMF ID: {local_jamf_id}")
    else:
        print("Error.")


if __name__ == '__main__':
    main()
