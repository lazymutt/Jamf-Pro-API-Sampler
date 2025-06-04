#!/usr/bin/env python3
import json
import subprocess
import requests
from local_credentials import jamf_user, jamf_password, jamf_hostname

def get_pro_api_token():
    '''
    Fetch a Pro API Bearer Token
    '''
    jamf_test_url = jamf_hostname + "/api/v1/auth/token"
    headers = {'Accept': 'application/json', }
    response = requests.post(url=jamf_test_url, headers=headers, auth=(jamf_user, jamf_password), timeout=10)
    response_json = response.json()

    return response_json['token']


def main():
    '''
    The previous version of the this script was quicker, because you could use the Classic API to directly call for inventory with a UDID.
    That call was deprecated so we have to brute force things. We page through the entire inventory until we find the specific UDID.
    Not awesome.
    '''
    local_hardware_raw = subprocess.check_output(['/usr/sbin/system_profiler', 'SPHardwareDataType', '-json']).decode('utf-8')
    hardware = json.loads(local_hardware_raw)
    local_uuid = hardware['SPHardwareDataType'][0]['platform_UUID']

    pro_api_token = get_pro_api_token()

    total_consumed = 0
    current_page = 0
    page_size = 100
    stop_paging = False

    while not stop_paging:
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + pro_api_token}
        response = requests.get(url=jamf_hostname + "/api/v1/computers-inventory/?section=GENERAL&&page-size=" + str(page_size) + "&page=" + str(current_page), headers=headers, timeout=10)

        response_json = response.json()
        total_computers = response_json["totalCount"]

        clients_raw = response_json['results']
        for client in clients_raw:
            if client['udid'] == local_uuid:
                print(f"JAMF ID: {client['id']}")
                break

        current_page += 1
        total_consumed += len(clients_raw)

        stop_paging = total_computers == total_consumed


if __name__ == '__main__':
    main()
