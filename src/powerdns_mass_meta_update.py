#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import argparse
import sys
import json


def api_get_zones(base_url='', api_key=''):
    headers = {'X-API-Key': api_key}
    url = '{}/api/v1/servers/localhost/zones'.format(base_url)
    try:
        r = requests.get(url, headers=headers)
    except Exception as exc:
        print('Error occurred: {}({})'.format(type(exc).__name__, exc))
        return False
    else:
        if r.status_code == 200:
            return r.json()
        else:
            print('Error occurred: Can not get a list of zones')
            return False


def api_get_zone_meta(base_url='', api_key='', zone_name='', meta=''):
    headers = {'X-API-Key': api_key}
    url = '{}/api/v1/servers/localhost/zones/{}'.format(base_url, zone_name)
    try:
        r = requests.get(url, headers=headers)
    except Exception as exc:
        print('Error occurred: {}({})'.format(type(exc).__name__, exc))
        return False
    else:
        if r.status_code == 200:
            return r.json()[meta]
        else:
            print('Error occurred: Can not get zone information')
            return False


def api_update_meta(base_url='', api_key='', zone_name='', soa_edit_api=''):
    headers = {'X-API-Key': api_key}
    payload = {'soa_edit_api': soa_edit_api, 'kind': 'Master'}
    url = '{}/api/v1/servers/localhost/zones/{}'.format(base_url, zone_name)
    try:
        r = requests.put(url, headers=headers, data=json.dumps(payload))
    except Exception as exc:
        print('Error occurred: {}({})'.format(type(exc).__name__, exc))
        return False
    else:
        if r.status_code == 204:
            return True
        else:
            print('Error occurred: Can not update zone "{}"'.format(r.text))
            return False


def create_cli():
    parser = argparse.ArgumentParser(description='Script for mass soa-edit-api meta update')
    parser.add_argument('-a', '--host', type=str, required=True,
                        help='powerdns server api address')
    parser.add_argument('-p', '--port', type=int, default=8081,
                        help='powerdns server api port (defaults to %(default)i)')
    parser.add_argument('-k', '--api-key', type=str, required=True,
                        help='powerdns server api key')
    parser.add_argument('-m', '--soa-edit-api', type=str, required=True,
                        choices=['DEFAULT', 'INCEPTION-INCREMENT', 'INCEPTION-EPOCH', 'INCREMENT-WEEKS', 'INCEPTION', 'INCEPTION-WEEK', 'EPOCH'],
                        help='soa-edit-api value')
    parser.add_argument('--use-ssl', action='store_true',
                        help='use https instead http')
    parser.add_argument('--dry-run', action='store_true',
                        help='read-only mode. just show changes')

    return parser


def main():
    parser = create_cli()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    base_proto = 'https' if args.use_ssl else 'http'

    zones = api_get_zones(base_url='{}://{}:{}'.format(base_proto, args.host, args.port), api_key=args.api_key)
    if not zones:
        sys.exit()

    zones_need_update = []

    for zone in zones:
        if api_get_zone_meta(base_url='{}://{}:{}'.format(base_proto, args.host, args.port), api_key=args.api_key, zone_name=zone['name'], meta='soa_edit_api') != args.soa_edit_api and zone['kind'] == 'Master':
            zones_need_update.append(zone['name'])

    for zone in zones_need_update:
        if args.dry_run:
            print('SOA-EDIT-ZONE must be set to "{}" for zone "{}"'.format(args.soa_edit_api, zone))
        else:
            if api_update_meta(base_url='{}://{}:{}'.format(base_proto, args.host, args.port), api_key=args.api_key, zone_name=zone, soa_edit_api=args.soa_edit_api):
                print('SOA-EDIT-ZONE set to "{}" for zone "{}"'.format(args.soa_edit_api, zone))


if __name__ == '__main__':
    main()
