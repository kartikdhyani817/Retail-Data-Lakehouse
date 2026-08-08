import pandas as pd

from scripts.bronze import add_record_hash


def test_record_hash_created():

    df = pd.DataFrame(
        {
            "city": [
                "Dublin",
                "Cork",
            ],
            "sales": [
                100,
                200,
            ],
        }
    )

    result = add_record_hash(df)

    assert "record_hash" in result.columns


def test_hash_not_empty():

    df = pd.DataFrame(
        {
            "city": ["Dublin"],
            "sales": [100],
        }
    )

    result = add_record_hash(df)

    assert result[
        "record_hash"
    ].notna().all()


def test_hash_length():

    df = pd.DataFrame(
        {
            "city": ["Dublin"],
            "sales": [100],
        }
    )

    result = add_record_hash(df)

    hash_value = result.iloc[0][
        "record_hash"
    ]

    assert len(hash_value) == 64


def test_same_record_same_hash():

    df = pd.DataFrame(
        {
            "city": [
                "Dublin",
                "Dublin",
            ],
            "sales": [
                100,
                100,
            ],
        }
    )

    result = add_record_hash(df)

    assert (
        result.iloc[0]["record_hash"]
        ==
        result.iloc[1]["record_hash"]
    )