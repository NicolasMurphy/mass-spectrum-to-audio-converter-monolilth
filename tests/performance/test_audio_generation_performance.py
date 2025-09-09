import time
from audio import generate_combined_wav_bytes_and_data
from db import get_massbank_peaks


# audio generation 9 peaks
def test_caffeine_performance():
    spectrum, _, _ = get_massbank_peaks("caffeine")

    start_time = time.perf_counter()
    _, transformation_data = generate_combined_wav_bytes_and_data(
        spectrum, algorithm="linear"
    )
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print("caffeine: ", execution_time)

    assert execution_time < 0.2
    assert len(transformation_data) == len(spectrum)


# 88 peaks
def test_ajmalin_performance():
    spectrum, _, _ = get_massbank_peaks("Ajmalin")

    start_time = time.perf_counter()
    _, transformation_data = generate_combined_wav_bytes_and_data(
        spectrum, algorithm="linear"
    )
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print("Ajmalin: ", execution_time)

    assert execution_time < 0.5
    assert len(transformation_data) == len(spectrum)


# 1933 peaks
def test_cyclopyrroxanthin_performance():
    spectrum, _, _ = get_massbank_peaks("Cyclopyrroxanthin")

    start_time = time.perf_counter()
    _, transformation_data = generate_combined_wav_bytes_and_data(
        spectrum, algorithm="linear"
    )
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print("Cyclopyrroxanthin: ", execution_time)

    assert execution_time < 9
    assert len(transformation_data) == len(spectrum)
