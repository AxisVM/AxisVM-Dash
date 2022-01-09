# -*- coding: utf-8 -*-
from collections import Iterable
import six
import numpy as np


def issequence(arg):
    """
    A sequence is an iterable, but not any kind of string.
    """
    return (
        isinstance(arg, Iterable)
        and not isinstance(arg, six.string_types)
    )
    
    
def floatformatter(*args, sig=6, **kwargs):
    """
    Formatter for a specified number of significant digits.
    """
    return "{" + "0:.{}g".format(sig) + "}"


def float_to_str_sig(value, *args, sig: int=6, atol: float=1e-7, **kwargs):
    """
    Returns a string representation of a floating point number, with
    given significant digits.

    Parameters
    ----------
    value : float or a sequence of floats
        A single value, or an iterable.

    sig : int
        Number of significant digits.

    atol : float
        Floating point tolerance. Values smaller than this 
        in the absolute sense are treated as zero.

    Returns
    -------
    string or a sequence of strings
        String representation of the provided input.
    """
    if not issequence(value):
        if atol is not None:
            if abs(value) < atol:
                value = 0.0
        return floatformatter(sig=sig).format(value)
    else:
        value = np.array(value)
        if atol is not None:
            inds = np.where(np.abs(value) < atol)[0]
            value[inds] = 0.0
        formatter = floatformatter(sig=sig)
        def f(v): return formatter.format(v)
        return list(map(f, value))
    