"""Configuration wizard.

Seven-step interactive configuration flow for agent use.
Each step returns a user prompt and validates the response.

Usage for agents:
    from wizard import Wizard
    w = Wizard()
    # Step 1
    prompt = w.start()                # Return this question to the user.
    # After the user replies:
    result = w.handle_step1(user_input)
    # result = {"next": "step2"|"retry"|"done", "prompt": str, "data": dict}

No institution presets are shipped; users supply names and entry points at runtime.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from urllib.parse import parse_qs, urlparse

from config import save_config, backup_config, delete_config, CONFIG_FILE
from schools_loader import match_school, list_school_names
from validators import (
    KNOWN_DATABASES,
    validate_carsi_entry,
    validate_ezproxy_url,
    validate_libraries,
    validate_school_name,
    validate_sso_domain,
)


def infer_access_from_url(url: str) -> dict[str, Any]:
    """Infer the likely library access route from a user-provided resource URL."""
    raw_url = url.strip()
    parsed = urlparse(raw_url if "://" in raw_url else f"https://{raw_url}")
    host = parsed.netloc.lower()
    path = parsed.path.lower()
    query = parse_qs(parsed.query)
    service = query.get("service", [""])[0]
    service_host = urlparse(service).netloc.lower() if service else ""

    result: dict[str, Any] = {
        "resource_entry": raw_url,
        "entry_host": host,
        "entry_type": "resource_entry",
        "auth_type": "custom",
        "sso_domain": host,
        "service_host": service_host or None,
        "institution_hint": None,
        "notes": "",
    }

    if "metaersp" in host or "metaauth" in host:
        result.update(
            {
                "entry_type": "resource_portal",
                "auth_type": "cas",
                "sso_domain": host,
                "institution_hint": host.split(".", 1)[0] if "." in host else None,
                "notes": "Resource portal; begin here and follow its SSO redirect if needed.",
            }
        )
    elif "/authserver/login" in path or host.startswith("cas."):
        hint = None
        if service_host:
            service_parts = urlparse(service).path.strip("/").split("/")
            if len(service_parts) >= 2:
                hint = service_parts[1]
        result.update(
            {
                "entry_type": "cas_login",
                "auth_type": "cas",
                "sso_domain": host,
                "institution_hint": hint,
                "notes": "CAS login; when service points to a resource portal, return there to access databases.",
            }
        )
    elif "ezproxy" in host or "libproxy" in host:
        result.update({"entry_type": "ezproxy", "auth_type": "custom", "notes": "Library remote-access proxy entry."})
    elif "webvpn" in host or "vpn" in host:
        result.update({"entry_type": "webvpn", "auth_type": "custom", "notes": "WebVPN entry."})
    elif "shibboleth" in path or "carsi" in host:
        result.update({"entry_type": "carsi", "auth_type": "sso", "notes": "CARSI/Shibboleth institutional authentication entry."})

    return result


class Wizard:
    """Configuration wizard state machine.

    State transitions:
        step1 (institution name) ->
            preset match -> step4 (databases) -> step6 (check) -> step7 (save)
            no match -> step2 (CARSI check) -> step3 (SSO domain) -> step4 -> step6 -> step7
                                                   or step5 (EZproxy) -> step6 -> step7
    """

    def __init__(self) -> None:
        self.state: str = "step1"
        self.data: dict[str, Any] = {}
        self.matched_preset: Optional[dict[str, Any]] = None

    # ===== Step 1: Ask for the institution entry. =====
    def start(self) -> str:
        """Return the first-step prompt."""
        self.state = "step1"
        return (
            "Configure your library resource entry before the first institutional download.\n\n"
            "Paste the library electronic-resource or database entry link you normally use.\n"
            "This can be a resource portal, database list, Web of Science entry, database detail page, "
            "or login link that redirects to institutional SSO.\n\n"
            "The wizard infers the CAS/CARSI/EZproxy/WebVPN or resource-portal access route from this link. "
            "This distribution contains no built-in institution names or authentication addresses."
        )

    def handle_step1(self, user_input: str) -> dict[str, Any]:
        """Handle a resource-entry URL; retain institution-preset fallback for non-URL input."""
        value = user_input.strip()
        if not value:
            return {"next": "retry", "prompt": "Input is empty. Paste your library resource or database entry link: "}

        if "://" in value or "." in value:
            inferred = infer_access_from_url(value)
            self.data.update(inferred)
            self.data["school_name"] = inferred.get("institution_hint") or inferred["entry_host"]
            self.data["source"] = "resource_url"
            self.data["auth_type"] = inferred["auth_type"]
            self.data["sso_domain"] = inferred["sso_domain"]
            self.data["carsi_entry"] = inferred["resource_entry"]
            self.data["libraries"] = ["Web of Science", "ScienceDirect", "Springer", "IEEE Xplore", "ACS"]
            self.data["notes"] = inferred.get("notes", "")
            self.data["discovery"] = {"resource_entry_url": inferred["resource_entry"]}
            if inferred["entry_type"] == "resource_portal":
                self.data["discovery"]["resource_portal_url"] = inferred["resource_entry"]
            if inferred.get("service_host"):
                self.data["discovery"]["auth_service_host"] = inferred["service_host"]

            self.state = "step4"
            return {
                "next": "step4",
                "prompt": (
                    "Access route inferred from the resource link:\n"
                    f"  Entry type: {inferred['entry_type']}\n"
                    f"  Authentication type: {inferred['auth_type']}\n"
                    f"  SSO domain: {inferred['sso_domain']}\n"
                    f"  Resource entry: {inferred['resource_entry']}\n\n"
                    "Use this configuration?\n"
                    "  1. Confirm and run the self-check\n"
                    "  2. Edit the database list\n"
                    "  3. Configure manually"
                ),
                "data": {"inferred": inferred},
            }

        name = value

        ok, msg = validate_school_name(name)
        if not ok:
            return {"next": "retry", "prompt": f"{msg}; enter the resource link or institution name again: "}

        # Look up institution presets.
        preset = match_school(name)
        if preset:
            self.matched_preset = preset
            self.data["school_name"] = preset["name"]
            self.data["source"] = "preset"

            # Pre-fill the preset configuration.
            auth = preset.get("auth", {})
            self.data["auth_type"] = auth.get("type", "cas")
            self.data["sso_domain"] = auth.get("sso_domain", "")
            self.data["carsi_entry"] = auth.get("carsi_entry", "")
            self.data["libraries"] = preset.get("libraries", [])
            self.data["notes"] = preset.get("notes", "")

            self.state = "step4"
            return {
                "next": "step4",
                "prompt": (
                    f"Matched institution preset: {preset['name']}\n"
                    f"  Authentication type: {auth.get('type', 'unknown')}\n"
                    f"  SSO domain: {auth.get('sso_domain', 'unknown')}\n"
                    f"  CARSI entry: {auth.get('carsi_entry', 'not configured')}\n"
                    f"  Preset databases: {', '.join(preset.get('libraries', []))}\n\n"
                    "Use the configuration above?\n"
                    "  1. Confirm and finish configuration\n"
                    "  2. Edit the database list\n"
                    "  3. This is not my institution; enter it again"
                ),
                "data": {"matched": preset["name"]},
            }

        # No preset matched; configure manually.
        self.data["school_name"] = name
        self.data["source"] = "manual"
        self.state = "step2"
        return {
            "next": "step2",
            "prompt": (
                f"No preset matched {name}; starting manual configuration.\n\n"
                "Step 2: Does your institution use CARSI federation authentication?\n"
                "(CARSI is an institutional SSO federation: https://www.carsi.edu.cn/)\n\n"
                "  1. Yes, CARSI is available\n"
                "  2. No / unsure; use library remote access (EZproxy)\n"
                "  3. Neither; I connect to the campus VPN"
            ),
        }

    # ===== Step 2: CARSI availability. =====
    def handle_step2(self, user_input: str) -> dict[str, Any]:
        """Handle the CARSI choice."""
        choice = user_input.strip()
        if choice == "1":
            self.data["use_carsi"] = True
            self.state = "step2b"
            return {
                "next": "step2b",
                "prompt": (
                    "Paste your institution CARSI entry URL.\n"
                    "(Find it in the member list at https://www.carsi.edu.cn/; "
                    "for example https://login.university.example/idp/shibboleth; use your actual institution entry.)\n\n"
                    "If unavailable, enter skip and add it later."
                ),
            }
        elif choice == "2":
            self.data["use_carsi"] = False
            self.state = "step3"
            return {
                "next": "step3",
                "prompt": (
                    "You selected library remote access (EZproxy).\n\n"
                    "Step 3: Enter your institution SSO domain.\n"
                    "(For example login.university.example; use the domain shown by your institution.)"
                ),
            }
        elif choice == "3":
            self.data["use_carsi"] = False
            self.data["use_vpn"] = True
            self.state = "step3"
            return {
                "next": "step3",
                "prompt": (
                    "VPN access selected.\n"
                    "Connect to the campus VPN, then enter your institution SSO domain.\n"
                    "(For example login.university.example; use your actual institution domain.)"
                ),
            }
        return {"next": "retry", "prompt": "Enter 1, 2, or 3: "}

    # ===== Step 2b: CARSI entry URL =====
    def handle_step2b(self, user_input: str) -> dict[str, Any]:
        """Handle CARSI entry URL input."""
        url = user_input.strip()
        if url in ("\u8df3\u8fc7", "skip", ""):
            self.data["carsi_entry"] = ""
            self.state = "step3"
            return {
                "next": "step3",
                "prompt": (
                    "Skipped the CARSI entry; you can add it later.\n\n"
                    "Step 3: Enter your institution SSO domain.\n"
                    "(For example login.university.example; use your actual institution domain.)"
                ),
            }

        # Validation.
        ok, msg = validate_carsi_entry(url)
        if not ok:
            return {
                "next": "retry",
                "prompt": f"{msg}\n\nEnter the CARSI entry URL again, or enter skip: ",
            }

        self.data["carsi_entry"] = url
        self.state = "step3"
        return {
            "next": "step3",
            "prompt": (
                f"CARSI entry validation passed.\n\n"
                "Step 3: Enter your institution SSO domain.\n"
                "(For example login.university.example; use your actual institution domain.)"
            ),
        }

    # ===== Step 3: SSO domain =====
    def handle_step3(self, user_input: str) -> dict[str, Any]:
        """Handle SSO domain input."""
        domain = user_input.strip()
        if not domain:
            return {"next": "retry", "prompt": "Domain must not be empty; enter it again: "}

        ok, msg = validate_sso_domain(domain)
        if not ok:
            return {
                "next": "retry",
                "prompt": f"{msg}\n\nEnter your institution SSO domain again (for example login.university.example): ",
            }

        self.data["sso_domain"] = domain.split("://")[-1].split("/")[0]
        # Default auth_type to cas if not yet set.
        if "auth_type" not in self.data:
            self.data["auth_type"] = "cas"

        # Handle the EZproxy route.
        if not self.data.get("use_carsi", True) and not self.data.get("use_vpn"):
            self.state = "step5"
            return {
                "next": "step5",
                "prompt": (
                    f"SSO domain validation passed: {msg}\n\n"
                    "Step 5: Enter your library EZproxy login URL.\n"
                    "(Your library may require enabling remote-access permission before using EZproxy.)\n\n"
                    "If unsure, enter skip and add it later."
                ),
            }

        self.state = "step4"
        return {
            "next": "step4",
            "prompt": (
                f"SSO domain validation passed: {msg}\n\n"
                "Step 4: Which databases do you use?\n"
                f"Options: {', '.join(KNOWN_DATABASES[:10])} ...\n\n"
                "Enter database names separated by commas or spaces: "
            ),
        }

    # ===== Step 4: Database selection. =====
    def handle_step4(self, user_input: str) -> dict[str, Any]:
        """Handle database selection."""
        if user_input.strip() in ("\u786e\u8ba4", "1", "ok", "yes", "\u597d"):
            # Confirm the institution preset.
            if not self.data.get("libraries"):
                return {"next": "retry", "prompt": "Enter database names: "}
        else:
            # Parse input.
            libs = [s.strip() for s in user_input.replace(",", " ").split() if s.strip()]
            if libs:
                self.data["libraries"] = libs

        ok, msg = validate_libraries(self.data.get("libraries", []))
        if not ok:
            return {"next": "retry", "prompt": f"{msg}; enter it again: "}

        self.state = "step6"
        return {
            "next": "step6",
            "prompt": (
                f"Recorded {len(self.data['libraries'])} databases.\n\n"
                "Step 6: Running the connectivity self-check..."
            ),
        }

    # ===== Step 5: EZproxy URL =====
    def handle_step5(self, user_input: str) -> dict[str, Any]:
        """Handle EZproxy URL input."""
        url = user_input.strip()
        if url in ("\u8df3\u8fc7", "skip", ""):
            self.data["ezproxy_url"] = None
            self.state = "step4"
            return {
                "next": "step4",
                "prompt": (
                    "Skipped EZproxy.\n\n"
                    "Step 4: Which databases do you use?\n"
                    "Enter database names separated by commas or spaces: "
                ),
            }

        ok, msg = validate_ezproxy_url(url)
        if not ok:
            return {
                "next": "retry",
                "prompt": f"{msg}\n\nEnter the EZproxy URL again, or enter skip: ",
            }

        self.data["ezproxy_url"] = url
        self.state = "step4"
        return {
            "next": "step4",
            "prompt": (
                f"EZproxy validation passed: {msg}\n\n"
                "Step 4: Which databases do you use?\n"
                "Enter database names separated by commas or spaces: "
            ),
        }

    # ===== Step 6: Connectivity self-check =====
    def handle_step6(self, user_input: str = "") -> dict[str, Any]:
        """Run a connectivity self-check."""
        # Defer the import to avoid circular dependencies.
        from health_check import health_check, clear_cache

        # Save a temporary configuration before running the self-check.
        try:
            temp_config = self._build_config()
        except ValueError as e:
            return {"next": "retry", "prompt": f"Unable to build the configuration: {e}"}

        # Save temporarily for the self-check.
        clear_cache()
        save_config(temp_config)
        result = health_check(force=True)

        self.state = "step7"
        details_text = "\n".join(f"  {d}" for d in result.get("details", []))
        if result["ok"]:
            return {
                "next": "step7",
                "prompt": (
                    f"Connectivity self-check passed:\n{details_text}\n\n"
                    "Step 7: Save this configuration?\n  1. Save\n  2. Reconfigure"
                ),
            }
        else:
            suggestions = "\n".join(f"  {s}" for s in result.get("suggestions", []))
            return {
                "next": "step7",
                "prompt": (
                    f"Connectivity self-check did not fully pass:\n{details_text}\n\n"
                    f"{suggestions}\n\n"
                    "Step 7: How should this proceed?\n"
                    "  1. Save anyway; correct it later\n"
                    "  2. Reconfigure"
                ),
                "data": {"warnings": result.get("details", [])},
            }

    # ===== Step 7: Persistence. =====
    def handle_step7(self, user_input: str) -> dict[str, Any]:
        """Handle final save confirmation."""
        choice = user_input.strip()
        if choice in ("2", "\u91cd\u65b0\u914d\u7f6e", "\u91cd\u65b0"):
            delete_config()
            self.__init__()
            return {"next": "step1", "prompt": self.start()}

        # Save.
        try:
            config = self._build_config()
            # Attach warnings when present.
            if self.data.get("warnings"):
                config["_warnings"] = self.data["warnings"]
            path = save_config(config)
            return {
                "next": "done",
                "prompt": (
                    f"Configured {self.data['school_name']} successfully.\n"
                    f"Configuration file: {path}\n\n"
                    "Literature downloads can now use this configuration. Use /reconfig to change institutions."
                ),
                "data": {"school": self.data["school_name"], "path": str(path)},
            }
        except ValueError as e:
            return {"next": "retry", "prompt": f"Save failed: {e}\nCheck the configuration and retry: "}

    # ===== Dispatch entry point. =====
    def handle(self, user_input: str) -> dict[str, Any]:
        """Dispatch to the handler for the current state."""
        handlers = {
            "step1": self.handle_step1,
            "step2": self.handle_step2,
            "step2b": self.handle_step2b,
            "step3": self.handle_step3,
            "step4": self.handle_step4,
            "step5": self.handle_step5,
            "step6": self.handle_step6,
            "step7": self.handle_step7,
        }
        handler = handlers.get(self.state)
        if handler is None:
            self.state = "step1"
            return {"next": "step1", "prompt": self.start()}
        return handler(user_input)

    # ===== Non-interactive institution-preset configuration. =====
    def configure_from_preset(self, school_name: str) -> dict[str, Any]:
        """Configure an institution preset non-interactively.

        Return the saved configuration mapping; raise ValueError on failure.
        """
        preset = match_school(school_name)
        if not preset:
            raise ValueError(f"Institution preset not found: {school_name}")

        auth = preset.get("auth", {})
        config = {
            "version": 1,
            "school": {
                "name": preset["name"],
                "code": preset.get("aliases", [""])[0] if preset.get("aliases") else None,
                "configured_at": datetime.now().isoformat(),
                "source": "preset",
            },
            "auth": {
                "type": auth.get("type", "cas"),
                "sso_domain": auth.get("sso_domain", ""),
                "carsi_entry": auth.get("carsi_entry") or None,
                "carsi_sp_entity_id": None,
            },
            "proxy": {
                "type": None,
                "ezproxy_url": None,
            },
            "libraries": preset.get("libraries", []),
            "discovery": preset.get("discovery", {}),
            "notes": preset.get("notes", ""),
        }

        path = save_config(config)
        return {"config": config, "path": str(path)}

    # ===== Non-interactive resource-entry configuration. =====
    def configure_from_resource_url(self, resource_url: str) -> dict[str, Any]:
        """Configure from a library resource portal or authentication URL."""
        inferred = infer_access_from_url(resource_url)
        self.data.update(inferred)
        self.data["school_name"] = inferred.get("institution_hint") or inferred["entry_host"]
        self.data["source"] = "resource_url"
        self.data["auth_type"] = inferred["auth_type"]
        self.data["sso_domain"] = inferred["sso_domain"]
        self.data["carsi_entry"] = inferred["resource_entry"]
        self.data["libraries"] = ["Web of Science", "ScienceDirect", "Springer", "IEEE Xplore", "ACS"]
        self.data["notes"] = inferred.get("notes", "")
        self.data["discovery"] = {"resource_entry_url": inferred["resource_entry"]}
        if inferred["entry_type"] == "resource_portal":
            self.data["discovery"]["resource_portal_url"] = inferred["resource_entry"]
        if inferred.get("service_host"):
            self.data["discovery"]["auth_service_host"] = inferred["service_host"]

        config = self._build_config()
        path = save_config(config)
        return {"config": config, "path": str(path), "inferred": inferred}

    # ===== Internal configuration builder. =====
    def _build_config(self) -> dict[str, Any]:
        """Build the configuration mapping from wizard responses."""
        if not self.data.get("school_name"):
            raise ValueError("Institution name is missing")
        if not self.data.get("sso_domain"):
            raise ValueError("SSO domain is missing")
        if not self.data.get("libraries"):
            raise ValueError("Database list is missing")

        return {
            "version": 1,
            "school": {
                "name": self.data["school_name"],
                "code": None,
                "configured_at": datetime.now().isoformat(),
                "source": self.data.get("source", "manual"),
            },
            "auth": {
                "type": self.data.get("auth_type", "cas"),
                "sso_domain": self.data["sso_domain"],
                "carsi_entry": self.data.get("carsi_entry") or None,
                "carsi_sp_entity_id": None,
            },
            "proxy": {
                "type": "ezproxy" if self.data.get("ezproxy_url") else None,
                "ezproxy_url": self.data.get("ezproxy_url") or None,
            },
            "libraries": self.data["libraries"],
            "discovery": self.data.get("discovery", {}),
            "notes": self.data.get("notes", ""),
        }


if __name__ == "__main__":
    # Non-interactive configuration example.
    w = Wizard()
    try:
        result = w.configure_from_preset("Example University")
        print(f"Configured successfully: {result['config']['school']['name']}")
        print(f"Configuration file: {result['path']}")
    except ValueError as e:
        print(f"Configuration failed: {e}")
        print(f"Configuration file path: {CONFIG_FILE}")
