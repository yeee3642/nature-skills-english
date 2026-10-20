"""Configuration read/write helpers.

Read, write, validate, and back up school.json.
Configuration path: ~/.config/lit-dl/school.json
"""

from __future__ import annotations

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

try:
    import jsonschema  # type: ignore
except ImportError:
    jsonschema = None  # type: ignore

# Configuration path; environment overrides support tests and multiple profiles.
CONFIG_DIR = Path(os.environ.get("LIT_DL_CONFIG_DIR", Path.home() / ".config" / "lit-dl"))
CONFIG_FILE = CONFIG_DIR / "school.json"

# Schema path relative to this module.
SCHEMA_FILE = Path(__file__).resolve().parent.parent / "data" / "school.schema.json"


def load_schema() -> dict[str, Any]:
    """Load the JSON Schema."""
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def config_exists() -> bool:
    """Return whether the configuration file exists."""
    return CONFIG_FILE.exists()


def validate(config: dict[str, Any]) -> list[str]:
    """Validate the configuration against its schema.

    Return validation errors; an empty list indicates success.
    When jsonschema is unavailable, perform basic field checks only.
    """
    errors: list[str] = []

    # Basic field checks without jsonschema.
    if not isinstance(config, dict):
        return ["Configuration must be a JSON object"]
    if "version" not in config:
        errors.append("Missing version field")
    if "school" not in config or "name" not in config.get("school", {}):
        errors.append("Missing school.name field")
    auth = config.get("auth", {})
    if "type" not in auth:
        errors.append("Missing auth.type field")
    if "sso_domain" not in auth or not auth["sso_domain"]:
        errors.append("Missing auth.sso_domain field")
    if not config.get("libraries"):
        errors.append("libraries must not be empty")

    # Optional schema validation.
    if jsonschema is not None and not errors:
        try:
            jsonschema.validate(instance=config, schema=load_schema())
        except jsonschema.ValidationError as e:  # type: ignore
            errors.append(f"Schema validation failed: {e.message}")

    return errors


def load_config() -> Optional[dict[str, Any]]:
    """Read the configuration file.

    Return the configuration mapping, or None when the file is absent.
    Back up malformed JSON and return None.
    """
    if not CONFIG_FILE.exists():
        return None

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        # Back up a corrupt configuration and return None.
        backup = CONFIG_FILE.with_suffix(".json.broken")
        shutil.copy2(CONFIG_FILE, backup)
        try:
            CONFIG_FILE.unlink()
        except OSError:
            pass
        print(f"Corrupt configuration backed up to {backup}; configure again. Error: {e}")
        return None


def save_config(config: dict[str, Any]) -> Path:
    """Write the configuration file.

    Create the directory and supply a configured_at timestamp.
    Return the configuration file path.
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Supply the timestamp.
    if not config.get("school", {}).get("configured_at"):
        config.setdefault("school", {})["configured_at"] = datetime.now().isoformat()

    # Validation.
    errors = validate(config)
    if errors:
        raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    # Restrict file permissions to the owner.
    os.chmod(CONFIG_FILE, 0o600)

    return CONFIG_FILE


def backup_config() -> Optional[Path]:
    """Back up the current configuration; return its path or None if absent."""
    if not CONFIG_FILE.exists():
        return None
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = CONFIG_FILE.with_suffix(f".json.{timestamp}.bak")
    shutil.copy2(CONFIG_FILE, backup)
    return backup


def delete_config() -> bool:
    """Delete the configuration for reconfiguration; report whether it was deleted."""
    if CONFIG_FILE.exists():
        backup_config()
        CONFIG_FILE.unlink()
        return True
    return False


def get_school_name() -> Optional[str]:
    """Return the configured institution name, or None."""
    cfg = load_config()
    if cfg is None:
        return None
    return cfg.get("school", {}).get("name")


def get_auth_info() -> Optional[dict[str, Any]]:
    """Return configured authentication details, or None."""
    cfg = load_config()
    if cfg is None:
        return None
    return cfg.get("auth")


if __name__ == "__main__":
    # CLI self-check.
    if config_exists():
        cfg = load_config()
        if cfg:
            print(f"Configured institution: {cfg.get('school', {}).get('name', 'unknown')}")
            print(f"Configuration path: {CONFIG_FILE}")
            errors = validate(cfg)
            if errors:
                print(f"Validation warnings: {errors}")
            else:
                print("Configuration validation passed")
        else:
            print("Configuration exists but is corrupt; configure again")
    else:
        print(f"Not configured. Configuration path: {CONFIG_FILE}")
