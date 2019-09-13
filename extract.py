import pandas as pd
import numpy as np
from encodings.aliases import aliases
from itertools import chain

def workaround(filename, header=0, sep=',', encoding='utf-8'):
    """ Extractor function which performs a dumb split and 
        reports problems to the user.
    """
    with open(filename, 'r', encoding=encoding) as fh:
        df = pd.DataFrame(
            line.strip().split(sep) for line in fh.readlines()
        )
    df.columns = [
        c.strip('"') if c else np.nan for c in df.iloc[header]
    ]
    if any(df.columns.isna()):
        """ Drop the row indexes which overflow into the null columns
        """
        ncols = pd.Series(df.columns.isna())
        bad_rows = df[df.iloc[:,ncols[ncols == True].index[0]].notna()]
        print(
            "Discovered problematic rows, dropping",
            *bad_rows.index
        )
        df = df.drop(bad_rows.index)
    return df.loc[header+1:, df.columns.notna()].reset_index(drop=True)

def encoding(filename):
    codecs = (encoding for alias, encoding in aliases.items())
    for codec in chain(('utf-8', 'latin-1'), codecs):
        try:
            with open(filename, 'r', encoding=codec):
                return codec
        except:
            pass
    raise Exception('Unknown exception, all codecs fail')

from contextlib import contextmanager

@contextmanager
def test(function: str):
    yield print(function + ' Test')

if __name__ == '__main__':
    with test('Workaround Extraction'):
        print('Control Test')
        workaround('./control.txt')
        print('Fail Test')
        workaround('./fail.txt')

    with test('Encoding Detection'):
        print(encoding('./control.txt'))
