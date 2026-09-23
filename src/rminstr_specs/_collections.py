"""Helper functions and structures for the specifications classes"""

import importlib
import pkgutil
from collections import namedtuple
from dataclasses import dataclass as _dataclass

import numpy as np

import rminstr_specs

SpecTuple = namedtuple('SpecTuple', 'model module spec')


@_dataclass
class meas_accuracy:
    """Stores accuracy specifications for a measurement type."""

    # strings containing unit inormation about ranges/specs
    reading_range_units: str
    days_since_cal_units: str
    temp_coef_units: str
    accuracy_units: str

    # list of specified ranges
    reading_ranges: list
    days_since_cal: list

    # dictionairy of accuracy specs
    accuracy: dict
    temp_coef: dict


# data class for returning accuracy queries


@_dataclass
class accuracy_point:
    """Named tuple that stores a single point from accuracy specs."""

    slope: float
    offset: float
    units: str
    reading_range: float
    reading_range_units: str
    days_since_cal_range: float


# data class for returning temperature coeficient queries


@_dataclass
class temp_coef_point:
    """Named tuple that stores a single point from temperature specs."""

    slope: float
    offset: float
    units: str
    reading_range: float
    reading_range_units: str
    acal: bool


def _ciel_to_list(x: float, l: list[float]) -> float:
    """
    Find the closest value l[i] to x where l[i] >= x.

    Parameters
    ----------
    x : float
        Input value to check.

    l : list[float]
        Ceiling values.

    Returns
    -------
    float
        Closest value l[i] to x where l[i] >= x.

    """
    # sort list
    l = np.sort(l)
    idx = np.abs(np.array(l) - x).argmin()
    if x > l[idx]:
        idx += 1
    idx = min(idx, len(l) - 1)
    return l[idx]


def iter_specs():
    for module in pkgutil.iter_modules(rminstr_specs.__path__):
        # if not private
        if module.name[0] != '_':
            instr_model = module.name
            module = importlib.import_module('rminstr_specs.' + module.name)

            for ostr in dir(module):
                if ostr[0] != '_':
                    o = getattr(module, ostr)
                    # print(module, ostr)

                    try:
                        is_spec_class = issubclass(o, rminstr_specs.Specification)
                    except TypeError:
                        continue
                    # print(o, is_spec_class)
                    if is_spec_class:
                        yield SpecTuple(instr_model, module, o)


if __name__ == '__main__':
    for s in iter_specs():
        pass
