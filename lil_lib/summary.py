import asyncio
import ipaddress
import socket
from dataclasses import dataclass


@dataclass
class ResolveSummary:
    raw_resolves: list[list[tuple[socket.AddressFamily, socket.SocketKind, int, str, tuple[str, int, int, int, ]]]]

    def count_initial_ip_family(self) -> int:
        count_ipv4 = 0
        count_ipv6 = 0
        for resolve in self.raw_resolves:
            # First resolve, ip tuple, ip addr
            curr_ip = ipaddress.ip_address(resolve[0][4][0])
            if isinstance(curr_ip, ipaddress.IPv4Address):
                count_ipv4 += 1
            elif isinstance(curr_ip, ipaddress.IPv6Address):
                count_ipv6 += 1
            else:
                raise Exception("Unknown IP address type!")
        return count_ipv4, count_ipv6

def getaddrinfo_summary(host: str, port: int, attempts: int) -> ResolveSummary:
    resolves = [socket.getaddrinfo(host, port) for _ in range(attempts)]
    return ResolveSummary(resolves)

def getaddrinfo_summary_async(host: str, port: int, attempts: int) -> ResolveSummary:
    async def __async_getaddrinfo(host: str, port: int, attempts: int):
        curr_loop = asyncio.get_event_loop()
        return await asyncio.gather(
            *[curr_loop.getaddrinfo(host, port) for _ in range(attempts)]
        )
    resolves = asyncio.run(__async_getaddrinfo(host, port, attempts))
    return ResolveSummary(resolves)
