import os
import pandas as pd
import pytest
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from models.cases import Cases
from io import StringIO


@pytest.fixture
def mock_data():
    # Mock CSV data as strings
    cases_csv = StringIO(
        "id,judul,status,tanggal_mulai,tanggal_selesai,perkembangan_kasus,catatan\n"
        "1,Case 1,On-going,2024-01-01,,Initial progress,Initial notes\n"
        "2,Case 2,Solved,2023-12-01,2024-01-01,Completed progress,Final notes\n"
    )

    suspect_cases_csv = StringIO(
        "id_suspect,id_kasus\n"
        "101,1\n"
        "102,2\n"
    )

    victim_cases_csv = StringIO(
        "id_victim,id_kasus\n"
        "201,1\n"
        "202,2\n"
    )

    detective_cases_csv = StringIO(
        "id_detective,id_kasus\n"
        "301,1\n"
        "302,2\n"
    )

    victims_csv = StringIO(
        "id,nama,foto,nik,usia,jk,hasil_forensik\n"
        "201,John Doe,,1234567890,30,Male,Positive\n"
        "202,Jane Smith,,0987654321,28,Female,Negative\n"
    )

    suspects_csv = StringIO(
        "id,nama,foto,nik,usia,jk,catatan_kriminal\n"
        "101,Jack,,123123123,35,Male,Fraud\n"
        "102,Emily,,321321321,29,Female,Theft\n"
    )

    detectives_csv = StringIO(
        "id,nama,nik\n"
        "301,Detective A,987654321\n"
        "302,Detective B,123456789\n"
    )

    return {
        "cases": pd.read_csv(cases_csv, index_col="id"),
        "suspect_cases": pd.read_csv(suspect_cases_csv),
        "victim_cases": pd.read_csv(victim_cases_csv),
        "detective_cases": pd.read_csv(detective_cases_csv),
        "victims": pd.read_csv(victims_csv, index_col="id"),
        "suspects": pd.read_csv(suspects_csv, index_col="id"),
        "detectives": pd.read_csv(detectives_csv, index_col="id"),
    }

@pytest.fixture
def cases_model(mock_data):
    # Create a mock implementation of the Cases class
    class CasesWithMockedData(Cases):
        def __init__(self, data):
            self.cases_df = data["cases"]
            self.victim_id = data["victim_cases"]
            self.suspect_id = data["suspect_cases"]
            self.detective_id = data["detective_cases"]
            self.victims_df = data["victims"]
            self.suspects_df = data["suspects"]
            self.detectives_df = data["detectives"]

        def write_cases(self):
            pass  # No-op for testing to avoid writing files

        def write_updated_case(self):
            pass  # No-op for testing to avoid writing files

    return CasesWithMockedData(mock_data)

def test_get_suspects_by_id_kasus(cases_model):
    suspects = cases_model.get_suspects_by_id_kasus(1)
    assert not suspects.empty
    assert suspects.iloc[0]["nama"] == "Jack"

def test_get_victims_by_id_kasus(cases_model):
    victims = cases_model.get_victims_by_id_kasus(1)
    assert not victims.empty
    assert victims.iloc[0]["nama"] == "John Doe"

def test_get_detectives_by_id_kasus(cases_model):
    detectives = cases_model.get_detectives_by_id_kasus(1)
    assert not detectives.empty
    assert detectives.iloc[0]["nama"] == "Detective A"

def test_get_cases_info(cases_model):
    case, suspects, victims, detectives = cases_model.get_cases_info(1)
    assert case["judul"] == "Case 1"
    assert not suspects.empty
    assert not victims.empty
    assert not detectives.empty

def test_update_case(cases_model):
    updated_case = {
        "judul": "Updated Case",
        "status": "On-going",
        "tanggal_mulai": "2024-01-01",
        "tanggal_selesai": None,
        "perkembangan_kasus": "Updated progress",
        "catatan": "Updated notes"
    }
    cases_model.update_case(1, updated_case, [102], [202], [302])
    updated = cases_model.get_cases_info(1)[0]
    assert updated["judul"] == "Updated Case"
    assert updated["catatan"] == "Updated notes"
