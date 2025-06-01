"""SSRF protection helpers."""
import ipaddress
import socket
import re
from urllib.parse import urlparse
from typing import List, Tuple

PRIVATE_RANGES = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
    ipaddress.IPv4Network("127.0.0.0/8"),
    ipaddress.IPv4Network("169.254.0.0/16"),
]

def is_private_ip(ip_str: str) -> bool:
    try:
        ip = ipaddress.IPv4Address(ip_str)
        return any(ip in net for net in PRIVATE_RANGES)
    except ValueError:
        return False

def validate_replay_target(url: str, allowed_domains: List[str]) -> Tuple[bool, str]:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False, "Only HTTP/HTTPS allowed"

    hostname = parsed.hostname
    if not hostname:
        return False, "Invalid hostname"

    # Resolve IP and block private ranges
    try:
        ip = socket.gethostbyname(hostname)
        if is_private_ip(ip):
            return False, f"Target resolves to private IP: {ip}"
    except socket.gaierror:
        return False, "Hostname resolution failed"

    # Domain allowlist (wildcard patterns)
    if allowed_domains:
        for pattern in allowed_domains:
            regex = "^" + re.escape(pattern).replace("\\*", ".*") + "$"
            if re.match(regex, hostname):
                break
        else:
            return False, "Domain not in allowlist"

    return True, "OK"
