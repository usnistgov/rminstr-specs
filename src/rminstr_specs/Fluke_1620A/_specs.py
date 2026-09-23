"""Module for getting manufacturer uncertainties on Fluke 1620A readings."""

import warnings

import numpy as np

from rminstr_specs import CalibrationWarning, Specification

__all__ = ['DatasheetHumidity', 'DatasheetTemperature']


class DatasheetHumidity(Specification):
    """
    Data sheet temperature accuracy spec class for Fluke 1620A.

    Attributes
    ----------
    calibrated : bool
        If the instrument is calibrated or not.

    days_since_cal : flaot
        The names since the last calibration.

    units : str
        The units to use for humidity. Shouldnt change.

    """

    def __init__(
        self,
        name: str,
        serial: str,
        calibrated: bool = None,
        days_since_cal: float = None,
        time_zero: float = None,
    ):
        """
        Create a datasheet model of a Fluke 1620A temperature reading.

        Parameters
        ----------
        name : str
            Name to give datasheet model. For ID purposes.

        serial : str
            Serial of instrument, used to look up calibration dates.

        calibrated : bool, optional
            If not provided, will attempt to be inferred from either
            days_since_cal or looking up the calibration logbook with the
            serial. The default is None.

        days_since_cal : float, optional
            Days since the last calibration, if provided used to determine if
            instrument is in spec. The default is None.

        time_zero : float, optional
            Time of readings taken (initial time).
            If neither days_since_cal or calibrated are provided, this must
            be provided to infer the calibration date. The default is None.

        Returns
        -------
        None.

        """
        self.name = name
        self.serial = serial
        self.calibrated = calibrated
        self.units = 'RH %'

        Specification.__init__(self, name, serial, 1, [self.humidity_accuracy])

        # calibration interval specified in data sheet
        calibration_interval = 365

        # try to check the calibration log if not stated
        # explicitly
        if self.calibrated is None:
            # if days since calibration is provided,
            # just check if its < interval
            if days_since_cal is not None:
                self.calibrated = days_since_cal <= calibration_interval
            # if not provided, try to read the log book
            else:
                warnings.warn(
                    'Assuming uncalibrated.', CalibrationWarning, stacklevel=2
                )
                calibrated = False

        # calibration lookup table
        self._cal_table = {
            0: {'RH %': {'range': (0, 20), 'guaranteed': (3)}},
            1: {'RH %': {'range': (20, 70), 'guaranteed': (1.5)}},
            2: {'RH %': {'range': (70, 100), 'guaranteed': (3)}},
        }

    def all_manufacturer_errors(
        self, readings: np.ndarray, addition_method: str = 'spec'
    ):
        """
        Calculate all manufacturer errors and add them together.

        Returns the uncertainty on the readings as 1 standard uncertianty,
        suitable for use in a standard uncertainty analysis.

        Add together all the manufacture errors using rules given by the
        datasheet.

        Parameters
        ----------
        readings : _np.ndarray
            Readings to get errors for.

        addition_method : str, optional
            Does nothing, provided for compataibility.

        Returns
        -------
        np.ndarray
            Total manufacturer uncertainty.

        """
        return self.humidity_accuracy(readings)

    def humidity_accuracy(self, humidity):
        """
        Get uncertainty associated with humidity readings.

        Parameters
        ----------
        humidity
            Humidity readings.

        Returns
        -------
        np.ndarray
            Humidity accuracy.

        """
        tmp = humidity
        out = np.zeros(tmp.shape)
        indexes = []
        for v in self._cal_table.values():
            ind = np.logical_and(
                v[self.units]['range'][0] <= tmp,
                v[self.units]['range'][1] >= tmp,
            )
            indexes.append(ind)

        for k, v in self._cal_table.items():
            ind = indexes[k]
            sd = v[self.units]['guaranteed'] / np.sqrt(3)
            out[ind] = sd
        return out


