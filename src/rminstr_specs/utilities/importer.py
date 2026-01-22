"""Importer utilities for calorimeter-python."""

from pathlib import Path
import importlib.util as _ilutil
import sys as _sys
import os as _os

def import_specs(model_name: str, functionality: str) -> type:
    """
    Import an instrument model/functionality by string.

    Parameters
    ----------
    model_name : str
        Name of of instrument model to import the spec sheet of.

    functionality : str
        Name of measurement functionality to import, this is the spec sheet so DatasheetDCV for example.

    Returns
    -------
    Specification
        Specification class.

    """
    mod_str = 'rminstr_specs.' + model_name
    if (spec := _ilutil.find_spec(mod_str)) is not None:
        # If you chose to perform the actual import ...
        mod = _ilutil.module_from_spec(spec)
        _sys.modules[mod_str] = mod
        spec.loader.exec_module(mod)
        cls = getattr(mod, functionality)
    return cls