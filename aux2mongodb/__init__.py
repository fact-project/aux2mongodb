import logging
import pymongo

from .utils import camel2snake, normalize_service_name
from .database import bulk_insert

from fact.auxservices import (
    MagicWeather, DriveTracking, DrivePointing,
    DriveSource, PfMini, FSCHumidity, FSCTemperature,
    FTMTriggerRates, BiasVoltage, FADTemperature
)


supported_services = {
    normalize_service_name(cls.__name__): cls
    for cls in (
        DriveTracking, DrivePointing, DriveSource, MagicWeather,
        PfMini, FSCHumidity, FSCTemperature, FTMTriggerRates,
        BiasVoltage, FADTemperature,
    )
}


log = logging.getLogger(__name__)


def fill_service(service, date, database):
    collection = database[camel2snake(service.__class__.__name__)]
    collection.create_index('timestamp', unique=True)

    df = service.read_date(date)
    data = df.to_dict(orient='records')

    try:
        result = bulk_insert(data, collection)
        log.info('Inserted: {}, Failed: 0 for {:%Y-%m-%d}, {}'.format(
                len(result.inserted_ids), date, collection.name
        ))
    except pymongo.errors.BulkWriteError as e:
        log.info('Inserted: {}, Failed: {} for {:%Y-%m-%d}, {}'.format(
            e.details['nInserted'],
            len(e.details['writeErrors']),
            date,
            collection.name
        ))
