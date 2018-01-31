==================================================================================
powerdns-mass-meta-update - Script for mass SOA-EDIT-API update on master PowerDNS
==================================================================================


What is this?
*************
This script get local domain zone on Master PowerDNS server by API request.
For each received domain zone with 'Master' kind, the script receives the SOA-EDIT-API meta.
If the zone does not have a SOA-EDIT-API meta, then this option is set


``powerdns-mass-meta-update`` provides an executable called ``powerdns-mass-meta-update``


Installation
************
*on most UNIX-like systems, you'll probably need to run the following*
``install`` *commands as root or by using sudo*

**from source**

::

  pip install git+http://github.com/verdel/powerdns-mass-meta-update

**or**

::

  git clone git://github.com/verdel/powerdns-mass-meta-update
  cd powerdns-mass-meta-update
  python setup.py install

as a result, the ``powerdns-mass-meta-update`` executable will be installed into a system ``bin``
directory

Usage
-----
::

    powerdns-mass-meta-update --help
    usage: powerdns-mass-meta-update [-h] -a HOST [-p PORT] -k API_KEY -m
                                    {DEFAULT,INCEPTION-INCREMENT,INCEPTION-EPOCH,INCREMENT-WEEKS,INCEPTION,INCEPTION-WEEK,EPOCH}
                                    [--use-ssl] [--dry-run]

    Script for mass soa-edit-api meta update

    optional arguments:
      -h, --help            show this help message and exit
      -a HOST, --host HOST  powerdns server api address
      -p PORT, --port PORT  powerdns server api port (defaults to 8081)
      -k API_KEY, --api-key API_KEY
                            powerdns server api key
      -m {DEFAULT,INCEPTION-INCREMENT,INCEPTION-EPOCH,INCREMENT-WEEKS,INCEPTION,INCEPTION-WEEK,EPOCH}, --soa-edit-api {DEFAULT,INCEPTION-INCREMENT,INCEPTION-EPOCH,INCREMENT-WEEKS,INCEPTION,INCEPTION-WEEK,EPOCH}
                            soa-edit-api value
      --use-ssl             use https instead http
      --dry-run             read-only mode. just show changes