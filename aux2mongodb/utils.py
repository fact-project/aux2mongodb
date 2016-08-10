import pandas as pd
import re


def fact_mjd_to_datetime(fact_mjd):
    ''' convert fact mjds (days since unix epoch) to pandas datetimes '''

    return pd.to_datetime(fact_mjd * 24 * 3600 * 1e9)


def camel2snake(string):
    ''' taken from http://stackoverflow.com/a/1176023/3838691 '''
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def normalize_service_name(string):
    return string.replace('_', '').lower()
