import tempfile
from pathlib import Path

from data_finder.helpers.baked_data_helper import LocalParquetElectionsHelper
from uk_geo_utils.helpers import Postcode

import pytest
import polars


@pytest.fixture()
def temp_data_root(settings):
    with tempfile.TemporaryDirectory("data") as tmp:
        settings.ELECTIONS_DATA_PATH = tmp
        yield tmp


@pytest.fixture
def sample_data_writer(temp_data_root):
    def write_data(data):
        if data is None:
            df = polars.DataFrame()
        else:
            df = polars.DataFrame(data)
        df_root = Path(temp_data_root)
        df_root.mkdir(exist_ok=True, parents=True)
        df_path = df_root / "AA1.parquet"
        df.write_parquet(df_path)

    yield write_data


def test_file_not_found(temp_data_root):
    helper = LocalParquetElectionsHelper(elections_parquet_path=Path(temp_data_root))
    postcode = Postcode("AA1 1AA")

    expected = {"address_picker": False, "ballot_ids": [], "request_success": False}
    assert helper.get_ballot_list(postcode) == expected


def test_empty_file(temp_data_root, sample_data_writer):
    sample_data_writer(None)

    helper = LocalParquetElectionsHelper(elections_parquet_path=Path(temp_data_root))
    postcode = Postcode("AA1 1AA")

    expected = {"address_picker": False, "ballot_ids": [], "request_success": True}
    assert helper.get_ballot_list(postcode) == expected


def test_postcode_not_found(temp_data_root, sample_data_writer):
    sample_data_writer(
        [
            {
                "postcode": "AA1 1AA",
                "uprn": "000001",
                "current_elections": [],
            },
            {
                "postcode": "AA1 1AA",
                "uprn": "000002",
                "current_elections": [],
            },
        ]
    )

    helper = LocalParquetElectionsHelper(elections_parquet_path=Path(temp_data_root))
    postcode = Postcode("AA1 2AA")

    expected = {"address_picker": False, "ballot_ids": [], "request_success": False}
    assert helper.get_ballot_list(postcode) == expected


def test_postcode_with_no_elections_not_split(temp_data_root, sample_data_writer):
    sample_data_writer(
        [
            {
                "postcode": "AA1 1AA",
                "uprn": "000001",
                "current_elections": [],
            },
            {
                "postcode": "AA1 1AA",
                "uprn": "000002",
                "current_elections": [],
            },
        ]
    )

    helper = LocalParquetElectionsHelper(elections_parquet_path=Path(temp_data_root))
    postcode = Postcode("AA1 1AA")

    expected = {"address_picker": False, "ballot_ids": [], "request_success": True}
    assert helper.get_ballot_list(postcode) == expected


def test_postcode_with_elections_not_split(temp_data_root, sample_data_writer):
    sample_data_writer(
        [
            {
                "postcode": "AA1 1AA",
                "uprn": "000001",
                "current_elections": ["local.buckinghamshire.abbey.2025-05-01"],
            },
            {
                "postcode": "AA1 1AA",
                "uprn": "000002",
                "current_elections": ["local.buckinghamshire.abbey.2025-05-01"],
            },
        ]
    )

    helper = LocalParquetElectionsHelper(elections_parquet_path=Path(temp_data_root))
    postcode = Postcode("AA1 1AA")

    expected = {
        "address_picker": False,
        "ballot_ids": ["local.buckinghamshire.abbey.2025-05-01"],
        "request_success": True,
    }
    assert helper.get_ballot_list(postcode) == expected


def test_postcode_with_all_elections_split(temp_data_root, sample_data_writer):
    sample_data_writer(
        [
            {
                "postcode": "AA1 1AA",
                "uprn": "000001",
                "current_elections": ["local.buckinghamshire.abbey.2025-05-01"],
            },
            {
                "postcode": "AA1 1AA",
                "uprn": "000002",
                "current_elections": ["local.buckinghamshire.beaconsfield.2025-05-01"],
            },
        ]
    )

    helper = LocalParquetElectionsHelper(elections_parquet_path=Path(temp_data_root))
    postcode = Postcode("AA1 1AA")

    expected = {
        "address_picker": True,
        "ballot_ids": [],
        "request_success": True,
    }
    assert helper.get_ballot_list(postcode) == expected


