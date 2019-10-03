"""
A set of methods for bitwise arithmetic
As well as a class of synthetic floating point numbers and related arithmetic
"""


def add(a, b):
    """
    Simple bitwise add with cycle
    >>> results = list()
    >>> for a in range(-15, 15):
    ...    for b in range(-15, 15):
    ...       results.append(add(a, b) == a + b)
    >>> all(results)
    True
    """
    if a < 0 < b and abs(a) < abs(b):
        return minus(b, abs(a))
    if a > 0 > b and abs(a) > abs(b):
        return minus(a, abs(b))
    if abs(a) == abs(b) and a != b:
        return 0
    a, b = a ^ b, a & b
    while b:
        b <<= 1
        a, b = a ^ b, a & b
    return a


def plus(a, b):
    """
    Simple bitwise add with recursion
    >>> results = list()
    >>> for a in range(-15, 15):
    ...    for b in range(-15, 15):
    ...       results.append(plus(a, b) == a + b)
    >>> all(results)
    True
    """
    if a < 0 < b and abs(a) < abs(b):
        return minus(b, abs(a))
    if a > 0 > b and abs(a) > abs(b):
        return minus(a, abs(b))
    if abs(a) == abs(b) and a != b:
        return 0

    if not b:
        return a
    return plus(a ^ b, (a & b) << 1)


def sub(a, b):
    """
    Simple bitwise sub with cycle
    >>> results = list()
    >>> for a in range(-15, 15):
    ...    for b in range(-15, 15):
    ...       results.append(sub(a, b) == a - b)
    >>> all(results)
    True
    """
    subzero = a < b
    if subzero:
        a, b = b, a

    a, b = a ^ b, ~a & b
    while b:
        b <<= 1
        a, b = a ^ b, ~a & b

    if subzero:
        return increment(~a)
    return a


def minus(a, b, subzero=False):
    """
    simple bitwise sub with recursion
    >>> results = list()
    >>> for a in range(-15, 15):
    ...    for b in range(-15, 15):
    ...       results.append(minus(a, b) == a - b)
    >>> all(results)
    True
    """
    if a < b:
        subzero = True
        a, b = b, a

    if not b:
        if subzero:
            return increment(~a)
        return a
    return minus(a ^ b, (~a & b) << 1, subzero)


def mul(a, b):
    """
    simple bitwise mul
    >>> results = list()
    >>> for a in range(-15, 15):
    ...    for b in range(-15, 15):
    ...       results.append(mul(a, b) == a * b)
    >>> all(results)
    True
    """
    subzero = False
    if a < 0 and b < 0:
        a, b = abs(a), abs(b)
    elif b < 0:
        b = abs(b)
        subzero = True
    elif a < 0:
        a = abs(a)
        subzero = True

    result = 0
    while b != 0:
        if b & 1 == 1:
            result = plus(result, a)
        a <<= 1
        b >>= 1
    if subzero:
        return increment(~result)
    return result


def _divisible(a, b):
    """
    help function
    can we get a with mul(b, 1..n)?
    >>> results = list()
    >>> for a in range(-15, 15):
    ...    for b in range(-15, 15):
    ...       dc = _divisible(a, b)
    ...       if not a or not b:
    ...          mod = float("inf")
    ...       else:
    ...          mod = a % b
    ...       results.append(not dc == bool(mod))
    >>> all(results)
    True
    """
    if abs(a) < abs(b):
        return False
    a, b = abs(a), abs(b)  # sign not required
    i = 1
    r = b
    if a == r and a != 0:
        return True
    if r == 0:
        return False
    while a > r:
        r = mul(b, i)
        if r == a:
            return True
        i = increment(i)
    return False


