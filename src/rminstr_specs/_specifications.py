"""Specs module."""

# system/file path libraries
import importlib
import inspect
import os.path
import time
import warnings

# specification abstractions
from abc import ABC, abstractmethod
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

# type hinting
from typing import Tuple, Union

import numpy as _np

# usual suspects
import pandas as _pd

# %% Inheritable Classes for identifying specifications


class CalibrationWarning(UserWarning):
    pass


class SpecsSettingWarning(UserWarning):
    pass


class Specification(ABC):
    """
    Specification datasheet parent class.

    All specification sheets will inherit from this class.

    Attributes
    ----------
    n_mechanisms : int
        Number of uncertanity mechanisms.

    mechanism_functions : list
        List of callable functions wite the mechanism functions.

    name : str
        Name of the instrument.

    serial : str
        Serial number of the instrument.

    time_zero : int
        Reference time. Set by the spec manager.

    """

    inst_list = []

    def __init__(
        self,
        name: str,
        serial: str,
        n_mechanisms: int,
        mechanism_functions: list[Callable],
    ):
        self.n_mechanisms = n_mechanisms
        self.mechanism_functions = mechanism_functions
        self.name = name
        self.serial = serial

        # these variables are auto-assigned by a spec_manager
        self.time_zero = None
        self.inst_list.append(self)

    def __str__(self):
        """Represent as a string."""
        msg = self.name + ';' + type(self).__name__ + ' spec with mechanisms :'
        for m in self.mechanism_functions:
            msg += '\n    ' + m.__name__
        return msg

    @abstractmethod
    def all_manufacturer_errors(
        self, readings: _np.ndarray, addition_method: str = 'spec'
    ) -> _np.ndarray:
        """
        Return the sum of all manufacturer errors for readings.

        Ensure that errors are added in the way specified by the data sheet,
        if provided. The default is spec unless overridden by a child class.

        if spec, it will use the spec sheet addition method, if provided
        if linear, it will add linearly
        if quadrature, it will add in quadrature

        Parameters
        ----------
        readings : _np.ndarray
            Array of measurements to get uncertainties for.

        addition_method : str, optional
            Specifies how the errors are added together. Linear will all the standard deviations linears,
            whereas quad will do a quadrature sum. Linear will give a worst case. The default is 'linear'.

        Returns
        -------
        np.ndarray
            Array of manufacturer errors of same shape as readings.
        """

    def _all_manufacturer_errors_linear(self, readings: _np.ndarray) -> _np.ndarray:
        """
        Return the sum of all manufacturer errors for readings added linearly

        Parameters
        ----------
        readings : _np.ndarray
            Array of measurements to get uncertainties for.

        Returns
        -------
        np.ndarray
            Array of manufacturer errors of same shape as readings.

        """
        err = _np.zeros(readings.shape)
        for f in self.components:
            err += f(readings)

        return err

    def _all_manufacturer_errors_quadrature(self, readings: _np.ndarray) -> _np.ndarray:
        """
        Return the sum of all manufacturer errors for readings added in quadrature

        Parameters
        ----------
        readings : _np.ndarray
            Array of measurements to get uncertainties for.

        Returns
        -------
        np.ndarray
            Array of manufacturer errors of same shape as readings.

        """
        err = _np.zeros(readings.shape)
        for f in self.components:
            err += f(readings) ** 2

        return _np.sqrt(err)
