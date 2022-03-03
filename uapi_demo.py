#!/usr/bin/env python3

import requests
from local_credentials import jamf_user, jamf_password, jamf_hostname


def get_uapi_token():

    jamf_test_url = jamf_hostname + "/api/v1/auth/token"
    headers = {'Accept': 'application/json', }
    response = requests.post(url=jamf_test_url, headers=headers, auth=(jamf_user, jamf_password))
    response_json = response.json()

    return response_json['token']


def invalidate_uapi_token(uapi_token):

    jamf_test_url = jamf_hostname + "/api/v1/auth/invalidate-token"
    headers = {'Accept': '*/*', 'Authorization': 'Bearer ' + uapi_token}
    response = requests.post(url=jamf_test_url, headers=headers)

    if response.status_code == 204:
        print('Token invalidated!')
    else:
        print('Error invalidating token.')


def main():

    # fetch Jamf Pro (ex-universal) api token
    uapi_token = get_uapi_token()

    # fetch sample Jamf Pro api call
    headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + uapi_token}
    response = requests.get(url=jamf_hostname + "/api/v1/jamf-pro-version", headers=headers)
    response_json = response.json()

    print(response_json['version'])

    # invalidating token
    print('invalidating token...')
    invalidate_uapi_token(uapi_token)


if __name__ == '__main__':
    main()
