"""Blanket tests that everything conformws to the expected API."""

from rminstr_specs._collections import iter_specs
from pathlib import Path
import rminstr_specs
import numpy as np
import pytest

SAMPLE_ARR = np.ones(10)
SAMPLE_NAME = 'my-spec'
SAMPLE_SERIAL = 'my-serial'


def test_simple():
    # calling with just a name and
    # serial every spec sheet should accept this,
    # than throw a warning if no logbook is connected
    for s in iter_specs():
        print('')
        print('Checking : ', s.spec)
        print('====================')
        spec = s.spec(SAMPLE_NAME, SAMPLE_SERIAL)
        arr_data = spec.all_manufacturer_errors(SAMPLE_ARR)


if __name__ == '__main__':
    test_simple()
