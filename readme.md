# rminstr_specs

This package is a library of classes that provides accuracy specifications for instruments
commonly used in the RF power calibration service at NIST. The manufacturer data sheet specifications can then be used as part of an uncertainty analysis when performing our RF calibrations. This package facilitates this analysis by providing an easy interface into these
validated specification sheets via a python interface.

For example, to get the uncertainty associated with voltage measurements of an HP 3458A voltmeter
under typical operating conditions, you can do the following:

```python
from rminstr_specs import HP3458A
import numpy as np

# make a spec sheet
voltage_specs =  HP3458A.DatasheetDCV()
# create measurements
my_measurements = np.array([0.1, 1.0, 2.0])
# supply to spec sheet
my_accuracy = voltage_specs.all_manufacturer_errors(my_measurements)
```

Read the [pages](https://pages.nist.gov/rminstr-specs-ipages) for code API and examples.


## Authors

Contributors names and contact info

Daniel C. Gray, Zenn C. Roberts, Aaron M. Hagerstrom

