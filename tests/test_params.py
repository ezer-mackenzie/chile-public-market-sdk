from datetime import UTC, date, datetime

import pytest

from chile_public_market_sdk.core.enums import TenderStatus
from chile_public_market_sdk.errors import RequestValidationError
from chile_public_market_sdk.params import ParameterEncoder


def test_parameter_encoder_encapsulates_wire_formats() -> None:
    assert ParameterEncoder.v1_date(date(2026, 7, 29)) == "29072026"
    assert (
        ParameterEncoder.iso_datetime(datetime(2026, 7, 29, tzinfo=UTC)) == "2026-07-29T00:00:00Z"
    )
    assert (
        ParameterEncoder.csv_values([TenderStatus.PUBLISHED, TenderStatus.CLOSED])
        == "publicada,cerrada"
    )
    assert ParameterEncoder.compact({"code": "x", "missing": None}) == {"code": "x"}


@pytest.mark.parametrize("value", ["20260729", "31022026", "abcdefgh"])
def test_v1_date_rejects_invalid_values(value: str) -> None:
    with pytest.raises(RequestValidationError):
        ParameterEncoder.v1_date(value)


def test_parameter_encoder_handles_strings_integers_and_invalid_iso_dates() -> None:
    assert ParameterEncoder.enum_value("custom") == "custom"
    assert ParameterEncoder.csv_values([13, 5]) == "13,5"

    with pytest.raises(RequestValidationError, match="ISO-8601"):
        ParameterEncoder.iso_datetime("not-a-date")
