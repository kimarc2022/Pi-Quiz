#!/usr/bin/env python3
"""Generate 1,000,000 digits of pi using Chudnovsky binary splitting (stdlib only).

Pure integer arithmetic throughout — no Decimal, no overflow.
Formula: pi = 426880 * sqrt(10005) * Q / T
We compute floor(pi * 10^D) as a Python int, then convert to string.
"""

from math import isqrt
import time, os, sys

DIGITS = 100_000
GUARD  = 15   # extra digits to absorb rounding; discarded at the end

# 640320^3 / 24 = 10939058860032000
_C3_OVER_24 = 640320 ** 3 // 24


def _split(a, b):
    """Binary-split Chudnovsky series. Returns (P, Q, T) as Python ints."""
    if b - a == 1:
        if a == 0:
            return 1, 1, 13591409
        Pab = (6*a - 5) * (2*a - 1) * (6*a - 1)
        Qab = a**3 * _C3_OVER_24
        Tab = Pab * (13591409 + 545140134 * a)
        if a % 2 == 1:
            Tab = -Tab
        return Pab, Qab, Tab
    m = (a + b) // 2
    Pam, Qam, Tam = _split(a, m)
    Pmb, Qmb, Tmb = _split(m, b)
    return Pam * Pmb, Qam * Qmb, Qmb * Tam + Pam * Tmb


def compute_pi_digits(num_digits):
    """Return pi as a digit string (no decimal point), e.g. '31415926...'."""
    num_terms = int(num_digits / 14.1816) + 20
    _, Q, T = _split(0, num_terms)

    # We want floor(pi * 10^D) where D = num_digits + GUARD.
    # pi = 426880 * sqrt(10005) * Q / T
    # => floor(pi * 10^D)
    #    = floor( 426880 * sqrt(10005 * 10^(2D)) * Q / T )
    #    ≈ 426880 * isqrt(10005 * 10^(2D)) * Q // T
    #
    # Error from isqrt is < 1, so 426880 * (error) * Q/T < pi ≈ 3.14
    # That's <4 units in the last position of pi_int — safely within GUARD digits.
    D = num_digits + GUARD
    sqrt_part = isqrt(10005 * 10 ** (2 * D))
    pi_int    = 426880 * sqrt_part * Q // T

    # pi_int ≈ pi * 10^D, so str(pi_int) starts with "31415926..."
    # Python 3.11+ throttles large int→str; caller must set_int_max_str_digits(0).
    return str(pi_int)[:num_digits]


def main():
    print(f"Generating {DIGITS:,} digits of pi...")
    print("Algorithm: Chudnovsky binary splitting (pure Python int arithmetic)")
    print("Expected time on Raspberry Pi 5: 1-3 minutes")
    sys.stdout.flush()

    t0 = time.time()
    pi_str = compute_pi_digits(DIGITS)
    elapsed = time.time() - t0
    print(f"Computed in {elapsed:.1f}s")

    assert pi_str[:20] == '31415926535897932384', \
        f"Digit mismatch! Got: {pi_str[:20]}"
    assert len(pi_str) == DIGITS, \
        f"Length mismatch: got {len(pi_str)}, expected {DIGITS}"

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pi_digits.js')
    print(f"Writing {out} ...")
    with open(out, 'w') as f:
        f.write(f'const PI_DIGITS = "{pi_str}";\n')

    size = os.path.getsize(out)
    print(f"Done! {size:,} bytes written.")
    print(f"First 30 digits: {pi_str[:30]}")


if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    sys.set_int_max_str_digits(0)  # Python 3.11+: allow arbitrarily large int→str
    main()