def div(a, b):
    """
    simple bitwise div
    >>> results = list()
    >>> for a in range(-15, 15):
    ...    for b in list(range(-15, 0)) + list(range(1, 15)):
    ...       results.append(div(a, b) == a // b)
    >>> all(results)
    True
    """
    _a, _b = a, b
    if b == 0:
        raise ZeroDivisionError
    if a == 0:
        return 0

    subzero = False
    if a < 0 and b < 0:
        a, b = abs(a), abs(b)
    elif b < 0:
        b = abs(b)
        subzero = True
    elif a < 0:
        a = abs(a)
        subzero = True

    result = 0
    a_nbits = 0
    a_saved = a
    while a_saved:
        a_nbits = increment(a_nbits)
        a_saved = a_saved >> 1
    b <<= a_nbits
    while a_nbits:
        a = minus(mul(2, a), b)
        if a >= 0:
            result = (result | 1) << 1
        else:
            result <<= 1
            a = plus(a, b)
        a_nbits = decrement(a_nbits)

    result >>= 1

    if subzero:
        if _divisible(_a, _b):
            return increment(~result)
        else:
            return ~result

    return result


def nod(a, b):
    """
    simple bitwise gcd function
    Это древний алгоритм, лучше чем Евклида
    НОД(0, n) = n; НОД(m, 0) = m; НОД(m, m) = m;
    НОД(1, n) = 1; НОД(m, 1) = 1;
    Если m, n чётные, то НОД(m, n) = 2*НОД(m/2, n/2);
    Если m чётное, n нечётное, то НОД(m, n) = НОД(m/2, n);
    Если n чётное, m нечётное, то НОД(m, n) = НОД(m, n/2);
    Если m, n нечётные и n > m, то НОД(m, n) = НОД((n-m)/2, m);
    Если m, n нечётные и n < m, то НОД(m, n) = НОД((m-n)/2, n);
    >>> from math import gcd
    >>> results = list()
    >>> for a in range(-15, 15):
    ...    for b in range(-15, 15):
    ...       results.append(nod(a, b) == gcd(a, b))
    >>> all(results)
    True
    """
    if abs(a) == abs(b):
        return abs(a)
    elif a == 0:
        return abs(b)
    elif b == 0:
        return abs(a)
    elif abs(a) == 1 or abs(b) == 1:
        return 1

    a, b = abs(a), abs(b)

    if not a & 1 and not b & 1:
        return mul(2, nod(div(a, 2), div(b, 2)))
    elif not a & 1 and b & 1:
        return nod(div(a, 2), b)
    elif a & 1 and not b & 1:
        return nod(a, div(b, 2))
    elif a & 1 and b & 1 and b > a:
        return nod(div(sub(b, a), 2), a)
    elif a & 1 and b & 1 and a > b:
        return nod(div(sub(a, b), 2), b)


def mod(a, b):
    """
    simple bitwise divmod
    >>> results = list()
    >>> for a in range(-15, 15):
    ...    for b in list(range(-15, 0)) + list(range(1, 15)):
    ...       results.append(mod(a, b) == a % b)
    >>> all(results)
    True
    """
    return minus(a, mul(div(a, b), b))


def decrement(a):
    """
    simple bitwise --
    >>> results = list()
    >>> for a in range(-15, 15):
    ...     results.append(decrement(a) == a - 1)
    >>> all(results)
    True
    """
    return minus(a, 1)


def increment(a):
    """
    simple bitwise ++
    >>> results = list()
    >>> for a in range(-15, 15):
    ...    results.append(increment(a) == a + 1)
    >>> all(results)
    True
    """
    return plus(a, 1)


def power(a, b):
    """
    simple bitwise pow
    >>> results = list()
    >>> for a in range(-5, 5):
    ...    for b in range(-5, 5):
    ...       if b < 0 and a != 1:
    ...           p = 0
    ...       else:
    ...           p = pow(a, b)
    ...       results.append(p == power(a, b))
    >>> all(results)
    True
    """
    if b == 0:
        return 1
    if a == 1:
        return 1
    if b < 0:     # TODO add negative power support
        return 0
    result = 1
    while b:
        result = mul(result, a)
        b = decrement(b)
    return result


