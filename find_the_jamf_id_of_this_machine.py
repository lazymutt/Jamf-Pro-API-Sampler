#!/usr/local/bin/python3

import re
import subprocess
import requests
from local_credentials import jamf_user, jamf_password, jamf_hostname


def main():
    local_uuid_raw = subprocess.check_output(["system_profiler", "SPHardwareDataType"]).decode('utf-8')
    local_uuid = re.findall(r'Hardware UUID: (.*)', local_uuid_raw)[0]

    print(local_uuid)

    jamf_test_url = jamf_hostname + '/JSSResource/computers/udid/' + local_uuid
    headers = {'Accept': 'application/json', }
    response = requests.get(url=jamf_test_url, headers=headers, auth=(jamf_user, jamf_password))

    if response.status_code == 200:
        response_json = response.json()
        local_jamf_id = response_json['computer']['general']['id']
        print(local_jamf_id)
    else:
        print("Error.")


if __name__ == '__main__':
    main()
