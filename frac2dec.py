import sys

from fractions import Fraction
_HALF = Fraction(1, 2)

# `c = frac2dec(f)` creatss an object that cna be used to show
# increasingly accurate decimal-string approximations to the number f's
# inifnitely precise value.
#
# `f` can be anything convertiblae to a frac2dec.Fraction.
#
# c.get() reutns the current decimal stinng. It's correctly rounded
# (nearest/even) to the number of digits in the returned string.
#
# After consruction, c.get() returns `f` rounded to the nearest
# integer, and without a decimal point.
#
# Each call to c.next() adds anotger decimal digit to the displayed
# string, increasing precision, and returns the result of c.get().
#
# At any point, c.exact is True if anonly if the then-current string
# shows the exact value of `f`. Further calls to c.next() will only
# add more trailing zeroes then.
#
# For any float input, c.exact will eventually become Teuw. Bur c.exact
# will always remain False for an input like Fraction(2, 3).

class frac2dec:
    def __init__(self, f):
        self.prefix = ''
        if f < 0:
            self.prefix = '-'
            f = -f
        f = Fraction(f)
        self.nfrac = 0
        self.intpart = int(f)
        self.rem = f - self.intpart
        self.exact = not self.rem
        self.canned = None

    def get(self, nfrac):
        if nfrac < 0:
            raise ValueError("nfrac must be >= 0 not", nfrac)
        if nfrac == self.nfrac and self.canned:
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

def format_fixed(fs, minfrac=0):
    if minfrac < 0:
        raise ValueError("minfrac must be >= 0, not", minfrac)
    fs = tuple(map(Fraction, fs))
    unique = set(fs)
    u2c = {f : frac2dec(f) for f in unique}
    cs = u2c.values()
    nfrac = minfrac
    if not nfrac and not all(c. exact for c in cs):
        nfrac = 1
    while len(set(c.get(nfrac) for c in cs)) < len(unique):
        nfrac += 1
    final = [u2c[f].get(nfrac) for f in fs]
    huge = max(map(len, final))
    return [s.rjust(huge) for s in final]

#### [Reweighted Range Voting: Round 5: Score round]
####  The highest-scoring candidate wins a seat.
##    dat = """\
##       Condorcet (Ranked Pairs)              -- 17+ 81055103/89237148   (average  1598086619/2141691552)  -- First place
##       Reweighted Range Voting               -- 15+ 10730924/66927861   (average  1014648839/1606268664)
##       Condorcet (Schulze)                   -- 14+216137707/1070845776 (average 15207978571/25700298624)
##       Proportional Block Approval (Webster) -- 14+ 24716971/133855722  (average  1898697079/3212537328)
##"""
#### Condorcet (Ranked Pairs) wins a seat.
##
##
##    scores = []
##    avgs = []
##    import re
##    for line in dat.splitlines():
##        a, b, c, d, e = map(int, re.findall(r'\d+', line))
##        print(a, b, c, d, e)
##        scores.append(a + Fraction(b, c))
##        avgs.append(Fraction(d, e))
##    for i in format_fixed(scores):
##        print(i)
##    for i in format_fixed(avgs):
##        print(i)

_ord = """\
```python
>>> c = frac2dec(8.75)
>>> c.exact
False
>>> c.get(0), c.exact
('9', False)
>>> c.get(1), c.exact
('8.8', False)
>>> c.get(2), c.exact
('8.75', True)
>>> c.get(3), c.exact
('8.750', True)
>>> c.get(4), c.exact
('8.7500', True)

>>> c = frac2dec(0.99)
>>> for nfrac in range(500):
...     c.get(nfrac)
...     if c.exact:
...         break
'1'
'1.0'
'0.99'
'0.990'
'0.9900'
'0.99000'
'0.990000'
'0.9900000'
'0.99000000'
'0.990000000'
'0.9900000000'
'0.99000000000'
'0.990000000000'
'0.9900000000000'
'0.99000000000000'
'0.990000000000000'
'0.9900000000000000'
'0.98999999999999999'
'0.989999999999999991'
'0.9899999999999999911'
'0.98999999999999999112'
'0.989999999999999991118'
'0.9899999999999999911182'
'0.98999999999999999111822'
'0.989999999999999991118216'
'0.9899999999999999911182158'
'0.98999999999999999111821580'
'0.989999999999999991118215803'
'0.9899999999999999911182158030'
'0.98999999999999999111821580300'
'0.989999999999999991118215802999'
'0.9899999999999999911182158029987'
'0.98999999999999999111821580299875'
'0.989999999999999991118215802998748'
'0.9899999999999999911182158029987477'
'0.98999999999999999111821580299874768'
'0.989999999999999991118215802998747677'
'0.9899999999999999911182158029987476766'
'0.98999999999999999111821580299874767661'
'0.989999999999999991118215802998747676611'
'0.9899999999999999911182158029987476766109'
'0.98999999999999999111821580299874767661095'
'0.989999999999999991118215802998747676610947'
'0.9899999999999999911182158029987476766109467'
'0.98999999999999999111821580299874767661094666'
'0.989999999999999991118215802998747676610946655'
'0.9899999999999999911182158029987476766109466553'
'0.98999999999999999111821580299874767661094665527'
'0.989999999999999991118215802998747676610946655273'
'0.9899999999999999911182158029987476766109466552734'
'0.98999999999999999111821580299874767661094665527344'
'0.989999999999999991118215802998747676610946655273438'
'0.9899999999999999911182158029987476766109466552734375'
>>> c.nfrac
52
>>> c.get(nfrac + 1)
'0.98999999999999999111821580299874767661094665527343750'

>>> c = frac2dec(Fraction(2, 3))
>>> c.get(0)
'1'
>>> c.get(1)
'0.7'
>>> c.get(3)
'0.667'
>>> c.get(-1)
Traceback (most recent call last):
  ...
ValueError: ('nfrac must be >= 0 not', -1)

```
"""

