"""Тесты для модуля csv_loader."""

from unittest.mock import Mock, patch

from src.csv_loader import load_transactions_from_csv, load_transactions_from_excel


class TestLoadTransactionsFromCsv:
    """Тесты для функции load_transactions_from_csv."""

    @patch("src.csv_loader.pd.read_csv")
    @patch("src.csv_loader.Path")
    def test_load_transactions_from_csv_success(self, mock_path: Mock, mock_read_csv: Mock) -> None:
        """Тест успешного чтения CSV файла."""
        # Arrange
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance
        mock_df = Mock()
        mock_df.to_dict.return_value = [
            {"id": 650703.0, "state": "EXECUTED", "amount": 16210.0, "currency_code": "PEN"},
            {"id": 3598919.0, "state": "EXECUTED", "amount": 29740.0, "currency_code": "COP"},
        ]
        mock_read_csv.return_value = mock_df

        # Act
        result = load_transactions_from_csv("data/transactions.csv")

        # Assert
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 650703
        assert result[0]["amount"] == "16210.0"
        mock_path.assert_called_once_with("data/transactions.csv")
        mock_read_csv.assert_called_once()

    @patch("src.csv_loader.Path")
    def test_load_transactions_from_csv_file_not_found(self, mock_path: Mock) -> None:
        """Тест чтения несуществующего CSV файла."""
        # Arrange
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value = mock_path_instance

        # Act
        result = load_transactions_from_csv("nonexistent.csv")

        # Assert
        assert result == []
        mock_path.assert_called_once_with("nonexistent.csv")

    @patch("src.csv_loader.pd.read_csv")
    @patch("src.csv_loader.Path")
    def test_load_transactions_from_csv_empty_file(self, mock_path: Mock, mock_read_csv: Mock) -> None:
        """Тест чтения пустого CSV файла."""
        # Arrange
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance
        import pandas as pd  # type: ignore[import-untyped]

        mock_read_csv.side_effect = pd.errors.EmptyDataError("No columns to parse from file")

        # Act
        result = load_transactions_from_csv("data/empty.csv")

        # Assert
        assert result == []
        mock_path.assert_called_once()

    @patch("src.csv_loader.pd.read_csv")
    @patch("src.csv_loader.Path")
    def test_load_transactions_from_csv_error(self, mock_path: Mock, mock_read_csv: Mock) -> None:
        """Тест обработки ошибок при чтении CSV файла."""
        # Arrange
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance
        mock_read_csv.side_effect = Exception("Ошибка чтения файла")

        # Act
        result = load_transactions_from_csv("data/invalid.csv")

        # Assert
        assert result == []
        mock_path.assert_called_once()


class TestLoadTransactionsFromExcel:
    """Тесты для функции load_transactions_from_excel."""

    @patch("src.csv_loader.pd.read_excel")
    @patch("src.csv_loader.Path")
    def test_load_transactions_from_excel_success(self, mock_path: Mock, mock_read_excel: Mock) -> None:
        """Тест успешного чтения Excel файла."""
        # Arrange
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance
        mock_df = Mock()
        mock_df.to_dict.return_value = [
            {"id": 650703.0, "state": "EXECUTED", "amount": 16210.0, "currency_code": "PEN"},
            {"id": 3598919.0, "state": "EXECUTED", "amount": 29740.0, "currency_code": "COP"},
        ]
        mock_read_excel.return_value = mock_df

        # Act
        result = load_transactions_from_excel("data/transactions_excel.xlsx")

        # Assert
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 650703
        assert result[0]["amount"] == "16210.0"
        mock_path.assert_called_once_with("data/transactions_excel.xlsx")
        mock_read_excel.assert_called_once_with("data/transactions_excel.xlsx", engine="openpyxl")

    @patch("src.csv_loader.Path")
    def test_load_transactions_from_excel_file_not_found(self, mock_path: Mock) -> None:
        """Тест чтения несуществующего Excel файла."""
        # Arrange
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value = mock_path_instance

        # Act
        result = load_transactions_from_excel("nonexistent.xlsx")

        # Assert
        assert result == []
        mock_path.assert_called_once_with("nonexistent.xlsx")

    @patch("src.csv_loader.pd.read_excel")
    @patch("src.csv_loader.Path")
    def test_load_transactions_from_excel_empty_file(self, mock_path: Mock, mock_read_excel: Mock) -> None:
        """Тест чтения пустого Excel файла."""
        # Arrange
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance
        import pandas as pd  # type: ignore[import-untyped]

        mock_read_excel.side_effect = pd.errors.EmptyDataError("No columns to parse from file")

        # Act
        result = load_transactions_from_excel("data/empty.xlsx")

        # Assert
        assert result == []
        mock_path.assert_called_once()

    @patch("src.csv_loader.pd.read_excel")
    @patch("src.csv_loader.Path")
    def test_load_transactions_from_excel_error(self, mock_path: Mock, mock_read_excel: Mock) -> None:
        """Тест обработки ошибок при чтении Excel файла."""
        # Arrange
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance
        mock_read_excel.side_effect = Exception("Ошибка чтения файла")

        # Act
        result = load_transactions_from_excel("data/invalid.xlsx")

        # Assert
        assert result == []
        mock_path.assert_called_once()