class DatasheetTemperature(Specification):
    """
    Data sheet temperature accuracy spec class for Fluke 1620A.

    Attributes
    ----------
    calibrated : bool
        If the instrument is calibrated or not.

    days_since_cal : flaot
        The names since the last calibration.

    units : str
        The units to use for temperature.

    """

    def __init__(
        self,
        name: str,
        serial: str,
        units: str = 'C',
        calibrated: bool = None,
        days_since_cal: float = None,
        time_zero: float = None,
    ):
        """
        Create a datasheet model of a Fluke 1620A temperature reading.

        Parameters
        ----------
        name : str
            Name to give datasheet model. For ID purposes.

        serial : str
            Serial of instrument, used to look up calibration dates.

        units : str, optional
           'C' or 'F'. Units of temperature readings. The default is 'C'.

        calibrated : bool, optional
            If not provided, will attempt to be inferred from either
            days_since_cal or looking up the calibration logbook with the
            serial. The default is None.

        days_since_cal : float, optional
            Days since the last calibration, if provided used to determine if
            instrument is in spec. The default is None.

        time_zero : float, optional
            Time of readings taken (initial time).
            If neither days_since_cal or calibrated are provided, this must
            be provided to infer the calibration date. The default is None.

        Returns
        -------
        None.

        """
        self.name = name
        self.serial = serial
        self.calibrated = calibrated
        self.units = units

        Specification.__init__(self, name, serial, 1, [self.temperature_accuracy])

        # calibration interval specified in data sheet
        calibration_interval = 365

        # try to check the calibration log if not stated
        # explicitly
        if self.calibrated is None:
            # if days since calibration is provided,
            # just check if its < interval
            if days_since_cal is not None:
                self.calibrated = days_since_cal <= calibration_interval
            # if not provided, try to read the log book
            else:
                warnings.warn(
                    'Assuming uncalibrated.', CalibrationWarning, stacklevel=2
                )
                calibrated = False

        # calibration lookup table
        self._cal_table = {
            0: {
                'C': {'range': (0, 16), 'guaranteed': (0.5)},
                'F': (32, 60.8),
                'guaranteed': (0.9),
            },
            1: {
                'C': {'range': (16, 24), 'guaranteed': (0.125)},
                'F': (60.8, 75.2),
                'guaranteed': (0.225),
            },
            2: {
                'C': {'range': (24, 50), 'guaranteed': (0.5)},
                'F': (75.2, 122),
                'guaranteed': (0.9),
            },
        }

    def all_manufacturer_errors(
        self, readings: np.ndarray, addition_method: str = 'spec'
    ):
        """
        Calculate all manufacturer errors and add them together.

        Returns the uncertainty on the readings as 1 standard uncertianty,
        suitable for use in a standard uncertainty analysis.

        Add together all the manufacture errors using rules given by the
        datasheet.

        Parameters
        ----------
        readings : _np.ndarray
            Readings to get errors for.

        addition_method : str, optional
            Does nothing, provided for compataibility.

        Returns
        -------
        err : np.ndarray
            Total manufacturer uncertainty.
        """
        return self.temperature_accuracy(readings)

    def temperature_accuracy(self, temperature):
        """
        Get uncertainty associated with the temperature reading.

        Parameters
        ----------
        temperature
            The readings.

        Returns
        -------
        np.ndarray
            Temperature accuracy.

        """
        tmp = temperature
        out = np.zeros(tmp.shape)
        indexes = []
        for v in self._cal_table.values():
            ind = np.logical_and(
                v[self.units]['range'][0] <= tmp,
                v[self.units]['range'][1] >= tmp,
            )
            indexes.append(ind)

        for k, v in self._cal_table.items():
            ind = indexes[k]
            sd = v[self.units]['guaranteed'] / np.sqrt(3)
            out[ind] = sd
        return out


if __name__ == '__main__':
    temp = np.linspace(0, 50, 100)
    spec = DatasheetTemperature('test', 'xxx')
    # err = spec.all_manufacturer_errors(temp)

    hum = np.linspace(0, 100, 100)
    spec2 = DatasheetHumidity('test', 'xxx')
    # hum_err = spec2.all_manufacturer_errors(hum)
