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
            "01-02": ["Indulis", "Ivo", "Iva", "Ivis"],
            "01-03": ["Miervaldis", "Miervalda", "Ringolds"],
            "01-04": ["Spodra", "Ilva", "Ilvita"],
            "01-05": ["Sīmanis", "Zintis"],
            "01-06": ["Spulga", "Arnita"],
            "01-07": ["Rota", "Zigmārs", "Juliāns", "Digmārs"],
            "02-14": ["Valentīns"],
            "07-04": ["Ulvis", "Uldis", "Sandis", "Sandijs"],
            "12-24": ["Ādams", "Ieva"]
        }
        self.mock_json_data = json.dumps(self.mock_namedays)

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
    def test_date_invalid(self, mock_read_namedays):
        """
        Test the CLI command with an invalid date format.
        """
        mock_read_namedays.return_value = self.mock_namedays

        runner = CliRunner()

        result = runner.invoke(nameday.cli, ["date", "13-32"])
        self.assertIn("Incorrect date format", result.output)

        result = runner.invoke(nameday.cli, ["date", "1332"])
        self.assertIn("Incorrect date format", result.output)

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

        # Test case insensitive search
        result = runner.invoke(nameday.cli, ["name", "uldis"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("uldis", result.output)
        self.assertIn("07-04", result.output)

        # Test with a name that does not exist
        result = runner.invoke(nameday.cli, ["name", "John"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Nevarēju atrast vārda dienu:", result.output)
        self.assertIn("John", result.output)

    @patch("lv_namedays.nameday.read_namedays")
    @patch("click.secho")
    @patch("click.echo")
    def test_print_namedays_for_week(self, mock_echo, mock_secho, mock_read_namedays):
        """Test the print_namedays_for_week function."""
        mock_read_namedays.return_value = self.mock_namedays

        # Call the function with a fixed date
        test_date = dt.datetime(2023, 1, 4).date()
        nameday.print_namedays_for_week(test_date)

        # Expected outputs for the week
        expected_outputs = [
            "01-01 vārda dienas: Laimnesis, Solvita, Solvija",
            "01-02 vārda dienas: Indulis, Ivo, Iva, Ivis",
            "01-03 vārda dienas: Miervaldis, Miervalda, Ringolds",
            "01-04 vārda dienas: Spodra, Ilva, Ilvita",
            "01-05 vārda dienas: Sīmanis, Zintis",
            "01-06 vārda dienas: Spulga, Arnita",
            "01-07 vārda dienas: Rota, Zigmārs, Juliāns, Digmārs"
        ]

        # Assert outputs and bold styling for the current day
        for i, output in enumerate(expected_outputs):
            if i == 3:  # Current day
                mock_secho.assert_any_call(output, bold=True)
            else:
                mock_secho.assert_any_call(output, bold=False)

        # Ensure blank lines are echoed
        mock_echo.assert_any_call()

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