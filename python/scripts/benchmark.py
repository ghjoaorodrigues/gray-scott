import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from gray_scott import simulate

N, STEPS, F, K, REPEATS = 256, 5000, 0.060, 0.062, 5


def main():
    print(f"Benchmarking simulate(N={N}, steps={STEPS}, F={F}, k={K})...")
    simulate(N, STEPS, F, K)  # discard warm-up

    times = []
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        simulate(N, STEPS, F, K)
        times.append(time.perf_counter() - t0)

    print(f"samples: {[f'{t:.3f}s' for t in times]}")
    print(f"min:    {min(times):.3f}s")
    print(f"median: {sorted(times)[len(times)//2]:.3f}s")


if __name__ == "__main__":
    main()