"""
HP3458A accuracy specifications retrievable in a python format.

Source and more information and instructions for calculating accuracies are found in
Appendix A of manuals/HP3458A.pdf of this repo.
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

# %% Defining Accuracy  Specs
# %%% DC Volts Specs
_range_units = 'V'
_time_since_cal_units = 'days'
_accuracy_units = '(scale: ppm of reading, offset: ppm of range)'
_temp_coef_units = '(scale: ppm of reading/C, offset: ppm of range/C)'
_meas_ranges = [100e-3, 1, 10, 100, 1000]
_times_since_cal = [1, 90, 365, 730]
# accuracy touples are accuracy[meas_range][time_since_cal_range] = (scale,offset)
_accuracy = {
    0.1: {1: (2.5, 5), 90: (5, 10), 365: (9, 10), 730: (14, 20)},
    1: {1: (1.5, 0.5), 90: (4.6, 1), 365: (8, 1), 730: (14, 2)},
    10: {1: (0.5, 0.05), 90: (4.1, 0.2), 365: (8, 0.2), 730: (14, 0.5)},
    100: {1: (2.5, 0.3), 90: (6, 0.3), 365: (10, 0.3), 730: (14, 0.5)},
    1000: {1: (2.5, 0.1), 90: (6, 0.1), 365: (10, 0.1), 730: (14, 0.5)},
}
# temp coefs indexed by [meas_range: float][acal: bool]
_temp_coef = {
    0.1: {False: (1.2, 1), True: (0.15, 1)},
    1: {False: (1.2, 0.1), True: (0.15, 0.1)},
    10: {False: (0.5, 0.01), True: (0.15, 0.01)},
    100: {False: (2, 0.4), True: (0.15, 0.1)},
    1000: {False: (2, 0.04), True: (0.15, 0.01)},
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

# %%% DC Current Specs
_range_units = 'A'
_days_since_cal_units = 'days'
_accuracy_units = '(scale: ppm of reading, offset: ppm of range)'
_temp_coef_units = '(scale: ppm of reading/C, offset: ppm of range/C)'
_meas_ranges = [100e-9, 1e-6, 10e-6, 100e-6, 1e-3, 10e-3, 100e-3, 1]
_days_since_cal = [1, 90, 365, 730]
# accuracy tuples are accuracy[meas_range][time_since_cal_range] = (scale,offset)
_accuracy = {
    100e-9: {1: (10, 400), 90: (30, 400), 365: (30, 400), 730: (35, 400)},
    1e-6: {1: (10, 40), 90: (15, 40), 365: (20, 40), 730: (25, 40)},
    10e-6: {1: (10, 5), 90: (15, 10), 365: (20, 10), 730: (25, 10)},
    100e-6: {1: (10, 5), 90: (15, 8), 365: (20, 8), 730: (25, 8)},
    1e-3: {1: (10, 3), 90: (15, 5), 365: (20, 5), 730: (25, 5)},
    10e-3: {1: (10, 3), 90: (15, 5), 365: (20, 5), 730: (25, 5)},
    100e-3: {1: (25, 3), 90: (30, 5), 365: (35, 5), 730: (40, 5)},
    1: {1: (100, 10), 90: (100, 10), 365: (110, 10), 730: (115, 10)},
}
# temp coefs indexed by [meas_range: float][acal: bool]
_temp_coef = {
    100e-9: {False: (10, 200), True: (2, 50)},
    1e-6: {False: (2, 20), True: (2, 5)},
    10e-6: {False: (10, 4), True: (2, 1)},
    100e-6: {False: (10, 3), True: (2, 1)},
    1e-3: {False: (10, 2), True: (2, 1)},
    10e-3: {False: (10, 2), True: (2, 1)},
    100e-3: {False: (25, 2), True: (2, 1)},
    1: {False: (25, 3), True: (2, 2)},
}


DCI = meas_accuracy(
    _range_units,
    _days_since_cal_units,
    _temp_coef_units,
    _accuracy_units,
    _meas_ranges,
    _days_since_cal,
    _accuracy,
    _temp_coef,
)

# %%% Ohm Current Specs
_range_units = 'Ohms'
_days_since_cal_units = 'days'
_accuracy_units = '(scale: ppm of reading, offset: ppm of range)'
_temp_coef_units = '(scale: ppm of reading/C, offset: ppm of range/C)'
_meas_ranges = [10, 100, 1e3, 10e3, 100e3, 1e6, 10e6, 100e6, 1e9]
_days_since_cal = [1, 90, 365, 730]
# accuracy tuples are accuracy[meas_range][time_since_cal_range] = (scale,offset)
_accuracy = {
    10: {1: (5, 3), 90: (15, 5), 365: (15, 5), 730: (20, 10)},
    100: {1: (3, 3), 90: (10, 5), 365: (12, 5), 730: (20, 10)},
    1e3: {1: (2, 0.2), 90: (8, 0.5), 365: (10, 0.5), 730: (15, 1)},
    10e3: {1: (2, 0.2), 90: (8, 0.5), 365: (10, 0.5), 730: (15, 1)},
    100e3: {1: (2, 0.2), 90: (8, 0.5), 365: (10, 0.5), 730: (15, 1)},
    1e6: {1: (10, 1), 90: (12, 2), 365: (15, 2), 730: (20, 4)},
    10e6: {1: (50, 5), 90: (50, 10), 365: (50, 10), 730: (75, 10)},
    100e6: {1: (500, 10), 90: (500, 10), 365: (500, 10), 730: (1000)},
    1e9: {1: (5000, 10), 90: (5000, 10), 365: (5000, 10), 730: (10000, 10)},
}
# temp coefs indexed by [meas_range: float][acal: bool]
_temp_coef = {
    10: {False: (3.1), True: (1, 1)},
    100: {False: (3, 1), True: (1, 1)},
    1e3: {False: (3, 0.1), True: (1, 0.1)},
    10e3: {False: (3, 0.1), True: (1, 0.1)},
    100e3: {False: (3, 0.1), True: (1, 0.1)},
    1e6: {False: (3, 1), True: (1, 1)},
    10e6: {False: (20, 20), True: (5, 2)},
    100e6: {False: (100, 20), True: (25, 2)},
    1e9: {False: (1000, 20), True: (250, 2)},
}

DCOhm = meas_accuracy(
    _range_units,
    _days_since_cal_units,
    _temp_coef_units,
    _accuracy_units,
    _meas_ranges,
    _days_since_cal,
    _accuracy,
    _temp_coef,
)


def _get_accuracy(
    spec: meas_accuracy,
    reading_range: float,
    days_since_cal: float,
) -> accuracy_point:
    """
    Get accuracy specs from the HP3458 datasheet.

    Valid for:
        1.temperature ranges of +-1 C of last calibration temperature.
        2.NPLC = 100
        3.Fixed measurement range

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


