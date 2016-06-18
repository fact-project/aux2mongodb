'''
Usage:
    shorten_fits_file <input> <output> [options]

Options:
    -n <N>, --num-rows=<N>    how many rows to store [default: 20]
'''
from astropy.table import Table
from docopt import docopt

if __name__ == '__main__':

    args = docopt(__doc__)
    t = Table.read(args['<input>'])
    t[:int(args['--num-rows'])].write(args['<output>'])
