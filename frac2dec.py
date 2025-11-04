__version__ = "0.9"

__all__ = ["format_fixed",
           "frac2dec",
          ]

from fractions import Fraction
_HALF = Fraction(1, 2)

class frac2dec:
    def __init__(self, f):
        self.prefix = ''
        if f < 0:
            self.prefix = '-'
            f = -f
        f = Fraction(f)
        self.nfrac = -1
        self.intpart = int(f)
        self.rem = f - self.intpart
        self.exact = not self.rem
        self.canned = None

    def get(self, nfrac):
        """Return decimal string with `nfrac` fractional digits.

        >>> frac2dec(2/3).get(3)
        '0.667'
        """

        if nfrac < 0:
            raise ValueError("nfrac must be >= 0 not", nfrac)
        if nfrac == self.nfrac:
            return self.canned
        self.nfrac = nfrac
        pow10 = 10 ** nfrac
        i = self.rem * pow10
        newdiga = int(i)
        rem = i - newdiga
        self.exact = not rem
        digs = self.intpart * pow10 + newdiga
        if (rem > _HALF
              or (rem == _HALF and (digs & 1))):
            digs += 1
        s = str(digs)
        if len(s) < nfrac:
            s = s.rjust(nfrac, '0')
        if nfrac:
            s = s[:-nfrac] + '.' + s[-nfrac:]
            if s[0] == '.':
                s = '0' + s
        self.canned = self.prefix + s
        return self.canned

def format_fixed(fs, /, *, minfrac=0, extra=0):
    """Return list of decimal strings with minimal fractional digits.

    >>> format_fixed(200 + i / 1000 for i in range(6))
    ['200.000', '200.001', '200.002', '200.003', '200.004', '200.005']
    """

    if minfrac < 0:
        raise ValueError("minfrac must be >= 0, not", minfrac)
    if extra < 0:
        raise ValueError("extra must be >= 0, not", extra)
    fs = tuple(map(Fraction, fs))
    unique = set(fs)
    u2c = {f : frac2dec(f) for f in unique}
    cs = u2c.values()
    nfrac = minfrac
    if not nfrac and not all(c. exact for c in cs):
        nfrac = 1
    while True:
        seen = set()
        for c in cs:
            this = c.get(nfrac)
            if this in seen:
                break
            seen.add(this)
        else:
            break
        nfrac += 1
    nfrac += extra
    final = [u2c[f].get(nfrac) for f in fs]
    huge = max(map(len, final))
    return [s.rjust(huge) for s in final]

if __name__ == "__main__":
    import doctest, os
    TESTFN = "README.md"
    print(doctest.testmod())
    if os.path.exists(TESTFN):
        print(doctest.testfile(TESTFN))
    else:
        print("tesr file", TESTFN, "not found")
