from pyassorted.datetime.datetime import aware_datetime_now, iso_datetime_now


def test_aware_datetime_now():
    df_now = aware_datetime_now("UTC")
    assert df_now is not None
    assert df_now.tzinfo is not None


def test_iso_datetime_now():
    iso_df_now = iso_datetime_now("UTC")
    assert iso_df_now is not None
