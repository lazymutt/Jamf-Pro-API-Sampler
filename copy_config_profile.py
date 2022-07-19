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

# Notes ########################################################################
#
# Blanks scope for safety
#
# boils down the payload to an xml file, limiting further editing
#
# Pro API doesn't contain these features yet
#
# I wouldn't use this in production, but it may be a useful starting point
#   for someone
#
#
#
################################################################################

import html
import requests
from local_credentials import jamf_user, jamf_password, jamf_hostname

XML_STRING = ''


def xml_from_dict(data):
    """
    recursively builds xml document from dictionary
    """

    global XML_STRING

    if isinstance(data, list):
        for item in data:
            xml_from_dict(item)
    elif isinstance(data, dict):
        for key, value in data.items():
            XML_STRING += (f"<{key}>")
            if key == 'payloads':
                value = html.escape(value)
            if key == 'scope':
                value = {}
            if key == 'uuid':
                value = ""
            else:
                xml_from_dict(value)
            XML_STRING += (f"</{key}>")
    else:
        XML_STRING += (f"{data}")

    return XML_STRING


def main():
    # Set this value to the ID of the policy you want to experiment with
    test_policy = str(1)

    jamf_test_url = jamf_hostname + "/JSSResource/osxconfigurationprofiles/id/" + test_policy
    headers = {'Accept': 'application/json', }
    response = requests.get(url=jamf_test_url, headers=headers, auth=(jamf_user, jamf_password))

    print("Download: ", response.status_code)
    this_profile = response.json()['os_x_configuration_profile']

    # Adding 'copied' to the name to make it easy to find
    this_profile['general']['id'] = ''
    this_profile['general']['name'] = 'Copied ' + this_profile['general']['name']
    this_profile['self_service']['self_service_display_name'] = 'Copied ' + this_profile['self_service']['self_service_display_name']

    this_xml = '<?xml version="1.0" encoding="UTF-8"?><os_x_configuration_profile>' + xml_from_dict(this_profile) + '</os_x_configuration_profile>'

    # Useful for debugging and seeing what's going on 
#     print()
#     print(this_xml)
#     print()

    # the 0 id in the URL is incredibly important, it tells the JSS to create a new item
    jamf_test_url = jamf_hostname + "/JSSResource/osxconfigurationprofiles/id/" + str(0)
    headers = {'Accept': 'application/xml', }
    response = requests.post(url=jamf_test_url, headers=headers, data=this_xml.encode("utf-8"), auth=(jamf_user, jamf_password))

    # response.text will include the ID of the new profile, or the error text
    print("Upload: ", response.status_code)
    print("Upload: ", response.text)


if __name__ == '__main__':
    main()
