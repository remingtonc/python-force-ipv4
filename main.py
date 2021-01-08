#!/usr/bin/env python3
import argparse
import logging

from lil_lib import patch, profile


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Attempt to force IPv4 and/or IPv6 address resolution in Python (using normal means).",
        usage="python main.py [host] [port] [attempts] [debug]",
    )
    parser.add_argument("-host", help="hostname to resolve", default="ipv4.google.com", type=str)
    parser.add_argument("-port", help="port of hostname to lookup", default=443, type=int)
    parser.add_argument("-attempts", help="number of attempts to run", default=100, type=int)
    parser.add_argument("-debug", help="debug logging", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    logging.info("Profiling IPv4 ...")
    patch.patch_ipv4()
    profile.profile_getaddrinfo(args.host, args.port, args.attempts)
    profile.profile_getaddrinfo_async(args.host, args.port, args.attempts)
    logging.info("Profiling IPv6 ...")
    patch.patch_ipv6()
    profile.profile_getaddrinfo(args.host, args.port, args.attempts)
    profile.profile_getaddrinfo_async(args.host, args.port, args.attempts)
    logging.info("Profiling default ...")
    patch.patch_orig()
    profile.profile_getaddrinfo(args.host, args.port, args.attempts)
    profile.profile_getaddrinfo_async(args.host, args.port, args.attempts)

if __name__ == '__main__':
    main()
