def mz_to_frequency_linear(mz, offset: float = 300):
    return mz + offset


def mz_to_frequency_inverse(mz, scale: float = 100000, shift: float = 1):
    return scale / (mz + shift)


def mz_to_frequency_modulo(
    mz, factor: float = 10, modulus: float = 500, base: float = 100
):
    return ((mz * factor) % modulus) + base
