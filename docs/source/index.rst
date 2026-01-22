Rocky Mountain Instrument Specifications
========================================

This package is a library of classes that provide manufacturer data sheet specifications for instruments
commonly used in the RF power calibration service at NIST. The manufacturer data sheet specifications - which we
verify with DC voltage standards traceable to the SI - can then be used as part of an uncertainty analysis when
performing our RF calibrations. This package facilitates this analysis by providing an easy interface into these
validated specification sheets via a python interface.

For example, to get the uncertainty associated with voltage measurements of an HP 3458A voltmeter
under typicaly operating conditions, you can do the following:

.. code-block:: python
   from rminstr_specs import HP3458A
   import numpy as np

   # make a spec sheet
   voltage_specs =  HP3458A.DatasheetDCV()
   # create measurements
   my_measurements = np.array([0.1, 1.0, 2.0])
   # supply to spec sheet
   my_accuracy = voltage_specs.all_manufacturer_errors(my_measurements)

Table of Contents
=================

.. toctree::
   :maxdepth: 4

   auto_examples/index.rst
   for_contributors/index.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _GUM: https://jcgm.bipm.org/vim/en/2.41.html
.. _FAIR: https://www.go-fair.org/fair-principles/
