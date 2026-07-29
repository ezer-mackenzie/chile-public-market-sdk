import httpx
import pytest
from pydantic import BaseModel

from chile_public_market_sdk.errors import (
    APIError,
    AuthenticationError,
    NotFoundError,
    ResponseValidationError,
)
from chile_public_market_sdk.parsers import ResponseParser


class ExamplePayload(BaseModel):
    ok: bool


def test_decode_json_accepts_utf8_bom() -> None:
    assert ResponseParser.decode_json(b'\xef\xbb\xbf{"ok": true}') == {"ok": True}


def test_decode_json_rejects_invalid_payload() -> None:
    with pytest.raises(ResponseValidationError):
        ResponseParser.decode_json(b"<html>error</html>")


def test_response_parser_encapsulates_decoding_and_model_validation() -> None:
    payload = ResponseParser.decode_json(b'{"ok": true}')

    assert ResponseParser.parse_model(ExamplePayload, payload) == ExamplePayload(ok=True)


def test_model_validation_error_is_normalized() -> None:
    with pytest.raises(ResponseValidationError, match="ExamplePayload"):
        ResponseParser.parse_model(ExamplePayload, {"ok": "not-a-boolean"})


@pytest.mark.parametrize(
    ("status", "error_type"),
    [(401, AuthenticationError), (403, AuthenticationError), (404, NotFoundError)],
)
def test_response_parser_maps_http_errors(
    status: int,
    error_type: type[APIError],
) -> None:
    response = httpx.Response(
        status,
        json={"errors": [{"codigo": status, "mensaje": "upstream failure"}]},
    )

    with pytest.raises(error_type, match="upstream failure"):
        ResponseParser.decode_response(response)


def test_response_parser_handles_non_json_error_and_nok_success() -> None:
    with pytest.raises(APIError, match="HTTP 500"):
        ResponseParser.decode_response(httpx.Response(500, text="<html>failure</html>"))

    with pytest.raises(APIError, match="logical failure"):
        ResponseParser.decode_response(
            httpx.Response(200, json={"success": "NOK", "error": "logical failure"})
        )
