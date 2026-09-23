r"""
HP34420A accuracy specifications retrievable in a python format.

Source and more information and instructions for calculating accuracies are found in
manuals\HP 34420A user's guide.pdf of this repo.
"""

import warnings as _warnings

import numpy as _np
from scipy.interpolate import interp1d as _interp1d

from rminstr_specs import CalibrationWarning, Specification, SpecsSettingWarning
from rminstr_specs._collections import (
    _ciel_to_list,
    accuracy_point,
    meas_accuracy,
    temp_coef_point,
)

_warning_stack = 3

# %% Defining Accuracy  Specs
# %%% DC Volts Specs
_range_units = 'V'
_time_since_cal_units = 'days'
_accuracy_units = '(scale: percent of reading, offset: percent of range)'
_temp_coef_units = '(scale: percent of reading, offset: percent of range)'
_meas_ranges = [1e-3, 10e-3, 100e-3, 1, 10, 100]
_times_since_cal = [1, 90, 365]
# accuracy tuples are accuracy[meas_range][time_since_cal_range] = (scale,offset)
_accuracy = {
    1e-3: {1: (0.0025, 0.0020), 90: (0.0040, 0.0020), 365: (0.0050, 0.0020)},
    10e-3: {1: (0.0025, 0.0002), 90: (0.0040, 0.0002), 365: (0.0050, 0.0003)},
    100e-3: {1: (0.0015, 0.0003), 90: (0.0030, 0.0004), 365: (0.0040, 0.0004)},
    1: {1: (0.0010, 0.0003), 90: (0.0025, 0.0004), 365: (0.0035, 0.0004)},
    10: {1: (0.0002, 0.0001), 90: (0.0020, 0.0004), 365: (0.0030, 0.0004)},
    100: {1: (0.0010, 0.0004), 90: (0.0025, 0.0005), 365: (0.0035, 0.0005)},
}
# temp coefs indexed by [meas_range: float][acal: bool]
_temp_coef = {
    1e-3: (0.0004, 0.0001),
    10e-3: (0.0004, 0.00002),
    100e-3: (0.0004, 0.00006),
    1: (0.0004, 0.00004),
    10: (0.0001, 0.00002),
    100: (0.0004, 0.00005),
}
DCV = meas_accuracy(
    _range_units,
    _time_since_cal_units,
    _temp_coef_units,
    _accuracy_units,
    _meas_ranges,
    _times_since_cal,
    _accuracy,
    _temp_coef,
)


def _get_accuracy(
    spec: meas_accuracy,
    reading_range: float,
    days_since_cal: float,
) -> accuracy_point:
    """
    Get accuracy specs from the HP34420A data sheet.

    Parameters
    ----------
    spec : meas_accuracy
        Measurement types specification. (eg. specs.DCI).

    meas_range : float
        Measurement range. Valued is autumatically rounded up to nearest
        value in spec.reading_ranges.
    days_since_cal : float
        Number of days since last calibration. Value is automatically rounded
        up to nearest value in spec.days_since_last_cal

    Returns
    -------
    accuracy_point
        Data class containing the offset, slope, units, and operating ranges of the
        returned specification.

    """
    reading_range = _ciel_to_list(reading_range, spec.reading_ranges)
    days_since_cal = _ciel_to_list(days_since_cal, spec.days_since_cal)
    vals = spec.accuracy[reading_range][days_since_cal]
    # put into name tuple for output
    return accuracy_point(
        vals[0],
        vals[1],
        spec.accuracy_units,
        reading_range,
        spec.reading_range_units,
        days_since_cal,
    )


