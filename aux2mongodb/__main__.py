'''
Usage:
    aux2mongodb [options]

Options:
    --services=<s>     Comma Separated list of services to store in the mongodb
                       If not given, all supported services are stored
    --begin=<date>     First date to fill into the database [default: 2016-01-01]
    --end=<date>       Last date to fill into the database [default: 2016-01-31]
    --config=<file>    Config file with database credentials [default: aux2mongodb.yaml]
    --auxdir=<auxdir>  Aux data path (must contain the yyyy/mm/dd/ structure)
                       [default: /fact/aux]
    --overwrite        If given, already existing entries are overwritten, else ignored
'''

from .auxservices import MagicWeather, DriveTracking, DrivePointing, DriveSource, PfMini
import pymongo
import pandas as pd
import yaml
from docopt import docopt
import logging
from urllib.parse import quote_plus
import re


def camel2snake(string):
    ''' taken from http://stackoverflow.com/a/1176023/3838691 '''
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def normalize_service_name(string):
    return string.replace('_', '').lower()


supported_services = {
    'magicweather': MagicWeather,
    'drivetracking': DriveTracking,
    'drivepointing': DrivePointing,
    'drivesource': DriveSource,
    'pfmini': PfMini,
}


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

    dates = pd.date_range(args['--begin'], args['--end'], freq='1d')
    services = args['--services'].split(',') if args['--services'] else supported_services

    for service_name in services:

        service_name = normalize_service_name(service_name)
        assert service_name in services, service_name + ' is not supported'
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
                logging.exception()

            data = df.to_dict(orient='records')

            if args['--overwrite']:
                bulk = collection.initialize_unordered_bulk_op()
                for row in data:
                    bulk.find({'timestamp': row['timestamp']}).upsert().replace_one(row)
                result = bulk.execute()
                logging.info('Inserted: {}, Updated: {} for {:%Y-%m-%d}, {}'.format(
                    len(result['upserted']), result['nModified'], date, collection.name
                ))
            else:
                try:
                    result = collection.insert_many(data, ordered=False)
                    logging.info('Inserted: {}, Failed: 0 for {:%Y-%m-%d}, {}'.format(
                        len(result.inserted_ids), date, collection.name
                    ))

                except pymongo.errors.BulkWriteError as e:
                    logging.info('Inserted: {}, Failed: {} for {:%Y-%m-%d}, {}'.format(
                        e.details['nInserted'],
                        len(e.details['writeErrors']),
                        date,
                        collection.name
                    ))


if __name__ == '__main__':
    main()
