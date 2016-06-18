import pandas as pd


def fact_mjd_to_datetime(fact_mjd):
    ''' convert fact mjds (days since unix epoch) to pandas datetimes '''

    return pd.to_datetime(fact_mjd * 24 * 3600 * 1e9)