def _get_temp_coef(
    spec: meas_accuracy, reading_range: float, acal: bool
) -> temp_coef_point:
    """
    Get the temperature coefficient of reading accuracy.

    Temperature coefficients apply to readings with temperatures of >+-1 C
    of calibration temperature without ACAL, and >+-5 C of calibration
    temperature with ACAL. When applying temperature coefficient, use the
    distance from operating range. e.g a measurement made at 38C with a
    calibration temperature of 23 C using ACAL would multiply by 10 C.

    Parameters
    ----------
    spec : meas_accuracy
        Measurement types specification. (eg. specs.DCI).

    reading_range : float
        Measurement range. Valued is automatically rounded up to nearest
        value in spec.reading_ranges.

    acal : bool
        TRUE when measurement made with ACAL, FALSE if not.

    Returns
    -------
    temp_coef_point
        Data class containing the offset, slope, units, and operating ranges of the
        returned specification.

    """
    reading_range = _ciel_to_list(reading_range, spec.reading_ranges)
    vals = spec.temp_coef[reading_range][acal]
    return temp_coef_point(
        vals[0],
        vals[1],
        spec.temp_coef_units,
        reading_range,
        spec.reading_range_units,
        acal,
    )


# reading range interpolation tables for power line cycles
_x_nplc = _np.log10(_np.array([0.01, 1, 100, 1000]))
_y_nplc = _np.log10(_np.array([2.5, 0.075, 0.01, 0.01]))
finterp = _interp1d(_x_nplc, _y_nplc)
_dcv_nplc_ppm_range = lambda x: 10 ** finterp(_np.log10(x))

# reading gain interpolation tables for power line cycles
_x_nplc = _np.log10(_np.array([0.01, 0.1, 1, 100, 1000]))
_y_nplc = _np.log10(_np.array([15, 2.5, 0.5, 0.05, 0.01]))
finterp = _interp1d(_x_nplc, _y_nplc)
_dcv_nplc_ppm_reading = lambda x: 10 ** finterp(_np.log10(x))