def _get_temp_coef(spec: meas_accuracy, reading_range: float) -> temp_coef_point:
    """
    Get the temperature coefficient of reading accuracy.

    Parameters
    ----------
    spec : meas_accuracy
        Measurement types specification. (eg. specs.DCI).

    reading_range : float
        Measurement range. Valued is automatically rounded up to nearest
        value in spec.reading_ranges.

    Returns
    -------
    temp_coef_point
        Data class containing the offset, slope, units, and operating ranges of the
        returned specification.

    """
    reading_range = _ciel_to_list(reading_range, spec.reading_ranges)
    vals = spec.temp_coef[reading_range]
    return temp_coef_point(
        vals[0],
        vals[1],
        spec.temp_coef_units,
        reading_range,
        spec.reading_range_units,
        None,
    )


# class DatasheetDCV(ispecs.DatasheetMeasureDCV):
class DatasheetDCV(Specification):
    """
    Class that defines the current datasheet uncertainties for the HP 34420A.

    This model assumes a uniform distribution between the datasheet ranges,
    the functions output the standard deviation (1/sqrt(3)) of the posted
    errors.

    """

    def __init__(
        self,
        name: str = 'HP34420A',
        serial: str = 'NA',
        v_range: float = None,
        days_since_cal: float = None,
        t_ambient: float = None,
        null: bool = None,
        time_zero: float = None,
        suppress_warnings: bool = False,
        **kwargs,
    ):
        """
        Initialize instance of DCV datasheet specs of HP34420A.

        Parameters
        ----------
        name : str, optional,
            Used in spec_manager to generate names for uncertainty mechanisms.
            Used for identifying instruments in warnings. The default is 'HP34420A'.

        serial : str, optional
            Serial of instrument. Used to identify calibration history in
            log books. The default is 'NA'.

        v_range : float, optional
            Voltage measurement range. The default is None.

        days_since_cal : float, optional
            Days since the last calibration. The default is None.

        t_ambient : float, optional
            Ambient temperature of measurement. The default is None.

        null : bool, optional
            True if instrument was nulled prior to measurement.
            The default is False.

        time_zero : str,
            Used as comparison time when trying to infer days since cal from
            logbook.

        suppress_warnings : bool, optional
            Suppress warning output to the console. The default is False.

        Returns
        -------
        None.

        """
        mechanism_functions = [self.all_manufacturer_errors]

        # functions that make up the uncertainty mechanisms
        self.components = [
            self.accuracy_offset,
            self.accuracy_slope,
            self.temperature_coef_offset,
            self.temperature_coef_slope,
        ]
        n_mechanisms = 1

        # init as an abstract spec
        super().__init__(name, serial, n_mechanisms, mechanism_functions)

        # assign everything in case a uiser decides to manually provide something
        self.v_range = v_range
        self.days_since_cal = days_since_cal
        self.t_ambient = t_ambient
        self.null = null

        if v_range is None:
            # raise warning for defaults:
            if not suppress_warnings:
                _warnings.warn(
                    name + ' ' + DatasheetDCV.__name__ + ' Defaulting to auto range',
                    SpecsSettingWarning,
                    stacklevel=2,
                )
            self.v_range = 'auto'

        if t_ambient is None:
            # try to read a record
            # default to 2 and raise warning
            self.t_ambient = 26
            if not suppress_warnings:
                _warnings.warn(
                    name
                    + ' '
                    + DatasheetDCV.__name__
                    + ' Defaulting to '
                    + str(self.t_ambient)
                    + ' C Ambient Temperature',
                    SpecsSettingWarning,
                    stacklevel=2,
                )

        if days_since_cal is None:
            # default if nothing found in the log book
            if self.days_since_cal is None:
                self.days_since_cal = 365
                if not suppress_warnings:
                    _warnings.warn(
                        name
                        + ' '
                        + DatasheetDCV.__name__
                        + ' Defaulting to 365 (max) days since cal range',
                        SpecsSettingWarning,
                        stacklevel=2,
                    )

        if null is None:
            if not suppress_warnings:
                _warnings.warn(
                    name + ' ' + DatasheetDCV.__name__ + ' Defaulting to no null',
                    SpecsSettingWarning,
                    stacklevel=2,
                )
            self.null = False

        # check if in spec for temperature
        self.temp_out_of_spec = True
        if self.t_ambient > 18 and self.t_ambient < 28:
            self.temp_out_of_spec = False

    def all_manufacturer_errors(
        self, readings: _np.ndarray, addition_method: str = 'spec'
    ):
        """
        Return the sum of all manufacturer errors for readings.

        Ensure that errors are added in the way specified by the data sheet,
        if provided. The default is spec unless overridden by a child class.

        if spec, it will use linear since the spec sheet does not specify
        if linear, it will add linearly
        if quadrature, it will add in quadrature

        Parameters
        ----------
        readings : _np.ndarray
            Array of measurements to get uncertainties for.

        addition_method : str, optional
            Specifies how the errors are added together. Linear will add all the standard deviations linearly,
            whereas quad will do a quadrature sum. Linear will give a worst case. Setting this to 'spec' will
            do whatever the specsheet says if stated, otherwise it will revert to linear. The default is 'spec'.

        Returns
        -------
        np.ndarray
            Array of manufacturer errors of same shape as readings.

        """
        # if addition_method=='quad':
        #     return self._all_manufacturer_errors_quadrature(readings)
        # else:
        #     return self._all_manufacturer_errors_linear(readings)

        err = _np.zeros(readings.shape)
        for f in self.components:
            err += f(readings)

        # TODO I dont think this is accurate
        if not self.null:
            err += 100e-9 / _np.sqrt(3)

        return err

    def accuracy_offset(self, readings: _np.ndarray):
        """Get the offset accuracy errors."""
        if self.v_range is None or self.v_range == 'auto':
            pts = [_get_accuracy(DCV, r, self.days_since_cal) for r in readings]
            return _np.array([p.offset * p.reading_range * 1e-2 for p in pts]) / 3

        else:
            p = _get_accuracy(DCV, self.v_range, self.days_since_cal)
            return _np.ones(len(readings)) * p.offset * p.reading_range * 1e-2 / 3

    def accuracy_slope(self, readings: _np.ndarray):
        """Get the slope accuracy errors."""
        if self.v_range is None or self.v_range == 'auto':
            pts = [_get_accuracy(DCV, r, self.days_since_cal) for r in readings]
            return _np.array([p.slope * r * 1e-2 for p, r in zip(pts, readings)]) / 3

        else:
            p = _get_accuracy(DCV, self.v_range, self.days_since_cal)
            return readings * p.slope * 1e-2 / 3

    def temperature_coef_offset(self, readings: _np.ndarray):
        """Get the temperature coefficient errors."""
        if self.temp_out_of_spec:
            if self.v_range is None or self.v_range == 'auto':
                pts = [_get_temp_coef(DCV, r) for r in readings]
                return _np.array([p.offset * p.reading_range * 1e-2 for p in pts]) / 3
            else:
                p = _get_temp_coef(DCV, self.v_range)
                return _np.ones(len(readings)) * p.offset * p.reading_range * 1e-2 / 3
        else:
            return _np.zeros(len(readings))

    def temperature_coef_slope(self, readings: _np.ndarray):
        """Get the temperature coefficient slope errors."""
        if self.temp_out_of_spec:
            if self.v_range is None or self.v_range == 'auto':
                pts = [_get_temp_coef(DCV, r) for r in readings]
                return (
                    _np.array([p.slope * r * 1e-2 for p, r in zip(pts, readings)]) / 3
                )

            else:
                p = _get_temp_coef(DCV, self.v_range)
                return readings * p.slope * 1e-2 / 3
        else:
            return _np.zeros(len(readings))


# %% Reading Rates
# These may not be entirely accurate from testing
_nplc = [200, 100, 20, 10, 1, 0.2, 0.02]
_per_sec = [0.15, 0.3, 1.5, 3, 25, 100, 250]
dcv_readings_per_second = _interp1d(_nplc, _per_sec)

if __name__ == '__main__':
    DatasheetDCV('name', 'serial')
