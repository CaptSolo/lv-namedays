import pytest

@pytest.fixture
def mock_namedays():
    return {
        "01-01": ["Laimnesis", "Solvita", "Solvija"],
        "01-02": ["Indulis", "Ivo", "Iva", "Ivis"],
        "01-03": ["Miervaldis", "Miervalda", "Ringolds"],
        "01-04": ["Spodra", "Ilva", "Ilvita"],
        "01-05": ["Sīmanis", "Zintis"],
        "01-06": ["Spulga", "Arnita"],
        "01-07": ["Rota", "Zigmārs", "Juliāns", "Digmārs"],
        "02-14": ["Valentīns"],
        "02-29": ["-"],
        "07-04": ["Ulvis", "Uldis", "Sandis", "Sandijs"],
        "12-24": ["Ādams", "Ieva"]
    }