# reading range interpolation tables for power line cycles
_x_nplc = _np.log10(_np.array([0.01, 1, 1000]))
_y_nplc = _np.log10(_np.array([50, 2.5, 0.25]))
finterp = _interp1d(_x_nplc, _y_nplc)
_dci_nplc_ppm_range = lambda x: 10 ** finterp(_np.log10(x))

# reading gain interpolation tables for power line cycles
_x_nplc = _np.log10(_np.array([0.01, 0.1, 1, 100, 1000]))
_y_nplc = _np.log10(_np.array([15, 2, 0.5, 0.05, 0.01]))
finterp = _interp1d(_x_nplc, _y_nplc)
_dci_nplc_ppm_reading = lambda x: 10 ** finterp(_np.log10(x))

# reading range interpolation tables for power line cycles
_x_nplc = _np.log10(_np.array([0.01, 1, 1000]))
_y_nplc = _np.log10(_np.array([50, 2.5, 0.25]))
finterp = _interp1d(_x_nplc, _y_nplc)
_dcohm_nplc_ppm_range = lambda x: 10 ** finterp(_np.log10(x))

# reading gain interpolation tables for power line cycles
_x_nplc = _np.log10(_np.array([0.01, 0.1, 1, 100, 1000]))
_y_nplc = _np.log10(_np.array([15, 2, 0.5, 0.05, 0.01]))
finterp = _interp1d(_x_nplc, _y_nplc)
_dcohm_nplc_ppm_reading = lambda x: 10 ** finterp(_np.log10(x))


# %% Classes to interface with specifications manager


