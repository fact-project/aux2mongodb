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

import pandas as pd
import yaml
from docopt import docopt
import logging
from datetime import datetime, timedelta

from .utils import normalize_service_name
from . import fill_service, supported_services, connect_to_database

log = logging.getLogger('aux2mongodb')


def main():
    logging.basicConfig(level=logging.INFO)
    args = docopt(__doc__)
    print(args)

    with open(args['--config']) as f:
        config = yaml.safe_load(f)

    database = connect_to_database(**config['mongodb'])

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

        for date in dates:
            try:
                fill_service(service=service, date=date, database=database)
            except FileNotFoundError:
                logging.info(
                    'No data available for {}, {}'.format(service_name, date)
                )
            except Exception:
                logging.exception(
                    'Could not read auxdata for {}, {}'.format(service_name, date)
                )


if __name__ == '__main__':
    main()
