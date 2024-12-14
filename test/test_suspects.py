import pytest
import pandas as pd
from unittest.mock import patch
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from models.suspects import Suspects
from io import StringIO


@pytest.fixture
def mock_data():
    suspects_csv = StringIO(
        "id,nama,foto,nik,usia,jk,catatan_kriminal\n"
        "1,John Doe,not provided,12345,30,M,None\n"
        "2,Jane Smith,not provided,67890,25,F,Fraud\n"
        "3,Jake Peralta,not provided,11223,35,M,Theft\n"
    )
    suspect_cases_csv = StringIO(
        "id_suspect,id_kasus\n"
        "1,101\n"
        "1,102\n"
        "2,201\n"
        "3,301\n"
    )

    suspects_df = pd.read_csv(suspects_csv)
    suspect_cases_df = pd.read_csv(suspect_cases_csv)

    return {"suspects_df": suspects_df, "suspect_cases_df": suspect_cases_df}

@pytest.fixture
def mock_suspects(mock_data):
    class SuspectsWithMockedData(Suspects):
        def __init__(self, data):
            self.suspects_df = data["suspects_df"]
            self.cases_df = data["suspect_cases_df"]

        def write_suspects(self):
            pass  

    return SuspectsWithMockedData(mock_data)

def test_get_suspects(mock_suspects):
    suspects = mock_suspects.get_suspects()
    assert len(suspects) == 3  
    assert suspects.loc[0, "id_kasus"] == [101, 102] 
    assert suspects.loc[2, "id_kasus"] == [301]       

def test_search_suspects(mock_suspects):
    suspects = mock_suspects.search_suspects("Jane")
    assert len(suspects) == 1
    assert suspects.iloc[0]["nama"] == "Jane Smith"

def test_add_suspect(mock_suspects):
    new_suspect = {"id": 4, "nama": "Rosa Diaz", "foto": "not provided", "nik": "98765", "usia": 29, "jk": "F", "catatan_kriminal": "Assault"}
    mock_suspects.add_suspect(new_suspect)

    assert len(mock_suspects.suspects_df) == 4
    assert mock_suspects.get_suspect_by_id(4) == new_suspect

def test_delete_suspect(mock_suspects):
    mock_suspects.delete_suspect(1)

    assert len(mock_suspects.suspects_df) == 2
    assert mock_suspects.get_suspect_by_id(1) == {}

def test_update_suspect(mock_suspects):
    updated_suspect = {"id": 2, "nama": "Jane Doe", "foto": "updated.png", "nik": "67891", "usia": 26, "jk": "F", "catatan_kriminal": "Updated Fraud"}
    mock_suspects.update_suspect(updated_suspect)

    suspect = mock_suspects.get_suspect_by_id(2)
    assert suspect["nama"] == "Jane Doe"
    assert suspect["foto"] == "updated.png"
    assert suspect["nik"] == "67891"

def test_sort_suspects(mock_suspects):
    mock_suspects.suspects_df = mock_suspects.suspects_df.sample(frac=1)
    mock_suspects.sort_suspects()

    sorted_ids = mock_suspects.suspects_df["id"].tolist()
    assert sorted_ids == [1, 2, 3]

def test_get_last_suspect_id(mock_suspects):
    last_id = mock_suspects.get_last_suspect_id()
    assert last_id == 3
