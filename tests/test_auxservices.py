def test_reading_magic_weather():
    from aux2mongodb import MagicWeather
    from datetime import date

    d = date(2016, 1, 1)

    m = MagicWeather(auxdir='test_data')
    df = m.read_date(d)

    assert len(df.index) == 20
    assert 'timestamp' in df.columns
