import pytest
from unittest.mock import patch
from lv_namedays import nameday
from lv_namedays.nameday import NameDayDB

def test_actual_data():
    """Test the actual data returned by read_namedays."""
    namedays = nameday.read_namedays()

    # Example validations for specific known dates
    assert "01-01" in namedays
    assert "Laimnesis" in namedays["01-01"]

    assert "07-04" in namedays
    assert "Uldis" in namedays["07-04"]

    assert "02-29" in namedays
    assert "-" in namedays["02-29"]

    assert "05-22" in namedays
    assert "Visu neparasto un kalendāros neierakstīto vārdu diena" in namedays["05-22"]

    # Ensure no unexpected keys (validate structure)
    assert all(isinstance(date, str) and isinstance(names, list) for date, names in namedays.items())

def test_actual_data_extended():
    """Test the actual data from the extended namedays list."""
    namedays = nameday.read_namedays_ext()

    assert "01-01" in namedays
    assert "Afrodīte" in namedays["01-01"]

    assert "07-23" in namedays
    assert "Radomirs" in namedays["07-23"]

    # Ensure no unexpected keys (validate structure)
    assert all(isinstance(date, str) and isinstance(names, list) for date, names in namedays.items())


def test_get_nameday_extended():
    db = NameDayDB()
    assert db.get_date_for_name("Radomirs") is None
    assert db.get_date_for_name("Radomirs", extended=True) == "07-23"


@patch('lv_namedays.nameday.read_namedays')
def test_get_names_for_date(mock_read_namedays, mock_namedays):
    mock_read_namedays.return_value = mock_namedays
    db = NameDayDB()
    assert db.get_names_for_date("01-01") == ["Laimnesis", "Solvita", "Solvija"]
    assert db.get_names_for_date("01-00") is None

@patch('lv_namedays.nameday.read_namedays')
def test_get_date_for_name(mock_read_namedays, mock_namedays):
    mock_read_namedays.return_value = mock_namedays
    db = NameDayDB()
    assert db.get_date_for_name("Laimnesis") == "01-01"
    assert db.get_date_for_name("Ivo") == "01-02"
    assert db.get_date_for_name("Nonexistent") is None

@patch('lv_namedays.nameday.read_namedays')
def test_get_date_for_name_lowercase(mock_read_namedays, mock_namedays):
    mock_read_namedays.return_value = mock_namedays
    db = NameDayDB()
    assert db.get_date_for_name("laimnesis") == "01-01"
    assert db.get_date_for_name("ivo") == "01-02"
