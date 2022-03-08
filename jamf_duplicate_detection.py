#!/usr/local/ec/bin/python3
'''
Part of my JAMF Pro API sampler repo. This script demonstrates pagination.
Python 2/Classic API seen here: https://apple.lib.utah.edu/using-the-jamf-pro-api-and-python-to-detect-duplicated-attributes/
'''
import requests
from local_credentials import jamf_user, jamf_password, jamf_hostname


def parse_jss(uapi_token):
    '''
    pages through all machines in jss, parses computername, udid and serial numbers
    prints collisions
    '''
    total_consumed = 0
    current_page = 0
    page_size = 100
    stop_paging = False

    serial_dict = {}
    udid_dict = {}
    name_dict = {}

    while not stop_paging:
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + uapi_token}
        response = requests.get(url=jamf_hostname + "/uapi/preview/computers?section=GENERAL&page-size=" + str(page_size) + "&page=" + str(current_page) + "&sort=id%3Aasc", headers=headers)
        response_json = response.json()
        total_computers = response_json["totalCount"]

        clients_raw = response_json['results']
        for client in clients_raw:

            try:
                if serial_dict[client['serialNumber']]:
                    serial_dict[client['serialNumber']].append(client['id'])
            except KeyError:
                serial_dict[client['serialNumber']] = [client['id']]

            try:
                if udid_dict[client['udid']]:
                    udid_dict[client['udid']].append(client['id'])
            except KeyError:
                udid_dict[client['udid']] = [client['id']]

            try:
                if name_dict[client['name']]:
                    name_dict[client['name']].append(client['id'])
            except KeyError:
                name_dict[client['name']] = [client['id']]

        current_page += 1
        total_consumed += len(clients_raw)

        stop_paging = (total_computers == total_consumed)

    print("Serial Collisions:")
    for key, value in serial_dict.items():
        if len(value) > 1:
            print(f"[{len(value)}] {key} {value}")

    print("\nUDID Collisions:")
    for key, value in udid_dict.items():
        if len(value) > 1:
            print(f"[{len(value)}] {key} {value}")

    print("\nName Collisions:")
    for key, value in name_dict.items():
        if len(value) > 1:
            print(f"[{len(value)}] {key} {value}")


def get_uapi_token():
    '''
    fetches api token
    '''
    jamf_test_url = jamf_hostname + "/api/v1/auth/token"
    headers = {'Accept': 'application/json', }
    response = requests.post(url=jamf_test_url, headers=headers, auth=(jamf_user, jamf_password))
    response_json = response.json()

    return response_json['token']


def invalidate_uapi_token(uapi_token):
    '''
    invalidates api token
    '''
    jamf_test_url = jamf_hostname + "/api/v1/auth/invalidate-token"
    headers = {'Accept': '*/*', 'Authorization': 'Bearer ' + uapi_token}
    _ = requests.post(url=jamf_test_url, headers=headers)

#     if response.status_code == 204:
#         print('Token invalidated!')
#     else:
#         print('Error invalidating token.')


def main():
    uapi_token = get_uapi_token()

    parse_jss(uapi_token)

    # invalidating token
    print()
    print('invalidating token...')
    invalidate_uapi_token(uapi_token)


if __name__ == '__main__':
    main()
