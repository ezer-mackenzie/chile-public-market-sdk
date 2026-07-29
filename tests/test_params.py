from datetime import UTC, date, datetime

from chile_public_market_sdk.core.enums import TenderStatus
from chile_public_market_sdk.params import ParameterEncoder


def test_parameter_encoder_encapsulates_wire_formats() -> None:
    assert ParameterEncoder.v1_date(date(2026, 7, 29)) == "29072026"
    assert (
        ParameterEncoder.iso_datetime(datetime(2026, 7, 29, tzinfo=UTC))
        == "2026-07-29T00:00:00Z"
    )
    assert (
        ParameterEncoder.csv_values([TenderStatus.PUBLISHED, TenderStatus.CLOSED])
        == "publicada,cerrada"
    )
    assert ParameterEncoder.compact({"code": "x", "missing": None}) == {"code": "x"}
