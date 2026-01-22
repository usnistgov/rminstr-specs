# Rocky Mountain Instrument Specifications

> [!NOTE]
> This software is in active and early development by the RF power calibrations service at NIST to support
> RF power calibrations and the development primary RF power standards. Expect breaking breaking changes as the software
> evolves. Instruments are added and tested as needed. Bugs may
> be present that we are unaware of. Please exercise caution and verify the output of this library yourself.

This package is a library of classes that provide manufacturer data sheet specifications for instruments
commonly used in the RF power calibration service at NIST. The manufacturer data sheet specifications - which we
verify with DC voltage standards traceable to the SI - can then be used as part of an uncertainty analysis when
performing our RF calibrations. This package facilitates this analysis by providing an easy interface into these
validated specification sheets via a python interface.

For example, to get the uncertainty associated with voltage measurements of an HP 3458A voltmeter
under typicaly operating conditions, you can do the following:

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


## Developer Tools
It is assumed you have the following programs installed on your computer.

* [uv](https://docs.astral.sh/uv/) for package management
* [git bash](https://git-scm.com/downloads) or similar terminal emulator to run shell scripts if you are on windows.

Clone the repo and run, from the root directory:
```
uv sync
```
This will generate the virtual environment for the package.

Install git pre-commit:
```
uv run pre-commit install
```

### Running Local Tests
In a bash terminal, run:

```
tools/test.sh
tools/test.sh open
```
This should execute all the defined tests with
[pytest](https://docs.pytest.org/en/stable/). In addition, the
open command will open a webpage with detailed reports about
code coverage.

### Building Local Documentation
Clean the local documentation build (this needs to be run sometimes
if you are modifying the documentation and it gets into a broken state). It will reset the build directories and the next call to
build it will be completely from scratch.
```
tools/docs.sh clean
```

To build a copy of the current state
of the documentation with your changes run:
```
tools/docs.sh html
```

To build the full documentation with tagged
versions and the most recent stable and development
changes (this takes a while and is usually only run
as part of the release jobs) run:

```
tools/docs.sh html-multiversioned
```

To open the documentation (you may have to call open
in a newe console) run

```
tools/docs.sh serve
tools/docs.sh open
```

This will serve a local copy of the documentation on your local host,
and the open command will launch your default web browser directly to that page.
Currently, this web page is on port 8000.

### Code Profiling
If you are writing a test script, you can run it in a code
profile from the cloned directory. This will open a webpage
to navigate the statistics of your tests script once it
complete.

```
tools/profile.sh <path/to/script.py>
```

## Authors

Contributors names and contact info

Daniel C. Gray, Zenn C. Roberts, Aaron M. Hagerstrom