def negative(a):
    """
    simple bitwise -a
    >>> results = list()
    >>> for a in range(-15, 15):
    ...    results.append(negative(a) == -a)
    >>> all(results)
    True
    """
    return minus(0, a)


def same(sf: 'Float', rf: float, precision=0.0001):
    """
    Test function, for estimations Float class
    :param sf: (Float) Synthetic float number
    :param rf: (float) number
    :param precision: (float) comparator precision
    :return: (bool) are very similar objects?
    """
    if abs(rf - float(str(sf))) <= precision:
        return True
    return False


def float_range(start, stop, step):
    """
    Test function, for produce float sequences
    :param start: (float) from
    :param stop: (float) to
    :param step: (float) step
    :return: (generator) sequence as range
    """
    while start < stop:
        yield round(start, 8)
        start += step


class Float(object):
    """
    Synthetic float
    """
    BITS = 16  # bits per integer and fractional parts

    def __init__(self, num=0):
        """
        :param num:
        >>> n = 15.24
        >>> f = Float(n)
        >>> f.representation_int
        998768
        >>> print(f)
        15.2399902343750000
        >>> Float(float(str(f)))
        Float(15.239990234375)
        >>> f
        Float(15.24)
        >>> f.representation_str
        '0000000000001111.0011110101110000'
        >>> f.integer_str
        '15'
        >>> f.fractional_str
        '2399902343750000'
        >>> same(f, n)
        True
        >>> Float(1).representation_int
        65536
        >>> Float(0.1).representation_int
        6553
        >>> results = list()
        >>> for i in float_range(-32, 32, 0.4):
        ...     results.append(same(Float(i), i))  # 1 << 5 = 32
        >>> all(results)
        True
        """
        self._signed = num < 0
        self._nbits = self.BITS
        self._integer_view = '{:0>%s}' % self._nbits
        self._fractional_view = '{:0<%s}' % self._nbits
        self._view = '{:0>%sb}' % mul(self._nbits, 2)
        self.num = abs(num)
        printable = ''.join((self._integer_view, self._fractional_view)) \
            .format(self.integer_binary, self.fractional_binary)
        self._int = int(printable, 2)

    @property
    def integer_binary(self) -> str:
        return self._get_integer_binary()

    @property
    def fractional_binary(self) -> str:
        return self._get_fractional_binary()

    @property
    def integer_str(self) -> str:
        return str(int(self.num))

    @property
    def fractional_str(self) -> str:
        return self._get_fractional()

    @property
    def representation_int(self) -> int:
        if self._signed:
            return negative(self._int)
        return self._int

    @representation_int.setter
    def representation_int(self, value):
        _value_signed = value < 0
        if _value_signed:
            value = abs(value)
        self._int = value
        binary = self._view.format(value)
        i = int(self._integer_view.format(binary[:self._nbits]), 2)
        f = int(self._fractional_view.format(binary[self._nbits:]), 2)
        b = f"{abs(i)}.{abs(f)}"
        if self._signed and _value_signed:
            self._signed = True
        elif self._signed:
            self._signed = False
        elif _value_signed:
            self._signed = True
        else:
            self._signed = False
        self.num = float(b)

    @property
    def representation_str(self) -> str:
        return '.'.join((self._integer_view, self._fractional_view)).\
            format(self.integer_binary, self.fractional_binary)

    def _get_integer_binary(self, num=None) -> str:
        """
        >>> n = 15.27
        >>> f = Float(n)
        >>> f.integer_binary
        '1111'
        >>> f.integer_binary == f"{int(n):b}"
        True
        """
        integer = num if num is not None else self.num
        if "." in str(integer):
            integer = str(integer).split('.')[0]
        return '{:b}'.format(int(integer))

    def _get_fractional_binary(self, num=None) -> str:
        """
        >>> n = 15.27
        >>> f = Float(n)
        >>> f.fractional_binary
        '0100010100011110'
        """
        num = num if num is not None else self.num
        if "." not in str(num):
            return ""
        fractional = str(num).split('.')[1]
        fractional = int(self._fractional_view.format(fractional))
        result = list()
        bits = self._nbits
        while fractional and bits:
            fractional = mul(fractional, 2)
            if fractional >= power(10, self._nbits):
                result.append('1')
                fractional = minus(fractional, power(10, self._nbits))
            else:
                result.append('0')
            bits = decrement(bits)
        return ''.join(result)

    def _get_fractional(self) -> str:
        """
        >>> f = Float(15.27)
        >>> f.fractional_str
        '2699890136718750'
        """
        result = 0
        n = self._nbits
        step = self._nbits
        k = 5
        saved_first = str(k)
        for i in self.fractional_binary:
            num = power(k, increment(minus(self._nbits, n)))
            if saved_first < str(num)[0]:
                step = decrement(step)
            saved_first = str(num)[0]
            if i == '1':
                formatter = '{:0<%s}' % str(step)
                result = plus(result, int(formatter.format(num)))
            n = decrement(n)
        return self._integer_view.format(result)

    def __str__(self) -> str:
        str_ = '.'.join((self.integer_str, self.fractional_str))
        if self._signed:
            str_ = f"-{str_}"
        return str_

    def __repr__(self) -> str:
        rpr_ = f"{self.num}"
        if self._signed:
            rpr_ = f"-{rpr_}"
        return f"Float({rpr_})"

    def __rshift__(self, other) -> 'Float':
        """
        >>> f = Float(15.27)
        >>> print(f.representation_int)
        1000734
        >>> f >> 2
        Float(3.53575)
        >>> print(f.representation_int)
        250183
        >>> print(f)
        3.5357360839843750
        >>> f.num
        3.53575
        >>> print(f)
        3.5357360839843750
        >>> results = list()
        >>> for i in float_range(-8, 8, 0.4):
        ...     results.append(same(Float(i) >> 5, int(i) >> 5, 1))
        >>> all(results)
        True
        """
        self.representation_int = self.representation_int >> other
        return self

    def __lshift__(self, other) -> 'Float':
        """
        >>> f = Float(15.27)
        >>> print(f.representation_int)
        1000734
        >>> f << 2
        Float(61.524)
        >>> print(f.representation_int)
        4002936
        >>> print(f)
        61.5239868164062500
        >>> results = list()
        >>> for i in float_range(-8, 8, 0.4):
        ...     results.append(same(Float(i) << 5, int(i) << 5, 32))  # 1 << 5 = 32
        >>> all(results)
        True
        """
        self.representation_int = self.representation_int << other
        return self

    def __lt__(self, other):
        if self.num < other:
            return True
        return False

    def __gt__(self, other):
        if self.num > other:
            return True
        return False

    def __abs__(self):
        return abs(self.num)

    @staticmethod
    def _ri(other):
        if isinstance(other, Float):
            return other.representation_int
        return Float(other).representation_int

    def __xor__(self, other):
        """
        >>> f, g = Float(15.27), Float(12)
        >>> f.representation_int, g.representation_int
        (1000734, 786432)
        >>> Float(f) ^ g, Float(f) ^ 12, 15 ^ 12  # we need Float() to copy object
        (Float(3.17694), Float(3.17694), 3)

        Untestable for ranges, ^ not supported by float
        """
        self.representation_int = self.representation_int ^ self._ri(other)
        return self

    def __and__(self, other):
        """
        >>> f, g = Float(15.27), Float(7.25)
        >>> f.representation_int, g.representation_int
        (1000734, 475136)
        >>> f.representation_str, g.representation_str
        ('0000000000001111.0100010100011110', '0000000000000111.0100000000000000')
        >>> Float(f) & g, Float(f) & 7, 15 & 7
        (Float(7.16384), Float(7.0), 7)

        Untestable for ranges, ^ not supported by float
        """
        self.representation_int = self.representation_int & self._ri(other)
        return self

    def __add__(self, other):
        """
        >>> f, g = Float(15.27), Float(7.25)
        >>> Float(f) + g, Float(f) + 7.25, 15.27 + 7.25
        (Float(22.34078), Float(22.34078), 22.52)
        >>> results = list()
        >>> for i in float_range(-4, 4, 0.4):
        ...     for j in float_range(-4, 4, 0.4):
        ...         results.append(same(Float(i) + Float(j), i + j, 0.5))
        >>> all(results)
        True
        """
        self.representation_int = plus(self.representation_int, self._ri(other))
        return self

    def __sub__(self, other):
        """
        >>> f, g = Float(15.27), Float(7.25)
        >>> Float(f) - g, Float(f) - 7.25, 15.27 - 7.25
        (Float(8.131), Float(8.131), 8.02)
        >>> results = list()
        >>> for i in float_range(-4, 4, 0.4):
        ...     for j in float_range(-4, 4, 0.4):
        ...         results.append(same(Float(i) - Float(j), i - j, 0.5))
        >>> all(results)
        True
        """
        self.representation_int = minus(self.representation_int, self._ri(other))
        return self

    def __mul__(self, other):
        """
        >>> f, g = Float(15.27), Float(7.25)
        >>> Float(f) * g, Float(f) * 7.25, 15.27 * 7.25
        (Float(110.46361), Float(110.46361), 110.7075)
        >>> results = list()
        >>> for i in float_range(-4, 4, 0.4):
        ...     for j in float_range(-4, 4, 0.4):
        ...         results.append(same(Float(i) * Float(j), i * j, 1))
        >>> all(results)
        True
        """
        self.representation_int = mul(self.representation_int, self._ri(other)) >> self._nbits
        return self

    def __truediv__(self, other):
        """
        >>> f, g = Float(15.27), Float(7.25)
        >>> Float(f) * g, Float(f) * 7.25, 15.27 * 7.25
        (Float(110.46361), Float(110.46361), 110.7075)
        >>> results = list()
        >>> for i in float_range(-8, 8, 0.8):
        ...     for j in float_range(-8, 8, 0.8):
        ...         if not j:
        ...             continue
        ...         results.append(same(Float(i) / Float(j), round(i / j, 5), 1))
        >>> all(results)
        True
        """
        self.representation_int = div(self.representation_int, self._ri(other)) << self._nbits
        return self


