import json
import os
import tempfile
from typing import Any, Dict, List

import pytest

from src.utils import load_transactions_from_json


class TestLoadTransactionsFromJson:
    """Тесты для функции load_transactions_from_json."""

    def test_load_valid_json_list(self) -> None:
        """Проверка загрузки валидного JSON-файла со списком транзакций."""
        # Создаем временный файл с валидным JSON
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as temp_file:
            transactions = [
                {"id": 1, "amount": 100.0},
                {"id": 2, "amount": 200.0},
            ]
            json.dump(transactions, temp_file)
            temp_path = temp_file.name

        try:
            result = load_transactions_from_json(temp_path)
            assert isinstance(result, list)
            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[1]["id"] == 2
        finally:
            os.unlink(temp_path)

    def test_load_nonexistent_file(self) -> None:
        """Проверка загрузки несуществующего файла."""
        result = load_transactions_from_json("nonexistent_file.json")
        assert result == []

    def test_load_empty_file(self) -> None:
        """Проверка загрузки пустого файла."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            result = load_transactions_from_json(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_load_file_with_dict(self) -> None:
        """Проверка загрузки файла с не-списком (словарем)."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as temp_file:
            data = {"id": 1, "amount": 100.0}
            json.dump(data, temp_file)
            temp_path = temp_file.name

        try:
            result = load_transactions_from_json(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_load_invalid_json(self) -> None:
        """Проверка загрузки файла с невалидным JSON."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as temp_file:
            temp_file.write("{ invalid json }")
            temp_path = temp_file.name

        try:
            result = load_transactions_from_json(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_load_real_operations_file(self) -> None:
        """Проверка загрузки реального файла operations.json."""
        operations_path = "data/operations.json"
        if os.path.exists(operations_path):
            result = load_transactions_from_json(operations_path)
            assert isinstance(result, list)
            assert len(result) > 0
            # Проверяем структуру первой транзакции
            if result:
                assert "id" in result[0]
                assert "operationAmount" in result[0]


class TestLoadTransactionsFromJsonFixtures:
    """Тесты для функции load_transactions_from_json с использованием фикстур и параметризации."""

    @pytest.mark.parametrize(
        "file_content, expected_result",
        [
            ('[{"id": 1}]', [{"id": 1}]),
            ("[]", []),
            ('{"id": 1}', []),  # Не список
            ("invalid json", []),  # Невалидный JSON
        ],
    )
    def test_load_various_json_formats(self, file_content: str, expected_result: List[Dict[str, Any]]) -> None:
        """Проверка загрузки различных форматов JSON."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as temp_file:
            temp_file.write(file_content)
            temp_path = temp_file.name

        try:
            result = load_transactions_from_json(temp_path)
            if expected_result == []:
                assert result == []
            else:
                assert len(result) == len(expected_result)
                assert result[0]["id"] == expected_result[0]["id"]
        finally:
            os.unlink(temp_path)
