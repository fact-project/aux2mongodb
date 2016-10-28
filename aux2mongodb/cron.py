import schedule
from time import sleep
from datetime import datetime, timedelta
from argparse import ArgumentParser
import yaml
import logging
import os

from . import supported_services, connect_to_database, fill_service

dotdir = os.path.join(os.environ['HOME'], '.aux2mongo')
os.makedirs(dotdir, exist_ok=True)

parser = ArgumentParser()
parser.add_argument('-c', '--config', dest='config', default='aux2mongo.yaml')
parser.add_argument('-d', '--auxdir', dest='auxdir', default='/fact/aux')
parser.add_argument(
    '-l', '--logfile', dest='logfile',
    default=os.path.join(dotdir, 'aux2mongo.log')
)

log = logging.getLogger(__name__)


def fill_last_night(services, database):
    date = (datetime.utcnow() - timedelta(days=1)).date()

    for service in services:
        name = service.__class__.__name__

        log.info('Start uploading service {} for night {}'.format(name, date))
        try:
            fill_service(service=service, date=date, database=database)
        except FileNotFoundError:
            log.info(
                'No data available for {}, {}'.format(name, date)
            )
        except Exception:
            log.exception(
                'Could not read auxdata for {}, {}'.format(name, date)
            )


def main():
    args = parser.parse_args()

    log = logging.getLogger()
    stream = logging.StreamHandler()
    file_handler = logging.FileHandler(args.logfile)
    log.addHandler(stream)
    log.addHandler(file_handler)

    with open(args.config) as f:
        config = yaml.safe_load(f)

    log.info('Connecting to database')
    database = connect_to_database(**config['mongodb'])
    log.info('Connection established')

    services = [
        service(auxdir=args.auxdir)
        for service in supported_services.values()
    ]

    schedule.every().day.at('15:00').do(
        fill_last_night, services=services, database=database
    )

    try:
        while True:
            schedule.run_pending()
            sleep(60)
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
