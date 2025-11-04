# frac2dec
Minimal-width formatting of decimal approximations

This module supplies tools to help create nice decimal literals
for numeric types, particularly of type `fractions.Fraction.

Let's set up some helpers. This file is exeecuted by Python's doctest
module to verify all the examples work exactly as shown, so we need to
define everything we use.


```python
>>> from frac2dec import format_fixed, frac2dec
>>> from fractions import Fraction as F
>>> from decimal import Decimal as D

>>> def show(fs, **kws):
...     for s in format_fixed(fs, **kws):
...         print(s)

```

## Function `format_fixed()`

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
>>> args = sorted(F(pick(), pick()) for i in range(8))
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
>>> D(-80.1) # thw exact decimal value
Decimal('-80.099999999999994315658113919198513031005859375')

```

## Class `frac2dec`

`c = frac2dec(f)` creatws an object that can be used to show
increasingly accurate decimal-string approximations to the number f's
infinitely precise value.

`f` can be anything convertible to a `fraction.Fraction. `c.get(nfrac)`
returns a decimal literal string, correctly rounded (nearest/even)
to `nfrac` fractional digits.

Before `.get()` is called, `c.nfrac` is -1, and `c.exact` is `True` if
and only the value is an exact integer (no fractional part).

```python
>>> anint = frac2dec(D("0.103e4"))
>>> anint.nfrac; anint.exact
-1
True
>>> notint = frac2dec(D("10.3"))
>>> notint.nfrac; notint.exact
-1
False

```

After calling `c.get(nfrac)`, `c.nfrac` is `nfrac`, and `c.exact` is
`True` if and only if the string returned reproduces the exact infinitely
precise value. When `.exact` is `True`, calling `get()` with larger
`nfrac` values will only add trailing zeroes.


```python
>>> c = frac2dec(F(-7, 4))
>>> for nfrac in range(5):
...     print(c.get(nfrac), c.nfrac, c.exact)
-2 0 False
-1.8 1 False
-1.75 2 True
-1.750 3 True
-1.7500 4 True

```

For any float input, `c.exact` will eventually become `True` as `nfrac`
increases. Bur `c.exact` will always remain `False` for an input like
`Fraction(2, 3)`.

```python
>>> c = frac2dec(0.1)
>>> for nfrac in range(505):
...     ignore = c.get(nfrac)
...     if c.exact:
...         break
>>> print("exact at nfrac =", c.nfrac)
exact at nfrac = 55
>>> print(c.get(c.nfrac))
0.1000000000000000055511151231257827021181583404541015625
>>> print(D(.1)) # the same
0.1000000000000000055511151231257827021181583404541015625

>>> c = frac2dec(F(2, 3))
>>> for nfrac in range(8):
...     print(c.get(nfrac), c.exact)
1 False
0.7 False
0.67 False
0.667 False
0.6667 False
0.66667 False
0.666667 False
0.6666667 False

>>> c.get(-1)
Traceback (most recent call last):
  ...
ValueError: ('nfrac must be >= 0 not', -1)

```
