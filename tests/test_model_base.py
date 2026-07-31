import pytest

from chile_public_market_sdk.core.constants.wire_keys import WIRE_KEY_MAP
from chile_public_market_sdk.models.base import ChilePublicMarketModel
from chile_public_market_sdk.models.companies import CompanyResponse


def test_base_model_normalizes_nested_wire_keys_and_preserves_unknown_keys() -> None:
    payload = {
        "Nombre": "Tender",
        "Comprador": {
            "CodigoOrganismo": "123",
            "CustomField": [{"Rut": "76.000.000-0"}],
        },
    }

    assert ChilePublicMarketModel.normalize_payload(payload) == {
        "name": "Tender",
        "buyer": {
            "organization_code": "123",
            "CustomField": [{"tax_id": "76.000.000-0"}],
        },
    }


def test_company_shape_normalization_uses_the_base_model_interface() -> None:
    response = CompanyResponse.model_validate({"CodigoEmpresa": 10, "NombreEmpresa": "Supplier"})

    assert response.companies[0].company_code == 10
    assert response.companies[0].company_name == "Supplier"


def test_wire_key_map_is_immutable() -> None:
    with pytest.raises(TypeError):
        WIRE_KEY_MAP["NewWireKey"] = "new_field"  # type: ignore[index]
