import pytest
from unittest.mock import patch
from click.testing import CliRunner
import datetime as dt

from lv_namedays import cli

@pytest.fixture
def runner():
    return CliRunner()

@patch("lv_namedays.cli.read_namedays")
def test_date_command(mock_read_namedays, runner, mock_namedays):
    """Test the CLI command for displaying name days for a specific date."""
    mock_read_namedays.return_value = mock_namedays

    # Test with a valid date
    result = runner.invoke(cli.cli, ["date", "01-01"])
    assert result.exit_code == 0
    assert "01-01 vārda dienas:" in result.output
    assert "Laimnesis, Solvita, Solvija" in result.output

    # Test with a date that has no names
    result = runner.invoke(cli.cli, ["date", "02-29"])
    assert result.exit_code == 0
    assert "Šodien nav neviena vārda diena" in result.output

@patch("lv_namedays.cli.read_namedays")
def test_date_invalid(mock_read_namedays, runner, mock_namedays):
    """Test the CLI command with an invalid date format."""
    mock_read_namedays.return_value = mock_namedays

    result = runner.invoke(cli.cli, ["date", "13-32"])
    assert "Incorrect date format" in result.output

    result = runner.invoke(cli.cli, ["date", "1332"])
    assert "Incorrect date format" in result.output

@patch("lv_namedays.cli.read_namedays")
@patch("lv_namedays.cli.dt.datetime")
def test_now_command(mock_datetime, mock_read_namedays, runner, mock_namedays):
    """Test the CLI command for displaying today's name days."""
    mock_datetime.now.return_value = dt.datetime(2023, 1, 1)
    mock_datetime.now.return_value.strftime.return_value = "01-01"
    mock_read_namedays.return_value = mock_namedays

    result = runner.invoke(cli.cli, ["now"])
    assert result.exit_code == 0
    assert "Šodienas vārda dienas:" in result.output
    assert "Laimnesis, Solvita, Solvija" in result.output

@patch("lv_namedays.cli.read_namedays")
def test_name_command(mock_read_namedays, runner, mock_namedays):
    """Test the CLI command for finding a name's date."""
    mock_read_namedays.return_value = mock_namedays

    # Test with a name that exists
    result = runner.invoke(cli.cli, ["name", "Uldis"])
    assert result.exit_code == 0
    assert "Uldis" in result.output
    assert "07-04" in result.output

    # Test case insensitive search
    result = runner.invoke(cli.cli, ["name", "uldis"])
    assert result.exit_code == 0
    assert "uldis" in result.output
    assert "07-04" in result.output

    # Test with a name that does not exist
    result = runner.invoke(cli.cli, ["name", "John"])
    assert result.exit_code == 0
    assert "Nevarēju atrast vārda dienu:" in result.output
    assert "John" in result.output

@patch("lv_namedays.cli.read_namedays")
@patch("click.secho")
@patch("click.echo")
def test_print_namedays_for_week(mock_echo, mock_secho, mock_read_namedays, mock_namedays):
    """Test the print_namedays_for_week function."""
    mock_read_namedays.return_value = mock_namedays

    # Call the function with a fixed date
    test_date = dt.datetime(2023, 1, 4).date()
    cli.print_namedays_for_week(test_date)

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