#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2022 Todd McDaniel
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
