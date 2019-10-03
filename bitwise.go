package main

import (
	"fmt"
	"math"
)

func abs(a int) int { // not real abs
	y := a >> 63
	return Sub((a ^ y), y)
}

// Add - simple bitwise add (+)
func Add(a, b int) int {
	if abs(a) == abs(b) && a != b {
		return 0
	}
	a, b = a^b, a&b
	for b != 0 {
		b <<= 1
		a, b = a^b, a&b
	}
	return a
}

// Sub - simple bitwise sub (-)
func Sub(a, b int) int {
	subzero := a >= 0 && b < 0
	if subzero {
		a, b = b, a
	}
	a, b = a^b, ^a&b
	for b > 0 {
		b <<= 1
		a, b = a^b, ^a&b
	}
	if subzero {
		return Add(^a, 1)
	}
	return a
}

// Negative - return negative int
func Negative(a int) int {
	return Sub(0, a)
}

// Mul - simple bitwise mul (*)
func Mul(a, b int) int {
	subzero := false
	if a < 0 && b < 0 {
		a, b = abs(a), abs(b)
	} else if b < 0 {
		b = abs(b)
		subzero = true
	} else if a < 0 {
		a = abs(a)
		subzero = true
	}

	result := 0
	for b != 0 {
		if b&1 == 1 {
			result = Add(result, a)
		}
		a <<= 1
		b >>= 1
	}
	if subzero {
		return Add(^result, 1)
	}
	return result
}

// Div - simple bitwise sub (//)
func Div(a, b int) int {
	//_a, _b := a, b
	if b == 0 {
		panic("integer divide by zero")
	}
	if a == 0 {
		return 0
	}

	subzero := false
	if a < 0 && b < 0 {
		a, b = abs(a), abs(b)
	} else if b < 0 {
		b = abs(b)
		subzero = true
	} else if a < 0 {
		a = abs(a)
		subzero = true
	}

	result := 0
	aBits := 0
	aSaved := a
	for aSaved > 0 {
		aBits = Add(aBits, 1)
		aSaved = aSaved >> 1
	}
	b = b << uint(aBits)
	for aBits > 0 {
		a = Sub(Mul(2, a), b)
		if a >= 0 {
			result = (result | 1) << 1
		} else {
			result <<= 1
			a = Add(a, b)
		}
		aBits = Sub(aBits, 1)
	}

	result >>= 1

	if subzero {
		return Add(^result, 1)
	}

	return result
}

// Mod - simple bitwise mod (%)
func Mod(a, b int) int {
	return Sub(a, Mul(Div(a, b), b))
}

// Pow - simple bitwise pow (**)
func Pow(a, b int) int {
	if b == 0 {
		return 1
	}
	if a == 1 {
		return 1
	} else if a == Negative(1) && b&1 != 0 {
		return Negative(1)
	} else if a == Negative(1) && b&1 == 0 {
		return 1
	}
	if a == 0 && b < 0 {
		panic("construction of zero to a negative power")
	}
	if b < 0 {
		return 0
	}
	result := 1
	for b > 0 {
		result = Mul(result, a)
		b = Sub(b, 1)
	}
	return result
}

// Nod - simple bitwise Gcd
func Nod(a, b int) int {
	if abs(a) == abs(b) {
		return abs(a)
	} else if a == 0 {
		return abs(b)
	} else if b == 0 {
		return abs(a)
	} else if abs(a) == 1 || abs(b) == 1 {
		return 1
	}

	a, b = abs(a), abs(b)

	if a&1 == 0 && b&1 == 0 {
		return Mul(2, Nod(Div(a, 2), Div(b, 2)))
	} else if a&1 == 0 && b&1 != 0 {
		return Nod(Div(a, 2), b)
	} else if a&1 != 0 && b&1 == 0 {
		return Nod(a, Div(b, 2))
	} else if a&1 != 0 && b&1 != 0 && b > a {
		return Nod(Div(Sub(b, a), 2), a)
	} else if a&1 != 0 && b&1 != 0 && a > b {
		return Nod(Div(Sub(a, b), 2), b)
	}
	return 0 // mock ret value
}

func gcd(a, b int) int {
	a, b = abs(a), abs(b)
	for b > 0 {
		a, b = b, a%b
	}
	return a
}

func all(a []bool) bool {
	for _, i := range a {
		if i != true {
			return false
		}
	}
	return true
}

func main() {
	// test all func
	var resultsAdd []bool
	var resultsSub []bool
	var resultsNeg []bool
	var resultsMul []bool
	var resultsDiv []bool
	var resultsMod []bool
	var resultsPow []bool
	var resultsGcd []bool

	for i := -10; i < 10; i++ {
		resultsNeg = append(resultsNeg, -i == Negative(i))

		for j := -10; j < 10; j++ {
			resultsAdd = append(resultsAdd, i+j == Add(i, j))
			resultsSub = append(resultsSub, i-j == Sub(i, j))
			resultsMul = append(resultsMul, i*j == Mul(i, j))
			if !(i == 0 && j < 0) { // 0**(-x)
				res := int(math.Pow(float64(i), float64(j))) == Pow(i, j)
				resultsPow = append(resultsPow, res)
			}
			if !(j == 0) { // x/0
				resultsDiv = append(resultsDiv, i/j == Div(i, j))
				resultsMod = append(resultsMod, i%j == Mod(i, j))
			}
			resultsGcd = append(resultsGcd, gcd(i, j) == Nod(i, j))
		}
	}
	fmt.Printf("All tests passed successfully: %t\n", all([]bool{
		all(resultsAdd), all(resultsSub), all(resultsNeg),
		all(resultsMul), all(resultsDiv), all(resultsGcd),
		all(resultsMod), all(resultsPow),
	}))
}
