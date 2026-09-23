"""
K2450 accuracy specifications retrievable in a python format.

Source and more information and instructions for calculating accuracies are
found in Appendix A of manuals/K2450-Datasheet.pdf of this repo.

It is recommended to use classes in this module that inherit from
instruments.specifications.spec_type, which will access calibration logs and
attempt to infer calibration history and temperature information.

"""

import warnings as _warnings
from dataclasses import dataclass as _dataclass

import numpy as _np

from rminstr_specs import CalibrationWarning, Specification, SpecsSettingWarning
from rminstr_specs._collections import _ciel_to_list

# %% Classes for storing spec tables and outputting values

__all__ = []


@_dataclass
class _k2401_spec:
    """Stores accuracy specifications for the K2450."""

    # strings containing unit inormation about ranges/specs
    reading_range_units: str
    temp_coef_units: str
    accuracy_units: str
    # list of specified ranges
    reading_ranges: list
    # temperature coefficient multiplier
    temp_coef_multiplier: float
    # dictionairy of sourcing specs
    source: dict
    # dict of measuring specs
    measure: dict
    # source str
    provenance: str


# data class for returning accuracy queries


@_dataclass
class _k2401_spec_point:
    """Named tuple that stores a single point from K2450 specs."""

    slope: float
    offset: float
    units: str
    reading_range: float
    reading_range_units: str


# data class for returning temperature coeficient queries
_prov = 'Source and more information and instructions for calculating accuracies are found in Appendix A of manuals/K2450-Datasheet.pdf of this repo.'

# %% DC Volts Specs
_range_units = 'V'
_accuracy_units = '(scale: %reading, offset: volts)'
_temp_coef_units = '(scale: %reading/C, offset: volts/C)'
_temp_coef_multiplier = 0.15
# accuracy tuples = (scale,offset)
_source = {
    200 * 1e-3: (0.02, 600 * 1e-6),
    2: (0.02, 600 * 1e-6),
    20: (0.02, 2.4 * 1e-3),
    200: (0.02, 24 * 1e-3),
}
_measure = {
    200 * 1e-3: (0.012, 300 * 1e-6),
    2: (0.012, 300 * 1e-6),
    20: (0.015, 1.5 * 1e-3),
    200: (0.015, 10 * 1e-3),
}

_DCV = _k2401_spec(
    _range_units,
    _temp_coef_units,
    _accuracy_units,
    list(_measure.keys()),
    _temp_coef_multiplier,
    _source,
    _measure,
    _prov,
)
# %% DC Current  Specs
_range_units = 'A'
_accuracy_units = '(scale: %reading, offset: Amp)'
_temp_coef_units = '(scale: %reading/C, offset: Amp/C)'
_temp_coef_multiplier = 0.15
# accuracy tuples = (scale,offset)
_source = {
    1 * 1e-6: (0.035, 600 * 1e-12),
    10 * 1e-6: (0.033, 2 * 1e-9),
    100 * 1e-6: (0.031, 20 * 1e-9),
    1 * 1e-3: (0.034, 200 * 1e-9),
    10 * 1e-3: (0.045, 2 * 1e-6),
    100 * 1e-3: (0.066, 20 * 1e-6),
    1: (0.27, 900 * 1e-6),
}
_measure = {
    1 * 1e-6: (0.029, 300 * 1e-12),
    10 * 1e-6: (0.027, 700 * 1e-12),
    100 * 1e-6: (0.025, 6 * 1e-9),
    1 * 1e-3: (0.027, 60 * 1e-9),
    10 * 1e-3: (0.035, 600 * 1e-9),
    100 * 1e-3: (0.055, 6 * 1e-6),
    1: (0.22, 570 * 1e-6),
}

_DCI = _k2401_spec(
    _range_units,
    _temp_coef_units,
    _accuracy_units,
    list(_measure.keys()),
    _temp_coef_multiplier,
    _source,
    _measure,
    _prov,
)

