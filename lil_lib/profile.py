import logging
from collections.abc import Callable

from .summary import (ResolveSummary, getaddrinfo_summary,
                      getaddrinfo_summary_async)


def __profile(host: str, port: int, attempts: int, profile_method: Callable[[str, int, int], ResolveSummary]) -> None:
    getaddrinfo_summary = profile_method(host, port, attempts)
    count_ipv4, count_ipv6 = getaddrinfo_summary.count_initial_ip_family()
    logging.info("Number of initial IPv4 addresses: %i", count_ipv4)
    logging.info("Number of initial IPv6 addresses: %i", count_ipv6)

def profile_getaddrinfo(host: str = 'ipv4.google.com', port: int = 443, attempts: int = 100) -> None:
    logging.info("Profiling getaddrinfo synchronously ...")
    logging.debug("Profiling %s:%i x %i", host, port, attempts)
    __profile(host, port, attempts, getaddrinfo_summary)

def profile_getaddrinfo_async(host: str ='ipv4.google.com', port: int = 443, attempts: int = 100) -> None:
    logging.info("Profiling getaddrinfo asynchronously ...")
    logging.debug("Profiling %s:%i x %i", host, port, attempts)
    __profile(host, port, attempts, getaddrinfo_summary_async)
