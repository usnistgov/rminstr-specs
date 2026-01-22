"""
Datasheet Accuracy Interfaces
=============================

In this example, we use create datasheet specification
for DC Voltage measurements on an HP3458A Digital Multi Meter.

Every instrument provides class interfaces
where measurements can be provided. The state of the
instrument is provided to the constructor.

If not enough key word arguments are provided to the constructor,
the default assumptions about the state of the instrument are
printed as warnings.
"""

from rminstr_specs import HP3458A
import numpy as np


voltage_specs = HP3458A.DatasheetDCV()

# %%
# After creating your spec sheet, supply measurements
# to get an uncertainty estimate. The uncertainties
# are always returned as the standard uncertainty (i.e.
# standard deviation) of
# the assumed probability distribution. The probablity
# distribution is assumed to be uniform
# unless otherwise specified.


# Supply 1d numpy arrays to ``all_manufacturer_errors``
# to get a 1d numpy where the elements of the output
# corresponds to the estimated standard uncertainty
# on the inputs based on the

my_measurements = np.array([0.1, 1.0, 2.0])
my_accuracy = voltage_specs.all_manufacturer_errors(my_measurements)
