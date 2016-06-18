def test_fact_mjd_conversion():
    from aux2mongodb.utils import fact_mjd_to_datetime

    timestamp = fact_mjd_to_datetime(16801.33)
    assert timestamp.year == 2016
    assert timestamp.month == 1
    assert timestamp.day == 1
    assert timestamp.hour == 7
    assert timestamp.minute == 55
