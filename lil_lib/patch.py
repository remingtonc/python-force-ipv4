import functools
import socket

__orig_getaddrinfo = socket.getaddrinfo

def __hardcode_getaddrinfo_ipv4_override_please_dont_change_syscall_yikes(host, port, family=0, type=0, proto=0, flags=0) -> list[tuple[socket.AddressFamily, socket.SocketKind, int, str, tuple[str, int, int, int, ]]]:
    return __orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

def __hardcode_getaddrinfo_ipv6_override_please_dont_change_syscall_yikes(host, port, family=0, type=0, proto=0, flags=0) -> list[tuple[socket.AddressFamily, socket.SocketKind, int, str, tuple[str, int, int, int, ]]]:
    return __orig_getaddrinfo(host, port, socket.AF_INET6, type, proto, flags)

def __override_getaddrinfo_ipv4(*args, **kwargs) -> list[tuple[socket.AddressFamily, socket.SocketKind, int, str, tuple[str, int, int, int, ]]]:
    try:
        return socket.getaddrinfo(*args, **kwargs, family=socket.AF_INET)
    except TypeError:
        return __hardcode_getaddrinfo_ipv4_override_please_dont_change_syscall_yikes(*args, **kwargs)

def __override_getaddrinfo_ipv6(*args, **kwargs) -> list[tuple[socket.AddressFamily, socket.SocketKind, int, str, tuple[str, int, int, int, ]]]:
    try:
        return socket.getaddrinfo(*args, **kwargs, family=socket.AF_INET6)
    except TypeError:
        return __hardcode_getaddrinfo_ipv6_override_please_dont_change_syscall_yikes(*args, **kwargs)

def patch_ipv4() -> None:
    socket.getaddrinfo = __override_getaddrinfo_ipv4

def patch_ipv6() -> None:
    socket.getaddrinfo = __override_getaddrinfo_ipv6

def patch_orig() -> None:
    global __orig_getaddrinfo
    socket.getaddrinfo = __orig_getaddrinfo