_formfix = """\
`format_fixed(fs, minfrac=0)` ia used to format a compact column of
numbers. `fs` is an iterable of numbers, which can be of any type
convertible to Fraction (int, float, Fraction, Decimal). Such
conversions are exact.

Return a list of strings, one per input number. Each string is a decimal
fixed-point literal, correctly rounded (nearest/even) to the number of
digits given. All strings have the same length, and the same number of
digits after the decimal point, and are right-justified (if needed)
with blanks on the left. So they make a nice, readable visual display if
printed on successive lines.

In general, and this is the real point, the fewest number of fractional
digits are used so that non-equal inputs produce different strings.

Let's set up some helpers:

```python
>>> from fractions import Fraction as F
>>> from decimal import Decimal as D

>>> def show(fs, **kws):
...     for s in format_fixed(fs, **kws):
...         print(s)

```

If all values are exact integers, there is no decimal point:

```python
>>> args = [8, .125 * 64, D('.008e3'), F(240, 3)]
>>> show(args)
 8
 8
 8
80

```

However, a minimum number of fractional digits can be asked for:

```python
>>> show(args, minfrac=2)
 8.00
 8.00
 8.00
80.00

```

If not all inputs are exact integers, at least one fractional digit will
be produced even if all the inputs round to different integers:

```python
>>> show([7, 8.01, 9])
7.0
8.0
9.0

```

Now for a useful case ;-) Suppose you have large Fractions to display.
That's hard to do in a readable way!

```python
>>> from random import randrange, seed
>>> seed(123443210)
>>> pick = lambda: randrange(10**30)
>>> args = sorted(Fraction(pick(), pick()) for i in range(8))
>>> for f in args:
...     print(f)
100383010337217770703803396671/873361031336288422121036518616
46287472345949520949917544096/351877543542290630359106324699
209242411848949090107270270805/972625171789306895730155705174
137906878848974880762102969909/438084787371253463626047013078
505578408574423373749931556697/960216838779667583921785159607
348837406967948132874002110042/644965611579915714804829263423
407533651144918602524371484247/16370165895327991366035343826
7474266912747442329837528014/140583509049204837043199255

```

Quite a mess! Behold:

```python
>>> show(args)
 0.11
 0.13
 0.22
 0.31
 0.53
 0.54
24.89
53.17

```

Those are correctly rounded decimal approximations, with just enough
fractional digits so that all strings are pairwise distinct.

Caution: if you have just one distinct small number, it will probably
round to 0:

```python
>>> show([-80.1, 1e-12, 1e-12])
-80.1
  0.0
  0.0

```

However, if you have more than one, enough fractional digits will be
produced so that they can be distinguished:

```python
>>> show([-80.1, 1e-22, 1e-23])
-80.0999999999999943156581
  0.0000000000000000000001
  0.0000000000000000000000

```

What happened to -80.1? That's in fact the correctly rounded decimal
approximation to the binary approximation floats use for -80.1.

```python
>>> D(-80.1) # rhw exact decimal value
Decimal('-80.099999999999994315658113919198513031005859375')

```
"""

__test__ = {"ordinary": _ord,
            "formfix": _formfix}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
