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


class DrivePointing(AuxService):
    basename = 'DRIVE_CONTROL_POINTING_POSITION'
    renames = {
        'Time': 'timestamp',
        'Zd': 'zenith',
        'Az': 'azimuth',
    }
    transforms = {'timestamp': fact_mjd_to_datetime}
    ignored_columns = ['QoS', ]


class DriveSource(AuxService):
    basename = 'DRIVE_CONTROL_SOURCE_POSITION'
    renames = {
        'Time': 'timestamp',
        'Ra_src': 'right_ascension_source',
        'Ra_cmd': 'right_ascension_command',
        'Dec_src': 'declination_source',
        'Dec_cmd': 'declination_command',
        'Offset': 'wobble_offset',
        'Angle': 'wobble_angle',
        'Name': 'source_name',
    }
    transforms = {'timestamp': fact_mjd_to_datetime}
    ignored_columns = ['QoS', ]
