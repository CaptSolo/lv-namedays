import unittest
from unittest.mock import patch
from io import StringIO
from click.testing import CliRunner
from lv_namedays import nameday
import datetime as dt
import json

class TestNameday(unittest.TestCase):

    def setUp(self):
        self.mock_namedays = {
            "01-01": ["Laimnesis", "Solvita", "Solvija"],
            "02-14": ["Valentīns"],
            "07-04": ["Ulvis", "Uldis", "Sandis", "Sandijs"],
            "12-24": ["Ādams", "Ieva"]
        }
        self.mock_json_data = json.dumps(self.mock_namedays)

    @patch("importlib.resources.open_text")
    def test_read_namedays(self, mock_open_text):
        """Test reading the namedays from the JSON file."""
        mock_open_text.return_value.__enter__.return_value = StringIO(self.mock_json_data)
        namedays = nameday.read_namedays()
        self.assertEqual(namedays, self.mock_namedays)

    @patch("lv_namedays.nameday.read_namedays")
    def test_date_command(self, mock_read_namedays):
        """Test the CLI command for displaying name days for a specific date."""
        mock_read_namedays.return_value = self.mock_namedays

        runner = CliRunner()

        # Test with a valid date
        result = runner.invoke(nameday.cli, ["date", "01-01"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("01-01 vārda dienas:", result.output)
        self.assertIn("Laimnesis, Solvita, Solvija", result.output)

        # Test with a date that has no names
        result = runner.invoke(nameday.cli, ["date", "02-29"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Šodien nav neviena vārda diena", result.output)

    @patch("lv_namedays.nameday.read_namedays")
    @patch("lv_namedays.nameday.dt.datetime")
    def test_now_command(self, mock_datetime, mock_read_namedays):
        """Test the CLI command for displaying today's name days."""
        mock_datetime.now.return_value = dt.datetime(2023, 1, 1)
        mock_datetime.now.return_value.strftime.return_value = "01-01"
        mock_read_namedays.return_value = self.mock_namedays

        runner = CliRunner()
        result = runner.invoke(nameday.cli, ["now"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Šodienas vārda dienas:", result.output)
        self.assertIn("Laimnesis, Solvita, Solvija", result.output)

    @patch("lv_namedays.nameday.read_namedays")
    def test_name_command(self, mock_read_namedays):
        """Test the CLI command for finding a name's date."""
        mock_read_namedays.return_value = self.mock_namedays

        runner = CliRunner()

        # Test with a name that exists
        result = runner.invoke(nameday.cli, ["name", "Uldis"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Uldis", result.output)
        self.assertIn("07-04", result.output)

        # Test with a name that does not exist
        result = runner.invoke(nameday.cli, ["name", "John"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Nevarēju atrast vārda dienu:", result.output)
        self.assertIn("John", result.output)


class TestNamedayData(unittest.TestCase):
    def test_actual_data(self):
        """Test the actual data returned by read_namedays."""
        namedays = nameday.read_namedays()

        # Example validations for specific known dates
        self.assertIn("01-01", namedays)
        self.assertIn("Laimnesis", namedays["01-01"])

        self.assertIn("07-04", namedays)
        self.assertIn("Uldis", namedays["07-04"])

        self.assertIn("02-29", namedays)
        self.assertIn("–", namedays["02-29"])

        # Ensure no unexpected keys (validate structure)
        self.assertTrue(all(isinstance(date, str) and isinstance(names, list) for date, names in namedays.items()))


if __name__ == "__main__":
    unittest.main()