# %% Look up functions


def _accuracy(
    spec: _k2401_spec, reading_range: float, source: bool = True
) -> _k2401_spec_point:
    """
    Get accuracy specs from K2450.

    Valid for:

        1. Temperature ranges of 23+-5 C.

        2. NPLC = 1

        3. Output is on

        4. If sourcing current and range is 100nA or lower, Rear Triax Cables Only

    Parameters
    ----------
    spec : k2450_spec
        Measurement specification sheet.

    reading_range : float
        Measurement range. Value is automatically rounded up to nearest
        value in spec.reading_ranges.

    source : bool
        If True, returns specs for source. If False, returns specs for measure.

    Returns
    -------
    k2450_spec_point
        Data class containing the offset, slope, units, and operating ranges of the
        returned specification.

    """
    # if meas_range not provided, use reading to infer range
    reading_range = _ciel_to_list(reading_range, spec.reading_ranges)
    if source:
        vals = spec.source[reading_range]
    else:
        vals = spec.measure[reading_range]
    # put into name tuple for output
    return _k2401_spec_point(
        vals[0], vals[1], spec.accuracy_units, reading_range, spec.reading_range_units
    )


def _temperature_coefficient(
    spec: _k2401_spec, reading_range: float, source: bool = True
) -> _k2401_spec_point:
    """
    Get the temperature coefficient.

    Temperature coefficients are intended for when K2450 is operated outside
    the 23+-5 C range. Multiply by the distance from the range when using temperature
    coefficients. I.E. a measurement at 30 C would multiply the temperature
    coefficient by 2 C (since the normal operating range goes to 28 C).

    Parameters
    ----------
    spec : k2450_spec
        Measurement specification sheet.

    reading_range : float
        Measurement range. Value is automatically rounded up to nearest value in spec.reading_ranges.

    source: bool
        If True, returns specs for source. If False, returns specs for measure.

    Returns
    -------
    k2450_spec_point
        Data class containing the offset, slope, units, and operating ranges of the
        returned specification.

    """
    # if meas_range not provided, use reading to infer range
    vals = _accuracy(spec, reading_range, source)
    mult = spec.temp_coef_multiplier
    return _k2401_spec_point(
        vals.slope * mult,
        vals.offset * mult,
        spec.temp_coef_units,
        reading_range,
        spec.reading_range_units,
    )


# %% Manufacture Spec Interfaces


