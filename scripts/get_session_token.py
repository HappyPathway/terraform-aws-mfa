#!/usr/bin/env python2.7
from boto import sts, iam
import boto
import os
import json
import sys
from functools import partial

def get_user_name(iam_client):
    _ = iam_client.get_user()
    _ = _.get("get_user_response")
    _ = _.get("get_user_result")
    _ = _.get("user")
    _ = _.get("user_name")
    return _

def get_mfa_devices(iam_client):
    username = get_user_name(iam_client)
    _ = iam_client.get_all_mfa_devices(username)
    _ = _.get("list_mfa_devices_response")
    _ = _.get("list_mfa_devices_result")
    _ = _.get("mfa_devices")[0]
    _ = _.get("serial_number")
    return _

def main():
    module_config = json.loads(sys.stdin.read())
    region = module_config.get("region")
    mfa_token = module_config.get("mfa_token")

    
    # we will conditionally pass variables to aws_client connection function
    # using functools.partial to build up our function call.
    sts_client = sts.connect_to_region(region)
    iam_client = iam.connect_to_region(region)

    session_token = sts_client.get_session_token(
        mfa_token=mfa_token,
        mfa_serial_number=get_mfa_devices(iam_client)
    )

    print json.dumps(session_token.to_dict())

if __name__ == '__main__':
    main()