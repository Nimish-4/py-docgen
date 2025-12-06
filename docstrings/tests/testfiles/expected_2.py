class xyz:
    """One line summary for the class and its purpose.

    The __init__ method can be documented either here, or have its separate
    docstring in the method itself. Stick with one of the two choices.
    This paragraph (and others that may follow) are for explaining the
    class in more detail.

    After closing the class docstring, there should be one blank line to
    separate following codes (PEP257).

    Note
    ----
    The `self` parameter is not listed as the first parameter of methods.

    Parameters
    ----------
    num : float
        The number to be used for operations.

    msg : str (default: "")
        Message to be displayed.

    Attributes
    ----------
    x : int
        Description of attribute `x`

    Examples
    --------
    Import an example class

    >>> from foo import bar
    >>> y = bar(3.14)

    References
    ----------
    [1] https://numpydoc.readthedocs.io/en/latest/
    """

    def __init__(self, a, b):
        """Initialize `a` and `b`"""
        self.a = a
        self.b = b

    def calculate(self):
        """Calculate the sum of `a` and `b`"""
        return self.a + self.b
