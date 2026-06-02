def calculate(a, b, c=5):
    """Summarize the function in one line.

    Several sentences providing an extended description. Refer to
    variables using back-ticks, e.g. `var`. For functions (also method and module),
    there should be no blank lines after closing the docstring.

    Parameters
    ----------
    a: type (default:)
        Explanation of a.

    b: type (default:)
        Explanation of b.

    c: type (default:)
        Explanation of c.

    Returns
    -------
    describe : type
        Explanation of return value named `describe`.

    Examples
    --------

    >>> a = [1, 2, 3]
    >>> print([x + 3 for x in a])
    [4, 5, 6]
    """
    return a + b + c


def do_nothing():
   """Summarize the function in one line.

   Several sentences providing an extended description. Refer to
   variables using back-ticks, e.g. `var`. For functions (also method and module),
   there should be no blank lines after closing the docstring.

   Parameters
   ----------

   Returns
   -------
   describe : type
       Explanation of return value named `describe`.

   Examples
   --------

   >>> a = [1, 2, 3]
   >>> print([x + 3 for x in a])
   [4, 5, 6]
   """
   print("Do nothing")
   return
