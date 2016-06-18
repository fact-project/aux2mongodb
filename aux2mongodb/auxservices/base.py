from astropy.table import Table
from astropy.units import UnitsWarning
import os
import warnings


class AuxService:

    renames = {}
    ignored_columns = []
    transforms = {}
    basename = 'AUX_SERVICE'

    def __init__(self, auxdir='/fact/aux'):
        self.auxdir = auxdir
        self.filename_template = os.path.join(
            self.auxdir, '{date:%Y}',  '{date:%m}', '{date:%d}',
            '{date:%Y%m%d}.' + self.basename + '.fits'
        )

    def read_file(self, filename):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=UnitsWarning)
            df = Table.read(filename).to_pandas()

        df.drop(self.ignored_columns, axis=1, inplace=True)
        df.rename(columns=self.renames, inplace=True)

        for key, transform in self.transforms.items():
            df[key] = transform(df[key])

        return df

    def read_date(self, date):

        filename = self.filename_template.format(date=date)
        return self.read_file(filename)
