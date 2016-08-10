'''
Usage:
    aux2mongodb [options]

Options:
    --services=<s>     Comma Separated list of services to store in the mongodb
                       If not given, all supported services are stored
    --from=<date>      First date to fill into the database, yesterday if not given
    --until=<date>     Last date to fill into the database, yesterday if not given
    --config=<file>    Config file with database credentials [default: aux2mongodb.yaml]
    --auxdir=<auxdir>  Aux data path (must contain the yyyy/mm/dd/ structure)
                       [default: /fact/aux]
    --overwrite        If given, already existing entries are overwritten, else ignored
'''

from .auxservices import (
    MagicWeather, DriveTracking, DrivePointing,
    DriveSource, PfMini, FSCHumidity, FSCTemperature,
    FTMTriggerRates, BiasVoltage
)
import pymongo
import pandas as pd
import yaml
from docopt import docopt
import logging
from urllib.parse import quote_plus
from datetime import datetime, timedelta

from .utils import camel2snake, normalize_service_name
from .database import bulk_insert


supported_services = {
    normalize_service_name(cls.__name__): cls
    for cls in (
        DriveTracking, DrivePointing, DriveSource, MagicWeather,
        PfMini, FSCHumidity, FSCTemperature, FTMTriggerRates,
        BiasVoltage,
    )
}

log = logging.getLogger('aux2mongodb')


def main():
    logging.basicConfig(level=logging.INFO)
    args = docopt(__doc__)
    print(args)

    with open(args['--config']) as f:
        config = yaml.safe_load(f)

    for key in ('user', 'password'):
        config['mongodb'][key] = quote_plus(config['mongodb'][key])
    client = pymongo.MongoClient(
        'mongodb://{user}:{password}@{host}:{port}'.format(**config['mongodb'])
    )
    db = client.auxdata

    dates = pd.date_range(
        args['--from'] or (datetime.now() - timedelta(days=1)),
        args['--until'] or (datetime.now() - timedelta(days=1)),
        freq='1d',
    )
    services = args['--services'].split(',') if args['--services'] else supported_services

    for service_name in services:

        service_name = normalize_service_name(service_name)
        assert service_name in supported_services, service_name + ' is not supported'
        service = supported_services[service_name](auxdir=args['--auxdir'])

        collection = db[camel2snake(service.__class__.__name__)]
        collection.create_index('timestamp', unique=True)

        for date in dates:
            try:
                df = service.read_date(date)
            except FileNotFoundError:
                logging.info('No data available for {}, {}'.format(collection.name, date))
                continue
            except Exception:
                logging.exception(
                    'Could not read auxdata for {}, {}'.format(collection.name, date)
                )

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


if __name__ == '__main__':
    main()