class _k2401_datasheet:
    """
    Inheritable class that defines what a K2450 datasheet spec needs.

    This model assumes a uniform distribution for each datasheet range,
    the functions output the standard deviation (1/sqrt(3)) of the posted
    errors. Uniform distribution from reading - posted error to reading + posted error.

    """

    def __init__(
        self,
        name: str = 'K2450',
        serial: str = 'NA',
        reading_range: float = None,
        days_since_cal: float = None,
        t_ambient: float = None,
        spec_type: _k2401_spec = None,
        source: bool = None,
        time_zero: float = None,
        suppress_warnings: bool = False,
        **kwargs,
    ):
        """
        Initialize instance of K2450 datasheet.

        Parameters
        ----------
        name : str, optional
            Used in spec_manager to generate names for uncertainty mechanisms.
            Used for identifying instruments in warnings. The default is 'K2450'

        serial : str, optional
            Serial of instrument. Used to identify calibration history in
            log books. The default is 'NA'

        reading_range : float, optional
            Reading range. The default is None.

        days_since_cal : float, optional
            Days since the last calibration. The default is None.

        t_ambient : float, optional
            Ambient temperature of measurement. The default is None.

        spec_type : _k2401_spec, optional
            Instance of k2450_spec with appropriate values for the datasheet. The default is None.

        source : bool, optional
            Whether or not it is a source or measure. True is source. The default is None.

        time_zero : float, optional
            Timestamp of when the instrument was used. Used to find the days since calibration. The default is None.

        suppress_warnings : bool, optional
            Suppress warning output to the console. The default is False.

        Returns
        -------
        None.

        """
        # assign everything in case a user decides to manually provide something
        self.reading_range = reading_range
        self.days_since_cal = days_since_cal
        self.t_ambient = t_ambient
        self.spec = spec_type
        self.source = source
        self.serial = serial
        self.suppress_warnings = suppress_warnings

        # functions that make up the uncertainty mechanisms
        self.mechanism_functions = [self.all_manufacturer_errors]
        self.components = [
            self.accuracy_offset,
            self.accuracy_slope,
            self.temperature_coef_offset,
            self.temperature_coef_slope,
        ]
        self.n_mechanisms = 1
        stacklevel = 3
        if reading_range is None:
            # raise warning for defaults:
            if not suppress_warnings:
                _warnings.warn(
                    name
                    + ' '
                    + _k2401_datasheet.__name__
                    + ' Defaulting to auto range',
                    SpecsSettingWarning,
                    stacklevel=stacklevel,
                )
            self.reading_range = 'auto'

        if t_ambient is None:
            # try to read a record
            # default to 23+3 and raise warning
            self.t_ambient = 26
            if not suppress_warnings:
                _warnings.warn(
                    name
                    + ' '
                    + _k2401_datasheet.__name__
                    + ' Defaulting to '
                    + str(self.t_ambient)
                    + ' C Ambient Temperature',
                    SpecsSettingWarning,
                    stacklevel=stacklevel,
                )

        if days_since_cal is None and self.days_since_cal is None:
            self.days_since_cal = 365
            if not suppress_warnings:
                _warnings.warn(
                    name
                    + ' '
                    + serial
                    + ''
                    + _k2401_datasheet.__name__
                    + ' Defaulting to 365 (max) days since cal range',
                    SpecsSettingWarning,
                    stacklevel=stacklevel,
                )
        if self.days_since_cal > 365 and not suppress_warnings:
            _warnings.warn(
                name + ' days since calibration out of spec',
                CalibrationWarning,
                stacklevel=stacklevel,
            )

        # check if in spec for temperature
        self.temp_out_of_spec = True
        if self.t_ambient > 18 and self.t_ambient < 28:
            self.temp_out_of_spec = False
            self.delta_t_cal = 0
        # if not in spec get distance from operating range
        elif self.delta_t_cal < 18:
            self.delta_t_cal = abs(18 - self.t_ambient)
        elif self.delta_t_cal > 28:
            self.delta_t_cal = abs(28 - self.t_ambient)

    def all_manufacturer_errors(
        self, readings: _np.ndarray, addition_method: str = 'spec'
    ) -> _np.ndarray:
        """
        Return the sum of all manufacturer errors for readings.

        Ensure that errors are added in the way specified by the data sheet,
        if provided. The default is spec unless overridden by a child class.

        if spec, it will use linear since the spec sheet hints at linear addition
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
            if addition_method != 'spec' and self.suppress_warnings is False:
                _warnings.warn(
                    'addition_method '
                    + addition_method
                    + ' unknown, defaulting to linear'
                )
            return self._all_manufacturer_errors_linear(readings)

    def accuracy_offset(self, readings: _np.ndarray):
        """Get the offset accuracy errors."""
        if self.reading_range is None or self.reading_range == 'auto':
            pts = [_accuracy(self.spec, r, self.source) for r in readings]
            return _np.array([p.offset for p in pts]) / _np.sqrt(3)

        else:
            p = _accuracy(self.spec, self.reading_range, self.source)
            return _np.ones(len(readings)) * p.offset / _np.sqrt(3)

    def accuracy_slope(self, readings: _np.ndarray):
        """Get the slope accuracy errors."""
        if self.reading_range is None or self.reading_range == 'auto':
            pts = [_accuracy(self.spec, r, self.source) for r in readings]
            return _np.array(
                [p.slope * r * 1e-2 for p, r in zip(pts, readings)]
            ) / _np.sqrt(3)

        else:
            p = _accuracy(self.spec, self.reading_range, self.source)
            return readings * p.slope * 1e-2 / _np.sqrt(3)

    def temperature_coef_offset(self, readings: _np.ndarray):
        """Get the temperature coefficient errors."""
        if self.temp_out_of_spec:
            if self.reading_range is None or self.reading_range == 'auto':
                pts = [_temperature_coefficient(self.spec, r) for r in readings]
                return _np.array(
                    [p.offset * p.reading_range * self.delta_t_cal for p in pts]
                ) / _np.sqrt(3)

            else:
                p = _temperature_coefficient(self.spec, self.reading_range)
                return (
                    _np.ones(len(readings))
                    * p.offset
                    * p.reading_range
                    * self.delta_t_cal
                    / _np.sqrt(3)
                )
        else:
            return _np.zeros(len(readings))

    def temperature_coef_slope(self, readings: _np.ndarray):
        """Get the temperature coefficient slope errors."""
        if self.temp_out_of_spec:
            if self.v_range is None or self.v_range == 'auto':
                pts = [_temperature_coefficient(self.spec, r) for r in readings]
                return _np.array(
                    [
                        p.slope * r * self.delta_t_cal * 1e-2
                        for p, r in zip(pts, readings)
                    ]
                ) / _np.sqrt(3)

            else:
                p = _temperature_coefficient(self.spec, self.reading_range)
                return readings * p.slope * self.delta_t_cal * 1e-2 / _np.sqrt(3)
        else:
            return _np.zeros(len(readings))


# class DatasheetMeasureDCV(_k2401_datasheet, _ispecs.DatasheetMeasureDCV):
class DatasheetMeasureDCV(_k2401_datasheet, Specification):
    """DC Voltage Measure class of K2450 datasheet spec."""

    def __init__(
        self,
        name: str,
        serial: str,
        v_range: float = None,
        days_since_cal: float = None,
        t_ambient: float = None,
        suppress_warnings: bool = False,
        **kwargs,
    ):
        """
        Initialize a DC voltage measure datasheet spec of K2450.

        Parameters
        ----------
        name : str
            Name to attach to instance.

        serial : str
            Serial of the K2450.

        v_range : float, optional
            Current range. The default is 'auto'.

        days_since_cal : float, optional
            Days since cal. The default is 365.

        t_ambient : float, optional
            Ambient temperature at time of measurement. The default is 26 C.

        suppress_warnings
            Suppress warning output to the console. The default is False.

        Returns
        -------
        None.

        """
        # init as a _k2401 datashee specification
        self.v_range = v_range
        _k2401_datasheet.__init__(
            self,
            name,
            serial,
            reading_range=v_range,
            days_since_cal=days_since_cal,
            t_ambient=t_ambient,
            spec_type=_DCV,
            source=False,
            suppress_warnings=suppress_warnings,
            **kwargs,
        )

        # init as an dcv measure spec
        Specification.__init__(
            self, name, serial, self.n_mechanisms, self.mechanism_functions
        )


# class DatasheetSourceDCV(_k2401_datasheet, _ispecs.DatasheetSourceDCV):
class DatasheetSourceDCV(_k2401_datasheet, Specification):
    """DC Voltage Source class of K2450 datasheet spec."""

    def __init__(
        self,
        name: str,
        serial: str,
        v_range: float = None,
        days_since_cal: float = None,
        t_ambient: float = None,
        suppress_warnings: bool = False,
        **kwargs,
    ):
        """
        Intialize a DC voltage sourcing datasheet spec of K2450.

        Parameters
        ----------
        name : str
            Name to attach to instance.

        serial : str
            Serial of the K2450.

        v_range : float, optional
            Current range. The default is 'auto'.

        days_since_cal : float, optional
            Days since cal. The default is 365.

        t_ambient : float, optional
            Ambient temperature at time of measurement. The default is 26 C.

        suppress_warnings
            Suppress warning output to the console. The default is False.

        Returns
        -------
        None.

        """
        # init as a _k2401 datashee specification
        self.v_range = v_range
        _k2401_datasheet.__init__(
            self,
            name,
            serial,
            reading_range=v_range,
            days_since_cal=days_since_cal,
            t_ambient=t_ambient,
            spec_type=_DCV,
            source=True,
            suppress_warnings=suppress_warnings,
            **kwargs,
        )

        # init as an dcv source spec
        Specification.__init__(
            self, name, serial, self.n_mechanisms, self.mechanism_functions
        )


# class DatasheetMeasureDCI(_k2401_datasheet, _ispecs.DatasheetMeasureDCI):
class DatasheetMeasureDCI(_k2401_datasheet, Specification):
    """DC Current Measure class of K2450 datasheet spec."""

    def __init__(
        self,
        name: str,
        serial: str,
        i_range: float = None,
        days_since_cal: float = None,
        t_ambient: float = None,
        suppress_warnings: bool = False,
        **kwargs,
    ):
        """
        Intialize a DC current measuring datasheet spec of K2450.

        Parameters
        ----------
        name : str
            Name to attach to instance.

        serial : str
            Serial of the K2450.

        i_range : float, optional
            Current range. The default is 'auto'.

        days_since_cal : float, optional
            Days since cal. The default is 365.

        t_ambient : float, optional
            Ambient temperature at time of measurement. The default is 26 C.

        suppress_warnings
            Suppress warning output to the console. The default is False.

        Returns
        -------
        None.

        """
        # init as a _k2401 datashee specification
        self.i_range = i_range
        _k2401_datasheet.__init__(
            self,
            name,
            serial,
            reading_range=i_range,
            days_since_cal=days_since_cal,
            t_ambient=t_ambient,
            spec_type=_DCI,
            source=False,
            suppress_warnings=suppress_warnings,
            **kwargs,
        )

        # init as an dci measure spec
        Specification.__init__(
            self, name, serial, self.n_mechanisms, self.mechanism_functions
        )


# class DatasheetSourceDCI(_k2401_datasheet, _ispecs.DatasheetSourceDCI):
class DatasheetSourceDCI(_k2401_datasheet, Specification):
    """DC Current Source class of K2450 datasheet spec."""

    def __init__(
        self,
        name: str,
        serial: str,
        i_range: float = None,
        days_since_cal: float = None,
        t_ambient: float = None,
        suppress_warnings: bool = False,
        **kwargs,
    ):
        """
        Intialize a DC current sourcing spec of K2450 datasheet.

        Parameters
        ----------
        name : str
            Name to attach to instance.

        serial : str
            Serial of the K2450.

        i_range : float, optional
            Current range. The default is 'auto'.

        days_since_cal : float, optional
            Days since cal. The default is 365.

        t_ambient : float, optional
            Ambient temperature at time of measurement. The default is 26 C.

        suppress_warnings
            Suppress warning output to the console. The default is False.

        Returns
        -------
        None.

        """
        # init as a _k2401 datashee specification
        self.i_range = i_range
        _k2401_datasheet.__init__(
            self,
            name,
            serial,
            reading_range=i_range,
            days_since_cal=days_since_cal,
            t_ambient=t_ambient,
            spec_type=_DCI,
            source=True,
            suppress_warnings=suppress_warnings,
            **kwargs,
        )

        # init as an dci source spec
        Specification.__init__(
            self, name, serial, self.n_mechanisms, self.mechanism_functions
        )


if __name__ == '__main__':
    serial = 'asd'
    name = 'asd'
    DatasheetMeasureDCV('MV', '000')
    DatasheetSourceDCV('SV', '111')
    DatasheetMeasureDCI('MI', '222')
    DatasheetSourceDCI('SI', '333')
