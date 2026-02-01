#!/usr/bin/env python3
"""Bulk-update sample env var names to align with Microsoft Agent Framework.

- Adds `from sample_env import ...` to samples that reference AZURE_OPENAI_* legacy vars.
- Rewrites os.environ/os.getenv lookups to call helper functions.

Idempotent-ish: safe to re-run.
"""

from __future__ import annotations

from pathlib import Path
import re

REPL = [
    # Key
    (re.compile(r"os\.environ\[\"AZURE_OPENAI_API_KEY\"\]"), "get_azure_openai_api_key()"),
    (re.compile(r"os\.getenv\(\"AZURE_OPENAI_API_KEY\"\)"), "get_azure_openai_api_key()"),
    # Endpoint
    (re.compile(r"os\.environ\[\"AZURE_OPENAI_API_ENDPOINT\"\]"), "get_azure_openai_endpoint()"),
    (re.compile(r"os\.getenv\(\"AZURE_OPENAI_API_ENDPOINT\"\)"), "get_azure_openai_endpoint()"),
    # Version (legacy)
    (re.compile(r"os\.environ\[\"AZURE_OPENAI_API_VERSION\"\]"), "get_azure_openai_api_version()"),
    (re.compile(r"os\.getenv\(\"AZURE_OPENAI_API_VERSION\"\)"), "get_azure_openai_api_version()"),
    # Model/deployment
    (re.compile(r"os\.environ\[\"AZURE_OPENAI_API_MODEL\"\]"), "get_azure_openai_deployment_name()"),
    (re.compile(r"os\.getenv\(\"AZURE_OPENAI_API_MODEL\"\)"), "get_azure_openai_deployment_name()"),
    # v1 base_url
    (re.compile(r"os\.getenv\(\"AZURE_OPENAI_V1_API_ENDPOINT\"\)"), "get_azure_openai_v1_base_url()"),
    (re.compile(r"os\.environ\[\"AZURE_OPENAI_V1_API_ENDPOINT\"\]"), "get_azure_openai_v1_base_url()"),
]

IMPORT_BLOCK = (
    "from sample_env import (\n"
    "    get_azure_openai_api_key,\n"
    "    get_azure_openai_api_version,\n"
    "    get_azure_openai_endpoint,\n"
    "    get_azure_openai_deployment_name,\n"
    "    get_azure_openai_v1_base_url,\n"
    ")\n"
)


def needs_update(text: str) -> bool:
    return "AZURE_OPENAI_" in text and "from sample_env import" not in text


def add_import(text: str) -> str:
    # Insert after dotenv import if present, else after other imports.
    if "from dotenv import load_dotenv" in text:
        return text.replace("from dotenv import load_dotenv\n", "from dotenv import load_dotenv\n" + IMPORT_BLOCK + "\n", 1)

    # fallback: after last import line
    lines = text.splitlines(keepends=True)
    last_import_idx = -1
    for i, line in enumerate(lines):
        if line.startswith("import ") or line.startswith("from "):
            last_import_idx = i
    if last_import_idx >= 0:
        lines.insert(last_import_idx + 1, "\n" + IMPORT_BLOCK + "\n")
        return "".join(lines)

    return IMPORT_BLOCK + "\n" + text


def rewrite(text: str) -> str:
    for rx, repl in REPL:
        text = rx.sub(repl, text)
    return text


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    py_dir = repo / "python"
    changed = 0

    for path in sorted(py_dir.glob("*.py")):
        original = path.read_text(encoding="utf-8")
        text = original

        if "AZURE_OPENAI_" in text:
            if needs_update(text):
                text = add_import(text)
            text = rewrite(text)

        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1

    print(f"Updated {changed} file(s).")


if __name__ == "__main__":
    main()
