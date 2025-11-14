import os
from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_currency_to_rubles


class TestConvertCurrencyToRubles:
    """Тесты для функции convert_currency_to_rubles."""

    def test_convert_rub_to_rubles(self) -> None:
        """Проверка конвертации RUB (должна вернуть сумму как есть)."""
        transaction = {
            "operationAmount": {
                "amount": "100.50",
                "currency": {"code": "RUB"},
            },
        }

        with patch.dict(os.environ, {"API_KEY_CURRENCY": "test_key"}):
            result = convert_currency_to_rubles(transaction)
            assert result == 100.50
            assert isinstance(result, float)

    def test_convert_usd_to_rubles(self) -> None:
        """Проверка конвертации USD через API."""
        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {"code": "USD"},
            },
        }

        # Мокируем ответ API
        mock_response = Mock()
        mock_response.json.return_value = {"result": 7500.0}
        mock_response.raise_for_status = Mock()

        with patch.dict(os.environ, {"API_KEY_CURRENCY": "test_key"}):
            with patch("src.external_api.requests.get", return_value=mock_response):
                result = convert_currency_to_rubles(transaction)
                assert result == 7500.0
                assert isinstance(result, float)

    def test_convert_eur_to_rubles(self) -> None:
        """Проверка конвертации EUR через API."""
        transaction = {
            "operationAmount": {
                "amount": "50.0",
                "currency": {"code": "EUR"},
            },
        }

        # Мокируем ответ API
        mock_response = Mock()
        mock_response.json.return_value = {"result": 5000.0}
        mock_response.raise_for_status = Mock()

        with patch.dict(os.environ, {"API_KEY_CURRENCY": "test_key"}):
            with patch("src.external_api.requests.get", return_value=mock_response):
                result = convert_currency_to_rubles(transaction)
                assert result == 5000.0
                assert isinstance(result, float)

    def test_missing_api_key(self) -> None:
        """Проверка обработки отсутствующего API ключа."""
        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {"code": "USD"},
            },
        }

        # Мокируем load_dotenv, чтобы он не загружал переменные из .env
        with patch("src.external_api.load_dotenv"):
            with patch.dict(os.environ, {}, clear=True):
                with pytest.raises(ValueError, match="API_KEY_CURRENCY не установлен"):
                    convert_currency_to_rubles(transaction)

    def test_missing_operation_amount(self) -> None:
        """Проверка обработки отсутствующего поля operationAmount."""
        transaction: Dict[str, Any] = {}

        with patch.dict(os.environ, {"API_KEY_CURRENCY": "test_key"}):
            with pytest.raises(KeyError, match="operationAmount"):
                convert_currency_to_rubles(transaction)

    def test_missing_amount_field(self) -> None:
        """Проверка обработки отсутствующего поля amount."""
        transaction = {
            "operationAmount": {
                "currency": {"code": "RUB"},
            },
        }

        with patch.dict(os.environ, {"API_KEY_CURRENCY": "test_key"}):
            with pytest.raises(KeyError, match="operationAmount.amount"):
                convert_currency_to_rubles(transaction)

    def test_missing_currency_field(self) -> None:
        """Проверка обработки отсутствующего поля currency."""
        transaction = {
            "operationAmount": {
                "amount": "100.0",
            },
        }

        with patch.dict(os.environ, {"API_KEY_CURRENCY": "test_key"}):
            with pytest.raises(KeyError, match="operationAmount.currency"):
                convert_currency_to_rubles(transaction)

    def test_missing_currency_code(self) -> None:
        """Проверка обработки отсутствующего поля currency.code."""
        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {},
            },
        }

        with patch.dict(os.environ, {"API_KEY_CURRENCY": "test_key"}):
            with pytest.raises(KeyError, match="operationAmount.currency.code"):
                convert_currency_to_rubles(transaction)

    def test_invalid_currency(self) -> None:
        """Проверка обработки неподдерживаемой валюты."""
        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {"code": "GBP"},
            },
        }

        with patch.dict(os.environ, {"API_KEY_CURRENCY": "test_key"}):
            with pytest.raises(ValueError, match="Неподдерживаемая валюта"):
                convert_currency_to_rubles(transaction)

    def test_api_request_exception(self) -> None:
        """Проверка обработки ошибки при запросе к API."""
        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {"code": "USD"},
            },
        }

        with patch.dict(os.environ, {"API_KEY_CURRENCY": "test_key"}):
            with patch("src.external_api.requests.get", side_effect=Exception("API недоступен")):
                with pytest.raises(Exception, match="API недоступен"):
                    convert_currency_to_rubles(transaction)

    def test_api_response_missing_result(self) -> None:
        """Проверка обработки ответа API без поля result."""
        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {"code": "USD"},
            },
        }

        mock_response = Mock()
        mock_response.json.return_value = {"error": "Invalid request"}
        mock_response.raise_for_status = Mock()

        with patch.dict(os.environ, {"API_KEY_CURRENCY": "test_key"}):
            with patch("src.external_api.requests.get", return_value=mock_response):
                with pytest.raises(ValueError, match="отсутствует поле 'result'"):
                    convert_currency_to_rubles(transaction)

    def test_invalid_amount_format(self) -> None:
        """Проверка обработки невалидного формата суммы."""
        transaction = {
            "operationAmount": {
                "amount": "not_a_number",
                "currency": {"code": "RUB"},
            },
        }

        with patch.dict(os.environ, {"API_KEY_CURRENCY": "test_key"}):
            with pytest.raises(ValueError, match="Не удалось преобразовать сумму"):
                convert_currency_to_rubles(transaction)


