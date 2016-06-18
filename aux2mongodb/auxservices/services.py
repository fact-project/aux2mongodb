from .base import AuxService
from ..utils import fact_mjd_to_datetime


class MagicWeather(AuxService):
    basename = 'MAGIC_WEATHER_DATA'
    renames = {
        'Time': 'timestamp',
        'T': 'temperature',
        'T_dew': 'dewpoint',
        'H': 'humidity',
        'P': 'pressure',
        'v': 'wind_speed',
        'v_max': 'wind_gust_speed',
        'd': 'wind_direction',
    }

    ignored_columns = ['stat', 'QoS']
    transforms = {'timestamp': fact_mjd_to_datetime}


class DriveTracking(AuxService):
    basename = 'DRIVE_CONTROL_TRACKING_POSITION'
    renames = {
        'Time': 'timestamp',
        'Ra': 'right_ascension',
        'Dec': 'declination',
        'Ha': 'hourangle',
        'SrcRa': 'right_ascension_source',
        'SrcDec': 'declination_source',
        'HaDec': 'hourangle_source',
        'Zd': 'zenith',
        'Az': 'azimuth',
        'dZd': 'zenith_deviation',
        'dAz': 'azimuth_deviation',
        'dev': 'absolute_control_deviation',
        'avgdev': 'average_control_deviation',
    }
    transforms = {'timestamp': fact_mjd_to_datetime}
    ignored_columns = ['QoS', ]
