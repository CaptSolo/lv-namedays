from lv_namedays import nameday

def test_actual_data():
    """Test the actual data returned by read_namedays."""
    namedays = nameday.read_namedays()

    # Example validations for specific known dates
    assert "01-01" in namedays
    assert "Laimnesis" in namedays["01-01"]

    assert "07-04" in namedays
    assert "Uldis" in namedays["07-04"]

    assert "02-29" in namedays
    assert "–" in namedays["02-29"]

    # Ensure no unexpected keys (validate structure)
    assert all(isinstance(date, str) and isinstance(names, list) for date, names in namedays.items())