# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

import os as _os

import httpx
import pytest
from httpx import URL

import jarvisbot
from jarvisbot import DEFAULT_TIMEOUT, DEFAULT_MAX_RETRIES


def reset_state() -> None:
    jarvisbot._reset_client()
    jarvisbot.api_key = None or "My API Key"
    jarvisbot.organization = None
    jarvisbot.base_url = None
    jarvisbot.timeout = DEFAULT_TIMEOUT
    jarvisbot.max_retries = DEFAULT_MAX_RETRIES
    jarvisbot.default_headers = None
    jarvisbot.default_query = None
    jarvisbot.http_client = None
    jarvisbot.api_type = _os.environ.get("OPENAI_API_TYPE")  # type: ignore
    jarvisbot.api_version = None
    jarvisbot.azure_endpoint = None
    jarvisbot.azure_ad_token = None
    jarvisbot.azure_ad_token_provider = None


@pytest.fixture(autouse=True)
def reset_state_fixture() -> None:
    reset_state()


def test_base_url_option() -> None:
    assert jarvisbot.base_url is None
    assert jarvisbot.completions._client.base_url == URL("https://api.jarvisbot.ai/v1/")

    jarvisbot.base_url = "http://foo.com"

    assert jarvisbot.base_url == URL("http://foo.com")
    assert jarvisbot.completions._client.base_url == URL("http://foo.com")


def test_timeout_option() -> None:
    assert jarvisbot.timeout == jarvisbot.DEFAULT_TIMEOUT
    assert jarvisbot.completions._client.timeout == jarvisbot.DEFAULT_TIMEOUT

    jarvisbot.timeout = 3

    assert jarvisbot.timeout == 3
    assert jarvisbot.completions._client.timeout == 3


def test_max_retries_option() -> None:
    assert jarvisbot.max_retries == jarvisbot.DEFAULT_MAX_RETRIES
    assert jarvisbot.completions._client.max_retries == jarvisbot.DEFAULT_MAX_RETRIES

    jarvisbot.max_retries = 1

    assert jarvisbot.max_retries == 1
    assert jarvisbot.completions._client.max_retries == 1


def test_default_headers_option() -> None:
    assert jarvisbot.default_headers == None

    jarvisbot.default_headers = {"Foo": "Bar"}

    assert jarvisbot.default_headers["Foo"] == "Bar"
    assert jarvisbot.completions._client.default_headers["Foo"] == "Bar"


def test_default_query_option() -> None:
    assert jarvisbot.default_query is None
    assert jarvisbot.completions._client._custom_query == {}

    jarvisbot.default_query = {"Foo": {"nested": 1}}

    assert jarvisbot.default_query["Foo"] == {"nested": 1}
    assert jarvisbot.completions._client._custom_query["Foo"] == {"nested": 1}


def test_http_client_option() -> None:
    assert jarvisbot.http_client is None

    original_http_client = jarvisbot.completions._client._client
    assert original_http_client is not None

    new_client = httpx.Client()
    jarvisbot.http_client = new_client

    assert jarvisbot.completions._client._client is new_client


import contextlib
from typing import Iterator

from jarvisbot.lib.azure import AzureOpenAI


@contextlib.contextmanager
def fresh_env() -> Iterator[None]:
    old = _os.environ.copy()

    try:
        _os.environ.clear()
        yield
    finally:
        _os.environ.update(old)


def test_only_api_key_results_in_openai_api() -> None:
    with fresh_env():
        jarvisbot.api_type = None
        jarvisbot.api_key = "example API key"

        assert type(jarvisbot.completions._client).__name__ == "_ModuleClient"


def test_azure_api_key_env_without_api_version() -> None:
    with fresh_env():
        jarvisbot.api_type = None
        _os.environ["AZURE_OPENAI_API_KEY"] = "example API key"

        with pytest.raises(
            ValueError,
            match=r"Must provide either the `api_version` argument or the `OPENAI_API_VERSION` environment variable",
        ):
            jarvisbot.completions._client  # noqa: B018


def test_azure_api_key_and_version_env() -> None:
    with fresh_env():
        jarvisbot.api_type = None
        _os.environ["AZURE_OPENAI_API_KEY"] = "example API key"
        _os.environ["OPENAI_API_VERSION"] = "example-version"

        with pytest.raises(
            ValueError,
            match=r"Must provide one of the `base_url` or `azure_endpoint` arguments, or the `AZURE_OPENAI_ENDPOINT` environment variable",
        ):
            jarvisbot.completions._client  # noqa: B018


def test_azure_api_key_version_and_endpoint_env() -> None:
    with fresh_env():
        jarvisbot.api_type = None
        _os.environ["AZURE_OPENAI_API_KEY"] = "example API key"
        _os.environ["OPENAI_API_VERSION"] = "example-version"
        _os.environ["AZURE_OPENAI_ENDPOINT"] = "https://www.example"

        jarvisbot.completions._client  # noqa: B018

        assert jarvisbot.api_type == "azure"


def test_azure_azure_ad_token_version_and_endpoint_env() -> None:
    with fresh_env():
        jarvisbot.api_type = None
        _os.environ["AZURE_OPENAI_AD_TOKEN"] = "example AD token"
        _os.environ["OPENAI_API_VERSION"] = "example-version"
        _os.environ["AZURE_OPENAI_ENDPOINT"] = "https://www.example"

        client = jarvisbot.completions._client
        assert isinstance(client, AzureOpenAI)
        assert client._azure_ad_token == "example AD token"


def test_azure_azure_ad_token_provider_version_and_endpoint_env() -> None:
    with fresh_env():
        jarvisbot.api_type = None
        _os.environ["OPENAI_API_VERSION"] = "example-version"
        _os.environ["AZURE_OPENAI_ENDPOINT"] = "https://www.example"
        jarvisbot.azure_ad_token_provider = lambda: "token"

        client = jarvisbot.completions._client
        assert isinstance(client, AzureOpenAI)
        assert client._azure_ad_token_provider is not None
        assert client._azure_ad_token_provider() == "token"
