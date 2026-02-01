"""Environment variable helpers.

This repo originally used AZURE_OPENAI_API_* environment variables.
Issue #20 requests alignment with Microsoft Agent Framework's `.env.example`.

We support the Agent Framework names *and* keep backwards compatibility.
"""

from __future__ import annotations

import os

from sample_env import (
    get_azure_openai_api_key,
    get_azure_openai_api_version,
    get_azure_openai_endpoint,
    get_azure_openai_deployment_name,
    get_azure_openai_v1_base_url,
)



def _first(*names: str, default: str | None = None) -> str | None:
    for n in names:
        v = os.getenv(n)
        if v is not None and v != "":
            return v
    return default


def get_azure_openai_api_key() -> str:
    # Agent Framework doesn't define a dedicated Azure OpenAI key var, but many samples do.
    v = _first("AZURE_OPENAI_API_KEY", "OPENAI_API_KEY")
    if not v:
        raise KeyError(
            "Missing API key. Set AZURE_OPENAI_API_KEY (Azure OpenAI) or OPENAI_API_KEY."
        )
    return v


def get_azure_openai_endpoint() -> str:
    v = _first("AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_ENDPOINT")
    if not v:
        raise KeyError(
            "Missing endpoint. Set AZURE_OPENAI_ENDPOINT (preferred) or AZURE_OPENAI_API_ENDPOINT."
        )
    return v


def get_azure_openai_api_version() -> str:
    # Only required for the legacy (non-v1) AzureOpenAI client.
    return _first("AZURE_OPENAI_API_VERSION", default="2024-10-21")  # README mentions this as latest GA at time of writing.


def get_azure_openai_deployment_name() -> str:
    v = _first(
        "AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME",
        "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME",
        "AZURE_OPENAI_API_MODEL",
    )
    if not v:
        raise KeyError(
            "Missing deployment name. Set AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME (preferred), "
            "or AZURE_OPENAI_CHAT_DEPLOYMENT_NAME, or legacy AZURE_OPENAI_API_MODEL."
        )
    return v


def get_azure_openai_v1_base_url() -> str:
    # v1 API samples use OpenAI() client with a base_url pointing at the Azure OpenAI v1 endpoint.
    v = _first("AZURE_OPENAI_V1_API_ENDPOINT")
    if v:
        return v
    endpoint = get_azure_openai_endpoint().rstrip("/")
    return f"{endpoint}/openai/v1/"
