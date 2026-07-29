"""Shared type aliases used across the SDK."""

from collections.abc import Mapping

import httpx

type QueryParameterValue = str | int | float
type QueryParams = Mapping[str, QueryParameterValue]
type TimeoutValue = float | httpx.Timeout