class TestConvertCurrencyToRublesFixtures:
    """Тесты для функции convert_currency_to_rubles с использованием параметризации."""

    @pytest.mark.parametrize(
        "currency_code, amount_str, expected_multiplier",
        [
            ("RUB", "100.0", 1.0),  # RUB не конвертируется
            ("USD", "100.0", 75.0),  # USD конвертируется (мок возвращает 75.0)
            ("EUR", "100.0", 80.0),  # EUR конвертируется (мок возвращает 80.0)
        ],
    )
    def test_convert_various_currencies(self, currency_code: str, amount_str: str, expected_multiplier: float) -> None:
        """Проверка конвертации различных валют с параметризацией."""
        transaction = {
            "operationAmount": {
                "amount": amount_str,
                "currency": {"code": currency_code},
            },
        }

        # Для RUB не нужен мок API
        if currency_code == "RUB":
            with patch.dict(os.environ, {"API_KEY_CURRENCY": "test_key"}):
                result = convert_currency_to_rubles(transaction)
                assert result == float(amount_str) * expected_multiplier
        else:
            # Для USD и EUR мокируем API
            mock_response = Mock()
            expected_result = float(amount_str) * expected_multiplier
            mock_response.json.return_value = {"result": expected_result}
            mock_response.raise_for_status = Mock()

            with patch.dict(os.environ, {"API_KEY_CURRENCY": "test_key"}):
                with patch("src.external_api.requests.get", return_value=mock_response):
                    result = convert_currency_to_rubles(transaction)
                    assert result == expected_result

    @pytest.mark.parametrize(
        "missing_field, error_type, error_message",
        [
            ("operationAmount", KeyError, "operationAmount"),
            ("amount", KeyError, "operationAmount.amount"),
            ("currency", KeyError, "operationAmount.currency"),
        ],
    )
    def test_missing_fields(self, missing_field: str, error_type: type, error_message: str) -> None:
        """Проверка обработки отсутствующих полей с параметризацией."""
        transaction: Dict[str, Any] = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {"code": "RUB"},
            },
        }

        # Удаляем нужное поле
        if missing_field == "operationAmount":
            transaction = {}
        elif missing_field == "amount":
            del transaction["operationAmount"]["amount"]
        elif missing_field == "currency":
            del transaction["operationAmount"]["currency"]

        with patch.dict(os.environ, {"API_KEY_CURRENCY": "test_key"}):
            with pytest.raises(error_type, match=error_message):
                convert_currency_to_rubles(transaction)
