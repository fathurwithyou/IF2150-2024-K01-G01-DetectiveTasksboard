import pytest
import pandas as pd
from unittest.mock import patch
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from models.detectives import Detective
from io import StringIO


@pytest.fixture
def mock_data():
    # Create mock CSV data in-memory
    detectives_csv = StringIO(
        "id,nama,nik\n"
        "1,Sherlock Holmes,12345\n"
        "2,Hercule Poirot,67890\n"
        "3,Nancy Drew,11223\n"
    )

    detective_cases_csv = StringIO(
        "id_detective,id_kasus\n"
        "1,101\n"
        "1,102\n"
        "2,201\n"
        "3,301\n"
    )

    return {
        "detectives": pd.read_csv(detectives_csv),
        "detective_cases": pd.read_csv(detective_cases_csv),
    }

@pytest.fixture
def mock_detective(mock_data):
    class DetectiveWithMockedData(Detective):
        def __init__(self, data):
            self.detective_df = data["detectives"]
            self.cases_df = data["detective_cases"]

        def write_detectives(self):
            pass

    return DetectiveWithMockedData(mock_data)

def test_get_detectives(mock_detective):
    detectives = mock_detective.get_detectives()
    assert len(detectives) == 3 
    assert detectives.loc[0, "id_kasus"] == [101, 102] 

def test_search_detectives(mock_detective):
    detectives = mock_detective.search_detectives("Poirot")
    assert len(detectives) == 1
    assert detectives.iloc[0]["nama"] == "Hercule Poirot"

def test_add_detective(mock_detective):
    new_detective = {"id": 4, "nama": "Philip Marlowe", "nik": "98765"}
    mock_detective.add_detective(new_detective)

    assert len(mock_detective.detective_df) == 4
    assert mock_detective.get_detective_by_id(4) == new_detective

def test_delete_detective(mock_detective):
    mock_detective.delete_detective(1)

    assert len(mock_detective.detective_df) == 2
    assert mock_detective.get_detective_by_id(1) == {}
    assert len(mock_detective.cases_df[mock_detective.cases_df["id_detective"] == 1]) == 0

def test_update_detective(mock_detective):
    updated_detective = {"id": 2, "nama": "Hercule Poirot", "nik": "67891"}
    mock_detective.update_detective(updated_detective)

    detective = mock_detective.get_detective_by_id(2)
    assert detective["nik"] == "67891"

def test_sort_detectives(mock_detective):
    mock_detective.detective_df = mock_detective.detective_df.sample(frac=1) 
    mock_detective.sort_detectives()

    sorted_ids = mock_detective.detective_df["id"].tolist()
    assert sorted_ids == [1, 2, 3]  

def test_get_last_detective_id(mock_detective):
    last_id = mock_detective.get_last_detective_id()
    assert last_id == 3
