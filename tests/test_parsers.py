import pytest

from chile_public_market_sdk.errors import ResponseValidationError
from chile_public_market_sdk.parsers import decode_json


def test_decode_json_accepts_utf8_bom() -> None:
    assert decode_json(b'\xef\xbb\xbf{"ok": true}') == {"ok": True}


def test_decode_json_rejects_invalid_payload() -> None:
    with pytest.raises(ResponseValidationError):
        decode_json(b"<html>error</html>")
