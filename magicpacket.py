#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Sending WOL magic packet library
"""
import string
import binascii
import socket
import time
import argparse
import logging

__version__ = '2.0.0'
__author__ = __author_email__ = 'chrono-meter@gmx.net'
__license__ = 'PSF'
# __url__ = ''
# http://pypi.python.org/pypi?%3Aaction=list_classifiers
__classifiers__ = [i.strip() for i in '''\
    Development Status :: 5 - Production/Stable
    Intended Audience :: Developers
    Intended Audience :: End Users/Desktop
    License :: OSI Approved :: Python Software Foundation License
    Operating System :: OS Independent
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: 3
    Topic :: Software Development :: Libraries :: Python Modules
    Topic :: System :: Networking
    '''.strip().splitlines()]

logger = logging.getLogger(__name__)


def check_mac_address(source):
    source = binascii.a2b_hex(''.join(
        c for c in source if c in string.hexdigits
    ).encode('ascii'))

    if len(source) != 6:
        raise ValueError('Not a MAC address string: %r' % source)

    return source


def check_address(source):
    # 'IPADDR_OR_FQDN:PORT'
    if ':' in source:
        addr = source.split(':', 1)
        addr[1] = int(addr[1])

    # 'IPADDR_OR_FQDN'
    else:
        addr = source, 7

    return addr


class VerboseAction(argparse._CountAction):

    def __call__(self, parser, namespace, values, option_string=None):
        super().__call__(parser, namespace, values, option_string)
        level = getattr(namespace, self.dest)
        logging.root.setLevel(level=[
            logging.CRITICAL,
            logging.ERROR,
            logging.WARNING,
            logging.INFO,
            logging.DEBUG,
            logging.NOTSET,
        ][level])


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--version', '-V', action='version', version='%%(prog)s %s' % (__version__, ))
    parser.add_argument('--verbose', '-v', action=VerboseAction, default=2, help='increase log level')
    # parser.add_argument('--verbose', '-v', action='count', default=2, help='increase log level')
    parser.add_argument('mac_address', metavar='MAC address', type=check_mac_address)
    parser.add_argument('--destination', '--dest', '-d', type=check_address,
                        default='255.255.255.255:7', metavar='hostname[:port]',
                        help='destination address (default=%(default)s)')
    parser.add_argument('--count', '-c', type=int, default=1, help='repeat count (default=%(default)s)')
    parser.add_argument('--interval', '-i', type=float, default=1.0, metavar='SECONDS',
                        help='interval of repeat (default=%(default)s sec)')

    args = parser.parse_args(argv[1:])

    logger.debug('argument: %s', args)

    packet = b'\xff' * 6 + args.mac_address * 16

    if args.destination[0] == '255.255.255.255':
        # find addresses from bound interfaces
        addr_list = []
        for ifaddr in socket.gethostbyname_ex(socket.gethostname())[2]:
            addr_list.append((ifaddr.rsplit('.', 1)[0] + '.255', args.destination[1]))
    else:
        addr_list = [args.destination, ]

    for i in range(args.count):
        if i > 0:
            logger.info('sleep %s sec', args.interval)
            time.sleep(args.interval)

        for addr in addr_list:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            logger.info('send magic packet for %s via %s:%d',
                        binascii.b2a_hex(args.mac_address).decode().upper(),
                        addr[0],
                        addr[1])
            sock.sendto(packet, tuple(addr))


if __name__ == '__main__':
    import sys
    logging.basicConfig(stream=sys.stdout, format='%(message)s')
    sys.exit(main(sys.argv) or 0)