def test_postcode_with_some_elections_split(temp_data_root, sample_data_writer):
    sample_data_writer(
        [
            {
                "postcode": "AA1 1AA",
                "uprn": "000001",
                "current_elections": ["local.buckinghamshire.abbey.2025-05-01"],
            },
            {
                "postcode": "AA1 1AA",
                "uprn": "000002",
                "current_elections": [],
            },
        ]
    )

    helper = LocalParquetElectionsHelper(elections_parquet_path=Path(temp_data_root))
    postcode = Postcode("AA1 1AA")

    expected = {
        "address_picker": True,
        "ballot_ids": [],
        "request_success": True,
    }
    assert helper.get_ballot_list(postcode) == expected


def test_uprn_not_found(temp_data_root, sample_data_writer):
    sample_data_writer(
        [
            {
                "postcode": "AA1 1AA",
                "uprn": "000001",
                "current_elections": ["local.buckinghamshire.abbey.2025-05-01"],
            },
        ]
    )

    helper = LocalParquetElectionsHelper(elections_parquet_path=Path(temp_data_root))
    postcode = Postcode("AA1 1AA")

    expected = {
        "address_picker": False,
        "ballot_ids": [],
        "request_success": False,
    }
    assert helper.get_ballot_list(postcode, uprn="000002") == expected


def test_uprn_duplicate(temp_data_root, sample_data_writer):
    sample_data_writer(
        [
            {
                "postcode": "AA1 1AA",
                "uprn": "000001",
                "current_elections": ["local.buckinghamshire.abbey.2025-05-01"],
            },
            {
                "postcode": "AA1 1AA",
                "uprn": "000001",
                "current_elections": ["local.buckinghamshire.abbey.2025-05-01"],
            },
        ]
    )

    helper = LocalParquetElectionsHelper(elections_parquet_path=Path(temp_data_root))
    postcode = Postcode("AA1 1AA")

    expected = {
        "address_picker": False,
        "ballot_ids": [],
        "request_success": False,
    }
    assert helper.get_ballot_list(postcode, uprn="000001") == expected


def test_uprn_no_elections(temp_data_root, sample_data_writer):
    sample_data_writer(
        [
            {
                "postcode": "AA1 1AA",
                "uprn": "000001",
                "current_elections": [],
            },
            {
                "postcode": "AA1 1AA",
                "uprn": "000002",
                "current_elections": ["local.buckinghamshire.beaconsfield.2025-05-01"],
            },
        ]
    )

    helper = LocalParquetElectionsHelper(elections_parquet_path=Path(temp_data_root))
    postcode = Postcode("AA1 1AA")

    expected = {
        "address_picker": False,
        "ballot_ids": [],
        "request_success": True,
    }
    assert helper.get_ballot_list(postcode, uprn="000001") == expected


def test_uprn_with_elections(temp_data_root, sample_data_writer):
    sample_data_writer(
        [
            {
                "postcode": "AA1 1AA",
                "uprn": "000001",
                "current_elections": ["local.buckinghamshire.abbey.2025-05-01"],
            },
            {
                "postcode": "AA1 1AA",
                "uprn": "000002",
                "current_elections": [],
            },
        ]
    )

    helper = LocalParquetElectionsHelper(elections_parquet_path=Path(temp_data_root))
    postcode = Postcode("AA1 1AA")

    expected = {
        "address_picker": False,
        "ballot_ids": ["local.buckinghamshire.abbey.2025-05-01"],
        "request_success": True,
    }
    assert helper.get_ballot_list(postcode, uprn="000001") == expected
