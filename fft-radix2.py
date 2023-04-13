import cmath as math


def is_power_of_2(num: int) -> bool:
    """
    Checks if the given number is a power of 2. Negative numbers are excluded and return False.
    NOTE: Uses a bit-hacky strategy to save computational resources.
    """
    if num <= 0:
        return False

    return num == num & -num


def next_power_of_2(num: int) -> int:
    """
    Finds closest power of 2 BIGGER THAN OR EQUAL TO the current number.
    """
    return 1 << (num - 1).bit_length()


def twiddle(N: int, k: int) -> complex:
    """
    Calculates twiddle factor of e^(-j*2*pi*k/N).
    """
    return math.exp((-2j * math.pi * k) / N)


def FFT(x: list) -> list:
    """
    Uses the decimation-in-time (DIT) radix-2 FFT algorithm to find the DFT of an input signal x.
    Will pad extra 0's if necessary so that x's length is a power of 2.
    """
    if not is_power_of_2(len(x)):
        desired_len: int = next_power_of_2(len(x))
        x += [0] * (desired_len - len(x))

    fft: list = FFT_helper(x)
    return [round(n.real, 3) + round(n.imag, 3) * 1j for n in fft]


def FFT_helper(x: list) -> list:
    """
    Helper recursive function to FFT. Uses decimation-in-time radix-2 FFT. Expects the length of x to be a power of 2.
    """
    N: int = len(x)

    if N <= 1:
        return x

    a: list = [n for (idx, n) in enumerate(x) if not idx % 2]  # Even indices
    b: list = [n for (idx, n) in enumerate(x) if idx % 2]  # Odd indices
    dft_a: list = FFT_helper(a)
    dft_b: list = FFT_helper(b)

    dft_x = [0] * N
    for k in range(N >> 1):
        twi = twiddle(N, k)
        dft_x[k] = dft_a[k] + twi * dft_b[k]
        dft_x[k + (N >> 1)] = dft_a[k] - twi * dft_b[k]

    return dft_x


def main():
    print("Input a sequence of **real* numbers seperated by commas: ", end="")
    while True:
        try:
            numbers: list = [float(num) for num in input().split(",")]
            break
        except Exception as _:
            print("\nPlease enter a valid list of real numbers: ", end="")

    print("\nComputing the radix-2 FFT of {numbers}.\n")
    print(FFT(numbers))


if __name__ == "__main__":
    main()
