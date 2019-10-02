## Bitwise arithmetic

The module includes functions for addition, subtraction, multiplication, division,
modulo division, finding the greatest common divisor, raising integers to a power.
And a class to simulate  the above operations for floating point numbers

### Integer functions

| Operator   |  Methods   |
|------------|------------|
| -          | add, plus  |
| +          | sub, minus |
| *          | mul        |
| //         | div        |
| math.gcd() | nod        |
| %          | mod        |
| - 1        | decrement  |
| + 1        | increment  |
| pow        | power      |
| -x         | negative   |

### Float

Floating-point synthetic class.

```python
x = Float(-5.23)
x + 3         # by ref
print(x)      # -2.1507263183593750
x * 5
print(x)      # -11.9828948974609375
x << 2
print(x)      # -44.3931579589843750
x / 0.2
print(x)      # -224.0000000000000000
x / -21.2
print(x)      # 10.0000000000000000
Float(x) * 4  # by value
print(x)      # 10.0000000000000000
```

### DivFloat

Subclass of Float for more accurate division calculation