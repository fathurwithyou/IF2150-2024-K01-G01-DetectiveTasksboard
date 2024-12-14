import pytest
import pandas as pd
from unittest.mock import patch
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from models.victims import Victims
from io import StringIO


@pytest.fixture
def mock_data():
    # Create mock data as CSV strings
    victims_csv = StringIO(
        "id,nama,foto,nik,usia,jk,hasil_forensik\n"
        "1,Alice,not provided,12345,25,F,None\n"
        "2,Bob,not provided,67890,30,M,DNA Match\n"
        "3,Charlie,not provided,11223,35,M,Blood Analysis\n"
    )
    victim_cases_csv = StringIO(
        "id_victim,id_kasus\n"
        "1,101\n"
        "2,102\n"
        "2,103\n"
        "3,201\n"
    )

    # Load the data into DataFrames
    victims_df = pd.read_csv(victims_csv)
    victim_cases_df = pd.read_csv(victim_cases_csv)

    return {"victims_df": victims_df, "victim_cases_df": victim_cases_df}

@pytest.fixture
def mock_victims(mock_data):
    # Mock the Victims class to use the in-memory data
    class VictimsWithMockedData(Victims):
        def __init__(self, data):
            self.victims_df = data["victims_df"]
            self.cases_df = data["victim_cases_df"]

        def write_victims(self):
            pass  # Overriding to avoid file operations in tests

    return VictimsWithMockedData(mock_data)

def test_get_victims(mock_victims):
    victims = mock_victims.get_victims()
    assert len(victims) == 3  # Should match the number of unique victims
    assert victims.loc[1, "id_kasus"] == [102, 103]  # Bob has 2 cases
    assert victims.loc[2, "id_kasus"] == [201]       # Charlie has 1 case

def test_search_victims(mock_victims):
    victims = mock_victims.search_victims("Alice")
    assert len(victims) == 1
    assert victims.iloc[0]["nama"] == "Alice"

    victims = mock_victims.search_victims("DNA")
    assert len(victims) == 1
    assert victims.iloc[0]["hasil_forensik"] == "DNA Match"

def test_add_victim(mock_victims):
    new_victim = {"id": 4, "nama": "Diana", "foto": "not provided", "nik": "98765", "usia": 28, "jk": "F", "hasil_forensik": "Fingerprint"}
    mock_victims.add_victim(new_victim)

    assert len(mock_victims.victims_df) == 4
    assert mock_victims.get_victim_by_id(4) == new_victim

def test_delete_victim(mock_victims):
    mock_victims.delete_victim(1)

    assert len(mock_victims.victims_df) == 2
    assert mock_victims.get_victim_by_id(1) == {}

def test_update_victim(mock_victims):
    updated_victim = {"id": 2, "nama": "Bob Updated", "foto": "updated.png", "nik": "67891", "usia": 31, "jk": "M", "hasil_forensik": "DNA Updated"}
    mock_victims.update_victim(updated_victim)

    victim = mock_victims.get_victim_by_id(2)
    assert victim["nama"] == "Bob Updated"
    assert victim["foto"] == "updated.png"
    assert victim["nik"] == "67891"

def test_sort_victims(mock_victims):
    mock_victims.victims_df = mock_victims.victims_df.sample(frac=1)
    mock_victims.sort_victims()

    sorted_ids = mock_victims.victims_df["id"].tolist()
    assert sorted_ids == [1, 2, 3]

def test_get_last_victim_id(mock_victims):
    last_id = mock_victims.get_last_victim_id()
    assert last_id == 3
