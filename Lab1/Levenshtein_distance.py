import time
import functools
#1 naïve recursive implementation of Levenshtein distance
def levenshtein_distance(s1, s2):
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)
    if s1[0] == s2[0]:
        return levenshtein_distance(s1[1:], s2[1:])
    return 1 + min(
        levenshtein_distance(s1[1:], s2),
        levenshtein_distance(s1, s2[1:]),
        levenshtein_distance(s1[1:], s2[1:])
    )
#2 Use of memoization to optimize the recursive implementation
@functools.lru_cache(maxsize=None)
def levenshtein_distance_memo(s1, s2):
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)
    if s1[0] == s2[0]:
        return levenshtein_distance_memo(s1[1:], s2[1:])
    return 1 + min(
        levenshtein_distance_memo(s1[1:], s2),
        levenshtein_distance_memo(s1, s2[1:]),
        levenshtein_distance_memo(s1[1:], s2[1:])
    )
import matplotlib.pyplot as plt

def measure_execution_times(lengths):
    naive_times = []
    memoized_times = []

    for length in lengths:
        s1 = 'a' * length
        s2 = 'b' * length

        start_time = time.perf_counter()
        levenshtein_distance(s1, s2)
        naive_times.append((time.perf_counter() - start_time) * 1000)

        levenshtein_distance_memo.cache_clear()
        start_time = time.perf_counter()
        levenshtein_distance_memo(s1, s2)
        memoized_times.append((time.perf_counter() - start_time) * 1000)

    return naive_times, memoized_times


def plot_computation_times(lengths, naive_times, memoized_times):
    plt.plot(lengths, naive_times, marker='o', label='Naive recursive')
    plt.plot(lengths, memoized_times, marker='o', label='Memoized recursive')
    plt.xlabel('String length')
    plt.ylabel('Execution time (ms)')
    plt.title('Levenshtein Distance: Execution Time vs String Length')
    plt.yscale('log')
    plt.grid(True, which='both', linestyle='--', alpha=0.4)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    string_lengths = range(1, 11)
    naive_times, memoized_times = measure_execution_times(string_lengths)
    plot_computation_times(string_lengths, naive_times, memoized_times)