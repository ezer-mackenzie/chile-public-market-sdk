import pytest
from pydantic import BaseModel

from chile_public_market_sdk.errors import ResponseValidationError
from chile_public_market_sdk.parsers import ResponseParser, decode_json


class ExamplePayload(BaseModel):
    ok: bool


def test_decode_json_accepts_utf8_bom() -> None:
    assert decode_json(b'\xef\xbb\xbf{"ok": true}') == {"ok": True}


def test_decode_json_rejects_invalid_payload() -> None:
    with pytest.raises(ResponseValidationError):
        decode_json(b"<html>error</html>")


def test_response_parser_encapsulates_decoding_and_model_validation() -> None:
    payload = ResponseParser.decode_json(b'{"ok": true}')

    assert ResponseParser.parse_model(ExamplePayload, payload) == ExamplePayload(ok=True)