# %%% Manufacturer  Specs
class DatasheetDCV(Specification):
    """
    Class that defines the datasheet uncertainties for the HP3458A.

    This model assumes a uniform distribution between the datasheet ranges,
    the functions output the standard deviation (1/sqrt(3)) of the posted
    errors.

    """

    def __init__(
        self,
        name: str = 'HP3458ADCV',
        serial: str = 'NA',
        v_range: float = None,
        days_since_cal: int = None,
        delta_t_cal: float = None,
        acal: bool = None,
        time_zero: float = None,
        nplc: float = None,
        suppress_warnings: bool = False,
        **kwargs,
    ):
        """
        Initialize instance of DCV datasheet specs of HP3458A.

        Parameters
        ----------
        name : str,
            Used in spec_manager to generate names for uncertainty mechanisms.
            Used for identifying instruments in warnings. The default is 'HP3458ADCV'

        serial : str,
            Serial of instrument. Used to identify calibration history in
            log books. The default is 'NA'

        v_range : float, optional
            Current measurement range. The default is None.

        days_since_cal : int, optional
            Days since the last calibration. The default is None.

        delta_t_cal : float, optional
            Ambient temperature of measurement. The default is None.

        acal : bool, optional
            Whether or not the instrument was auto calibrated before measurements. The default is None.

        time_zero : float, optional
            Used as comparison time when trying to infer days since cal from
            logbook

        nplc : float, optional
            Power lince cycle integrations. Default is None.

        suppress_warnings : bool, optional
            Suppress warning output to the console. The default is False


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
            self.powerline_cycles,
        ]
        n_mechanisms = 1

        # init as an abstract spec
        super().__init__(name, serial, n_mechanisms, mechanism_functions)

        # assign everything in case a uiser decides to manually provide something
        self.v_range = v_range
        self.days_since_cal = days_since_cal
        self.delta_t_cal = delta_t_cal
        self.acal = acal
        self.nplc = nplc
        self.suppress_warnings = suppress_warnings
        # if a variable is not provided try to:
        # TODO:  a) check for instantiated specs with a common serial and variables (self.inst_list))
        # TODO:  b) infer a value using metadata and available records or
        #        c) default to a reasonable value based on worst case or usual expectations
        # get a log book

        if v_range is None:
            # raise warning for defaults:
            if not suppress_warnings:
                _warnings.warn(
                    name + ' ' + DatasheetDCV.__name__ + ' Defaulting to auto range',
                    SpecsSettingWarning,
                    stacklevel=2,
                )
            self.v_range = 'auto'

        if delta_t_cal is None:
            # try to read a record
            # default to 2 and raise warning
            self.delta_t_cal = 3
            if not suppress_warnings:
                _warnings.warn(
                    name
                    + ' '
                    + DatasheetDCV.__name__
                    + ' Defaulting to '
                    + str(self.delta_t_cal)
                    + ' C deviation from Tcal',
                    SpecsSettingWarning,
                    stacklevel=2,
                )

        if days_since_cal is None:
            # default if nothing found in the log book
            if self.days_since_cal is None:
                if not suppress_warnings:
                    _warnings.warn(
                        name
                        + ' '
                        + DatasheetDCV.__name__
                        + ' Defaulting to maximum days since cal range',
                        SpecsSettingWarning,
                        stacklevel=2,
                    )
                self.days_since_cal = 730

        if acal is None:
            if not suppress_warnings:
                _warnings.warn(
                    name + ' ' + DatasheetDCV.__name__ + ' Defaulting to no ACAL',
                    SpecsSettingWarning,
                    stacklevel=2,
                )
            self.acal = False

        if nplc is None:
            if not suppress_warnings:
                _warnings.warn(
                    name + ' ' + DatasheetDCV.__name__ + ' Defaulting to 1 PLC',
                    SpecsSettingWarning,
                    stacklevel=2,
                )
            self.nplc = 1

    def all_manufacturer_errors(
        self, readings: _np.ndarray, addition_method: str = 'spec'
    ):
        """
        Return the sum of all manufacturer errors for readings.

        Ensure that errors are added in the way specified by the data sheet,
        if provided. The default is spec unless overridden by a child class.

        if spec, it will use the spec sheet addition which is linear
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

        if addition_method == 'quad':
            return self._all_manufacturer_errors_quadrature(readings)
        else:
            if (
                addition_method != 'spec' and addition_method != 'linear'
            ) and self.suppress_warnings is False:
                _warnings.warn(
                    'addition_method '
                    + addition_method
                    + ' unknown, defaulting to linear'
                )
            return self._all_manufacturer_errors_linear(readings)

    def accuracy_offset(self, readings: _np.ndarray):
        """Get the offset accuracy errors."""
        if self.v_range is None or self.v_range == 'auto':
            pts = [_get_accuracy(DCV, r, self.days_since_cal) for r in readings]
            return _np.array(
                [p.offset * p.reading_range * 1e-6 for p in pts]
            ) / _np.sqrt(3)

        else:
            p = _get_accuracy(DCV, self.v_range, self.days_since_cal)
            return (
                _np.ones(len(readings))
                * p.offset
                * p.reading_range
                * 1e-6
                / _np.sqrt(3)
            )

    def accuracy_slope(self, readings: _np.ndarray):
        """Get the slope accuracy errors."""
        if self.v_range is None or self.v_range == 'auto':
            pts = [_get_accuracy(DCV, r, self.days_since_cal) for r in readings]
            return _np.array(
                [p.slope * r * 1e-6 for p, r in zip(pts, readings)]
            ) / _np.sqrt(3)

        else:
            p = _get_accuracy(DCV, self.v_range, self.days_since_cal)
            return readings * p.slope * 1e-6 / _np.sqrt(3)

    def temperature_coef_offset(self, readings: _np.ndarray):
        """Get the temperature coefficient errors."""
        if self.v_range is None or self.v_range == 'auto':
            pts = [_get_temp_coef(DCV, r, self.acal) for r in readings]
            return _np.array(
                [p.offset * p.reading_range * 1e-6 * self.delta_t_cal for p in pts]
            ) / _np.sqrt(3)

        else:
            p = _get_temp_coef(DCV, self.v_range, self.acal)
            return (
                _np.ones(len(readings))
                * p.offset
                * p.reading_range
                * self.delta_t_cal
                * 1e-6
                / _np.sqrt(3)
            )

    def temperature_coef_slope(self, readings: _np.ndarray):
        """Get the temperature coefficient slope errors."""
        if self.v_range is None or self.v_range == 'auto':
            pts = [_get_temp_coef(DCV, r, self.acal) for r in readings]
            return _np.array(
                [p.slope * r * 1e-6 * self.delta_t_cal for p, r in zip(pts, readings)]
            ) / _np.sqrt(3)

        else:
            p = _get_temp_coef(DCV, self.v_range, self.acal)
            return readings * p.slope * 1e-6 * self.delta_t_cal / _np.sqrt(3)

    def powerline_cycles(self, readings: _np.ndarray):
        """Get errors associates with powerline cycle readings

        This is specifiec as Root mean square of noise, so presumably k=1 uncertainty.
        """
        if self.v_range is None or self.v_range == 'auto':
            vrange = _np.array(
                [
                    _get_accuracy(DCV, r, self.days_since_cal).reading_range
                    for r in readings
                ]
            )
        else:
            vrange = self.v_range
        ppm_range = _dcv_nplc_ppm_range(self.nplc)
        ppm_rdgs = _dcv_nplc_ppm_reading(self.nplc)
        return readings * ppm_rdgs * 1e-6 + vrange * ppm_range * 1e-6


