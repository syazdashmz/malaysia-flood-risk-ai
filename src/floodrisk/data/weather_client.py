"""Client utilities for Malaysia weather data from data.gov.my."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


BASE_WEATHER_URL = "https://api.data.gov.my/weather"
USER_AGENT = "malaysia-flood-risk-ai/0.1.0"


def build_weather_url(endpoint: str, params: dict[str, Any] | None = None) -> str:
    """Build a data.gov.my weather API URL."""

    endpoint = endpoint.strip("/")

    if endpoint not in {"forecast", "warning"}:
        msg = f"Unsupported weather endpoint: {endpoint}"
        raise ValueError(msg)

    url = f"{BASE_WEATHER_URL}/{endpoint}"

    if not params:
        return url

    return f"{url}?{urlencode(params)}"


def fetch_json(url: str, timeout_seconds: int = 30) -> Any:
    """Fetch JSON from a URL."""

    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )

    with urlopen(request, timeout=timeout_seconds) as response:
        body = response.read().decode("utf-8")

    return json.loads(body)


def fetch_weather_forecast(
    *,
    limit: int = 100,
    contains: str | None = None,
    timeout_seconds: int = 30,
) -> Any:
    """Fetch 7-day general weather forecast records."""

    params: dict[str, Any] = {"limit": limit}

    if contains:
        params["contains"] = contains

    url = build_weather_url("forecast", params)
    return fetch_json(url, timeout_seconds=timeout_seconds)


def fetch_weather_warnings(
    *,
    limit: int = 100,
    timeout_seconds: int = 30,
) -> Any:
    """Fetch active or recent weather warning records."""

    url = build_weather_url("warning", {"limit": limit})
    return fetch_json(url, timeout_seconds=timeout_seconds)


def save_json(data: Any, output_path: Path) -> Path:
    """Save JSON data to disk."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return output_path