class DivFloat(Float):
    BITS = 32

    def __truediv__(self, other):
        """
        >>> results = list()
        >>> for i in [63.5, 22.8, 14, 8.2, 3.33, 1.4, 0.88, 0.1255, 0.004, -0.2, -1.14, -533]:
        ...     for j in [63.5, 22.8, 14, 8.2, 3.33, 1.4, 0.88, 0.1255, 0.004, -0.2, -1.14, -533]:
        ...         results.append(same(DivFloat(i) / DivFloat(j), round(i / j, 5), 1))
        >>> all(results)
        True
        """
        _int = abs(self.representation_int)
        _ont = abs(other.representation_int)
        _self_signed = self.representation_int < 0
        _value_signed = other.representation_int < 0

        x = 0
        while mul(_int, power(10, x)) < power(2, mul(self._nbits, 2)):
            x = increment(x)
        saved = div(mul(_int, power(10, x)), _ont) << self._nbits

        string_view = str(Float(saved)).split('.')[0]

        integer = '{:b}'.format(int(string_view[:negative(x)])) if string_view[:negative(x)] else '0'

        _lead_fr = '0' * minus(x, len(string_view)) if x > len(string_view) else ''
        fractional = self._get_fractional_binary(''.join((_lead_fr, string_view[negative(x):])))

        printable = ''.join((self._integer_view, self._fractional_view)).format(integer, fractional)
        self.representation_int = int(printable, 2) >> self._nbits

        if _self_signed and _value_signed:
            self._signed = False
        elif _self_signed or _value_signed:
            self._signed = True
        else:
            self._signed = False

        return self
