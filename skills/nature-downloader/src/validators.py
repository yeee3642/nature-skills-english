"""Configuration field validators.

Probe reachability of user-supplied configuration fields:
- sso_domain: DNS resolution + TCP 443 + HTTPS certificate
- carsi_entry: HTTP GET probe
- ezproxy_url: HTTP GET login-form probe

All validators return (ok: bool, message: str).
"""

from __future__ import annotations

import socket
import ssl
import urllib.parse
import urllib.request


def validate_sso_domain(domain: str, timeout: float = 5.0) -> tuple[bool, str]:
    """Validate an SSO domain: DNS resolution + TCP 443 + HTTPS certificate。

    Return (passed, explanatory message).
    """
    domain = domain.strip().lower()
    if not domain:
        return False, "Domain is empty"

    # Remove the protocol prefix.
    for prefix in ("https://", "http://"):
        if domain.startswith(prefix):
            domain = domain[len(prefix):]
    domain = domain.split("/")[0]

    # DNS resolution.
    try:
        addrs = socket.getaddrinfo(domain, 443, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror:
        return False, f"DNS resolution failed: {domain}; check the domain spelling"

    # TCP 443 connection and TLS handshake.
    last_err = ""
    for family, socktype, proto, _, sockaddr in addrs:
        try:
            with socket.create_connection(sockaddr, timeout=timeout) as sock:
                ctx = ssl.create_default_context()
                with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    if cert is None:
                        return False, f"Invalid HTTPS certificate: {domain}"
            return True, f"SSO domain is reachable: https://{domain}"
        except (socket.timeout, ConnectionRefusedError, OSError) as e:
            last_err = str(e)
            continue

    return False, f"Unable to connect to https://{domain} (port 443): {last_err}"


def validate_carsi_entry(url: str, timeout: float = 8.0) -> tuple[bool, str]:
    """Validate a CARSI entry: HTTP GET probe。

    Accept 2xx/3xx responses with CARSI, Shibboleth, or SSO redirect indicators.
    """
    url = url.strip()
    if not url:
        return False, "CARSI entry URL is empty"

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (lit-dl-config-validator)",
                "Accept": "text/html",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            body = resp.read(4096).decode("utf-8", errors="ignore").lower()

            if status >= 400:
                return False, f"CARSI entry returned HTTP {status}"

            # Check content indicators.
            keywords = ["carsi", "shibboleth", "idp", "sso", "login", "\u767b\u5f55", "\u7edf\u4e00\u8eab\u4efd"]
            matched = [k for k in keywords if k in body]
            if matched:
                return True, f"CARSI entry is reachable; detected indicators: {', '.join(matched[:3])}"

            # Accept 3xx redirects that may lead to SSO.
            if 300 <= status < 400:
                location = resp.headers.get("Location", "")
                return True, f"CARSI entry redirects to: {location}"

            return True, f"CARSI entry is reachable (HTTP {status}), but no clear SSO indicator was detected"

    except urllib.error.URLError as e:
        return False, f"CARSI entry is unreachable: {e.reason}"
    except Exception as e:
        return False, f"CARSI entry probe failed: {e}"


def validate_ezproxy_url(url: str, timeout: float = 8.0) -> tuple[bool, str]:
    """Validate an EZproxy URL: HTTP GET login-form probe。

    Check whether the page contains a password input.
    """
    url = url.strip()
    if not url:
        return False, "EZproxy URL is empty"

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (lit-dl-config-validator)",
                "Accept": "text/html",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            body = resp.read(8192).decode("utf-8", errors="ignore").lower()

            if status >= 400:
                return False, f"EZproxy returned HTTP {status}"

            if "password" in body or "\u5bc6\u7801" in body:
                return True, "EZproxy login page is reachable; password input detected"

            return True, f"EZproxy page is reachable (HTTP {status}), but no login form was detected"

    except urllib.error.URLError as e:
        return False, f"EZproxy is unreachable: {e.reason}"
    except Exception as e:
        return False, f"EZproxy probe failed: {e}"


def validate_school_name(name: str) -> tuple[bool, str]:
    """Validate basic institution-name formatting."""
    name = name.strip()
    if len(name) < 2:
        return False, "Institution name is too short"
    if len(name) > 100:
        return False, "Institution name is too long"
    return True, name


def validate_libraries(libraries: list[str]) -> tuple[bool, str]:
    """Validate the database list."""
    if not libraries:
        return False, "Database list must not be empty"
    if len(libraries) > 50:
        return False, "Database list is too long"
    return True, f"Selected {len(libraries)} databases"


# Known database names for wizard selection prompts.
KNOWN_DATABASES = [
    "Web of Science",
    "Scopus",
    "IEEE Xplore",
    "ScienceDirect",
    "Springer Link",
    "Wiley Online Library",
    "ACS Publications",
    "RSC Publishing",
    "Nature",
    "Science",
    "Elsevier ScienceDirect",
    "Taylor & Francis",
    "SAGE Journals",
    "EBSCO",
    "ProQuest",
    "JSTOR",
    "CNKI",
    "Wanfang",
    "VIP",
]


if __name__ == "__main__":
    # Self-check example.
    print("=== SSO domain validation ===")
    ok, msg = validate_sso_domain("login.university.example")
    print(f"  {ok}: {msg}")

    print("\n=== CARSI entry validation ===")
    ok, msg = validate_carsi_entry("https://www.carsi.edu.cn/")
    print(f"  {ok}: {msg}")
