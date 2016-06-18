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