class DatasheetDCI(Specification):
    """
    Class that defines the current datasheet uncertainties for the HP3458A.

    This model assumes a uniform distribution between the datasheet ranges,
    the functions output the standard deviation (1/sqrt(3)) of the posted
    errors.

    """

    def __init__(
        self,
        name: str = 'HP3458ADCI',
        serial: str = 'NA',
        i_range: float = None,
        days_since_cal: int = None,
        delta_t_cal=None,
        acal: bool = None,
        time_zero: float = None,
        nplc: float = None,
        suppress_warnings: bool = False,
        **kwargs,
    ):
        """
        Initialize instance of DCV datasheet specs of HP3458A.

        Parameters
        ----------
        name : str,
            Used in spec_manager to generate names for uncertainty mechanisms.
            Used for identifying instruments in warnings. The default is 'HP3458ADCI'.

        serial : str,
            Serial of instrument. Used to identify calibration history in
            log books. The default is 'NA'.

        i_range : float, optional
            Current measurement range. The default is None.

        days_since_cal : int, optional
            Days since the last calibration. The default is None.

        delta_t_cal : float, optional
            Ambient temperature of measurement. The default is None.

        acal : bool, optional
            Whether or not the instrument was autocalibrated before measurements. The default is None.

        time_zero: float, optional
            Used as comparison time when trying to infer days since cal from
            logbook.

        nplc: float, optional
            Power lince cycle integrations. Default is None.

        suppress_warnings : bool, optional
            Suppress warning output to the console. The default is False

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
            self.powerline_cycles,
        ]
        n_mechanisms = 5

        # init as an abstract spec
        super().__init__(name, serial, n_mechanisms, mechanism_functions)

        # assign everything in case a uiser decides to manually provide something
        self.i_range = i_range
        self.days_since_cal = days_since_cal
        self.delta_t_cal = delta_t_cal
        self.acal = acal
        self.nplc = nplc
        # if a variable is not provided try to:
        # TODO:  a) check for instantiated specs with a common serial and variables (self.inst_list))
        # TODO:  b) infer a value using metadata and available records or
        #        c) default to a reasonable value based on worst case or usual expectations
        # get a log book

        if i_range is None:
            # raise warning for defaults:
            if not suppress_warnings:
                _warnings.warn(
                    name + ' ' + DatasheetDCI.__name__ + ' Defaulting to auto range',
                    SpecsSettingWarning,
                    stacklevel=2,
                )
            self.i_range = 'auto'

        if delta_t_cal is None:
            # try to read a record
            # default to 3 and raise warning
            self.delta_t_cal = 3
            if not suppress_warnings:
                _warnings.warn(
                    name
                    + ' '
                    + DatasheetDCI.__name__
                    + ' Defaulting to '
                    + str(self.delta_t_cal)
                    + ' C deviation from Tcal',
                    SpecsSettingWarning,
                    stacklevel=2,
                )

        if days_since_cal is None:
            if not suppress_warnings:
                _warnings.warn(
                    name
                    + ' '
                    + DatasheetDCI.__name__
                    + ' Defaulting to maximum days since cal range',
                    SpecsSettingWarning,
                    stacklevel=2,
                )
            self.days_since_cal = 730

        if acal is None:
            if not suppress_warnings:
                _warnings.warn(
                    name + ' ' + DatasheetDCI.__name__ + ' Defaulting to no ACAL',
                    SpecsSettingWarning,
                    stacklevel=2,
                )
            self.acal = False

        if nplc is None:
            if not suppress_warnings:
                _warnings.warn(
                    name + ' ' + DatasheetDCV.__name__ + ' Defaulting to 1 PLC',
                    SpecsSettingWarning,
                    stacklevel=2,
                )
            self.nplc = 1

    def all_manufacturer_errors(
        self, readings: _np.ndarray, addition_method: str = 'spec'
    ):
        """
        Calculate all manufacturer errors and add them together.

        Add together all the manufacture errors using rules given by the
        datasheet.

        Parameters
        ----------
        readings : _np.ndarray
            Readings to get errors for.

        addition_method : str, optional
            Specifies how the errors are added together. Linear will add all the standard deviations linearly,
            whereas quad will do a quadrature sum. Linear will give a worst case. Setting this to 'spec' will
            do whatever the specsheet says if stated, otherwise it will revert to linear. The default is 'spec'.

        Returns
        -------
        err : np.ndarray
            Total manufacturer errors.

        """
        if addition_method == 'quad':
            return self._all_manufacturer_errors_quadrature(readings)
        else:
            if (
                addition_method != 'spec' and addition_method != 'linear'
            ) and self.suppress_warnings is False:
                _warnings.warn(
                    'addition_method '
                    + addition_method
                    + ' unknown, defaulting to linear'
                )
            return self._all_manufacturer_errors_linear(readings)

    def accuracy_offset(self, readings: _np.ndarray):
        """Get the offset accuracy errors."""
        if self.i_range is None or self.i_range == 'auto':
            pts = [_get_accuracy(DCI, r, self.days_since_cal) for r in readings]
            return _np.array(
                [p.offset * p.reading_range * 1e-6 for p in pts]
            ) / _np.sqrt(3)

        else:
            p = _get_accuracy(DCI, self.i_range, self.days_since_cal)
            return (
                _np.ones(len(readings))
                * p.offset
                * p.reading_range
                * 1e-6
                / _np.sqrt(3)
            )

    def accuracy_slope(self, readings: _np.ndarray):
        """Get the slope accuracy errors."""
        if self.i_range is None or self.i_range == 'auto':
            pts = [_get_accuracy(DCI, r, self.days_since_cal) for r in readings]
            return _np.array(
                [p.slope * r * 1e-6 for p, r in zip(pts, readings)]
            ) / _np.sqrt(3)

        else:
            p = _get_accuracy(DCI, self.i_range, self.days_since_cal)
            return readings * p.slope * 1e-6 / _np.sqrt(3)

    def temperature_coef_offset(self, readings: _np.ndarray):
        """Get the temperature coefficient errors."""
        if self.i_range is None or self.i_range == 'auto':
            pts = [_get_temp_coef(DCI, r, self.acal) for r in readings]
            return _np.array(
                [p.offset * p.reading_range * 1e-6 * self.delta_t_cal for p in pts]
            ) / _np.sqrt(3)

        else:
            p = _get_temp_coef(DCI, self.i_range, self.acal)
            return (
                _np.ones(len(readings))
                * p.offset
                * p.reading_range
                * self.delta_t_cal
                * 1e-6
                / _np.sqrt(3)
            )

    def temperature_coef_slope(self, readings: _np.ndarray):
        """Get the temperature coefficient slope errors."""
        if self.i_range is None or self.i_range == 'auto':
            pts = [_get_temp_coef(DCI, r, self.acal) for r in readings]
            return _np.array(
                [p.slope * r * 1e-6 * self.delta_t_cal for p, r in zip(pts, readings)]
            ) / _np.sqrt(3)

        else:
            p = _get_temp_coef(DCI, self.i_range, self.acal)
            return readings * p.slope * 1e-6 * self.delta_t_cal / _np.sqrt(3)

    def powerline_cycles(self, readings: _np.ndarray):
        """Get errors associates with powerline cycle readings

        This is specific as Root mean square of noise, so presumably k=1 uncertainty.
        """
        if self.i_range is None or self.i_range == 'auto':
            irange = _np.array(
                [
                    _get_accuracy(DCI, r, self.days_since_cal).reading_range
                    for r in readings
                ]
            )
        else:
            irange = self.i_range
        ppm_range = _dci_nplc_ppm_range(self.nplc)
        ppm_rdgs = _dci_nplc_ppm_reading(self.nplc)
        return readings * ppm_rdgs * 1e-6 + irange * ppm_range * 1e-6


class DatasheetDCOhm(Specification):
    """
    Class that defines the current datasheet uncertainties for the HP3458A.

    This model assumes a uniform distribution between the datasheet ranges,
    the functions output the standard deviation (1/sqrt(3)) of the posted
    errors.

    """

    def __init__(
        self,
        name: str = 'HP3458ADCI',
        serial: str = 'NA',
        ohm_range: float = None,
        days_since_cal: int = None,
        delta_t_cal=None,
        acal: bool = None,
        time_zero: float = None,
        nplc: float = None,
        wires: int = None,
        suppress_warnings: bool = False,
        **kwargs,
    ):
        """
        Initialize instance of DCV datasheet specs of HP3458A.

        Parameters
        ----------
        name : str,
            Used in spec_manager to generate names for uncertainty mechanisms.
            Used for identifying instruments in warnings. The default is 'HP3458ADCI'.

        serial : str,
            Serial of instrument. Used to identify calibration history in
            log books. The default is 'NA'.

        ohm_range : float, optional
            Current measurement range. The default is None.

        days_since_cal : int, optional
            Days since the last calibration. The default is None.

        delta_t_cal : float, optional
            Ambient temperature of measurement. The default is None.

        acal : bool, optional
            Whether or not the instrument was auto calibrated before measurements. The default is None.

        time_zero: float, optional
            Used as comparison time when trying to infer days since cal from
            logbook.

        nplc: float, optional
            Power line cycle integrations. Default is None.

        wires: int, optional
            How many wires measured with. The default is 2.

        suppress_warnings : bool, optional
            Suppress warning output to the console. The default is False

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
            self.powerline_cycles,
            self.accuracy_2wire,
        ]
        n_mechanisms = 6

        # init as an abstract spec
        super().__init__(name, serial, n_mechanisms, mechanism_functions)

        # assign everything in case a uiser decides to manually provide something
        self.i_range = ohm_range
        self.days_since_cal = days_since_cal
        self.delta_t_cal = delta_t_cal
        self.acal = acal
        self.nplc = nplc
        self.wires = wires
        # if a variable is not provided try to:
        # TODO:  a) check for instantiated specs with a common serial and variables (self.inst_list))
        # TODO:  b) infer a value using metadata and available records or
        #        c) default to a reasonable value based on worst case or usual expectations
        # get a log book

        if ohm_range is None:
            # raise warning for defaults:
            if not suppress_warnings:
                _warnings.warn(
                    name + ' ' + DatasheetDCI.__name__ + ' Defaulting to auto range',
                    SpecsSettingWarning,
                    stacklevel=2,
                )
            self.i_range = 'auto'

        if delta_t_cal is None:
            # try to read a record
            # default to 3 and raise warning
            self.delta_t_cal = 3
            if not suppress_warnings:
                _warnings.warn(
                    name
                    + ' '
                    + DatasheetDCI.__name__
                    + ' Defaulting to '
                    + str(self.delta_t_cal)
                    + ' C deviation from Tcal',
                    SpecsSettingWarning,
                    stacklevel=2,
                )

        if days_since_cal is None:
            if not suppress_warnings:
                _warnings.warn(
                    name
                    + ' '
                    + DatasheetDCI.__name__
                    + ' Defaulting to maximum days since cal range',
                    SpecsSettingWarning,
                    stacklevel=2,
                )
            self.days_since_cal = 730

        if acal is None:
            if not suppress_warnings:
                _warnings.warn(
                    name + ' ' + DatasheetDCI.__name__ + ' Defaulting to no ACAL',
                    SpecsSettingWarning,
                    stacklevel=2,
                )
            self.acal = False

        if nplc is None:
            if not suppress_warnings:
                _warnings.warn(
                    name + ' ' + DatasheetDCV.__name__ + ' Defaulting to 1 PLC',
                    SpecsSettingWarning,
                    stacklevel=2,
                )
            self.nplc = 1

        if wires is None:
            if not suppress_warnings:
                _warnings.warn(
                    name + ' ' + DatasheetDCV.__name__ + ' Defaulting to 2 wire',
                    SpecsSettingWarning,
                    stacklevel=2,
                )
            self.wires = 2

    def all_manufacturer_errors(
        self, readings: _np.ndarray, addition_method: str = 'spec'
    ):
        """
        Calculate all manufacturer errors and add them together.

        Add together all the manufacture errors using rules given by the
        datasheet.

        Parameters
        ----------
        readings : _np.ndarray
            Readings to get errors for.

        addition_method : str, optional
            Specifies how the errors are added together. Linear will add all the standard deviations linearly,
            whereas quad will do a quadrature sum. Linear will give a worst case. Setting this to 'spec' will
            do whatever the specsheet says if stated, otherwise it will revert to linear. The default is 'spec'.

        Returns
        -------
        err : np.ndarray
            Total manufacturer errors.

        """
        if addition_method == 'quad':
            return self._all_manufacturer_errors_quadrature(readings)
        else:
            if (
                addition_method != 'spec' and addition_method != 'linear'
            ) and self.suppress_warnings is False:
                _warnings.warn(
                    'addition_method '
                    + addition_method
                    + ' unknown, defaulting to linear'
                )
            return self._all_manufacturer_errors_linear(readings)

    def accuracy_offset(self, readings: _np.ndarray):
        """Get the offset accuracy errors."""
        if self.i_range is None or self.i_range == 'auto':
            pts = [_get_accuracy(DCI, r, self.days_since_cal) for r in readings]
            return _np.array(
                [p.offset * p.reading_range * 1e-6 for p in pts]
            ) / _np.sqrt(3)

        else:
            p = _get_accuracy(DCI, self.i_range, self.days_since_cal)
            return (
                _np.ones(len(readings))
                * p.offset
                * p.reading_range
                * 1e-6
                / _np.sqrt(3)
            )

    def accuracy_2wire(self, readings: _np.array):
        out = _np.zeros(readings.shape)
        if self.wires == 2:
            mapkeys = [24, 50, 90, 365, 730]
            map = {24: 0.05, 90: 0.15, 365: 0.25, 730: 0.5}
            key = _ciel_to_list(self.days_since_cal, mapkeys)
            out += map[key] / _np.sqrt(3)
        return out

    def accuracy_slope(self, readings: _np.ndarray):
        """Get the slope accuracy errors."""
        if self.i_range is None or self.i_range == 'auto':
            pts = [_get_accuracy(DCI, r, self.days_since_cal) for r in readings]
            return _np.array(
                [p.slope * r * 1e-6 for p, r in zip(pts, readings)]
            ) / _np.sqrt(3)

        else:
            p = _get_accuracy(DCI, self.i_range, self.days_since_cal)
            return readings * p.slope * 1e-6 / _np.sqrt(3)

    def temperature_coef_offset(self, readings: _np.ndarray):
        """Get the temperature coefficient errors."""
        if self.i_range is None or self.i_range == 'auto':
            pts = [_get_temp_coef(DCI, r, self.acal) for r in readings]
            return _np.array(
                [p.offset * p.reading_range * 1e-6 * self.delta_t_cal for p in pts]
            ) / _np.sqrt(3)

        else:
            p = _get_temp_coef(DCI, self.i_range, self.acal)
            return (
                _np.ones(len(readings))
                * p.offset
                * p.reading_range
                * self.delta_t_cal
                * 1e-6
                / _np.sqrt(3)
            )

    def temperature_coef_slope(self, readings: _np.ndarray):
        """Get the temperature coefficient slope errors."""
        if self.i_range is None or self.i_range == 'auto':
            pts = [_get_temp_coef(DCI, r, self.acal) for r in readings]
            return _np.array(
                [p.slope * r * 1e-6 * self.delta_t_cal for p, r in zip(pts, readings)]
            ) / _np.sqrt(3)

        else:
            p = _get_temp_coef(DCI, self.i_range, self.acal)
            return readings * p.slope * 1e-6 * self.delta_t_cal / _np.sqrt(3)

    def powerline_cycles(self, readings: _np.ndarray):
        """Get errors associates with powerline cycle readings

        This is specific as Root mean square of noise, so presumably k=1 uncertainty.
        """
        if self.i_range is None or self.i_range == 'auto':
            irange = _np.array(
                [
                    _get_accuracy(DCI, r, self.days_since_cal).reading_range
                    for r in readings
                ]
            )
        else:
            irange = self.i_range
        ppm_range = _dcohm_nplc_ppm_range(self.nplc)
        ppm_rdgs = _dcohm_nplc_ppm_reading(self.nplc)
        return readings * ppm_rdgs * 1e-6 + irange * ppm_range * 1e-6


if __name__ == '__main__':
    DatasheetDCI('xxx', 'xxx')
    DatasheetDCV('xxx', 'xxx')
    ohm = DatasheetDCOhm('xxx', 'xxx')
    print(ohm.all_manufacturer_errors(_np.array([0.1, 10, 100, 1000])))
    ohm = DatasheetDCOhm('xxx', 'xxx', wires=4)
    print(ohm.all_manufacturer_errors(_np.array([0.1, 10, 100, 1000])))
