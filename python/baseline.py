import time

import numpy as np

def laplacian(X):
    return(
        np.roll(X, 1, axis=0)
        + np.roll(X, -1, axis=0)
        + np.roll(X, 1, axis=1)
        + np.roll(X, -1, axis=1)
        - 4.0 * X
    )

def simulate(N, steps, F, k):
    Du=0.16
    Dv=0.08
    dt=1.0
    seed=0

    U = np.ones((N, N), dtype=np.float64)
    V = np.zeros((N, N), dtype=np.float64)

    r = N // 20
    mid = N // 2
    rng= np.random.default_rng(seed)
    U[mid - r:mid + r, mid - r:mid + r] = 0.50 + 0.02 * rng.standard_normal((2*r, 2*r))
    V[mid - r:mid + r, mid - r:mid + r] = 0.25 + 0.02 * rng.standard_normal((2*r, 2*r))

    for _ in range(steps):
        Lu = laplacian(U)
        Lv = laplacian(V)
        reaction = U * V * V
        U += dt * (Du * Lu - reaction + F * (1.0 - U))
        V += dt * (Dv * Lv + reaction - (F + k) * V)

    return V

def benchmark(N=256, steps=5000, F=0.060, k=0.062, repeats=3):
    simulate(N, steps, F, k) # discard warm-up round

    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        simulate(N, steps, F, k)
        times.append(time.perf_counter() - t0)

    best = min(times)
    print(f"NumPy simulate(N={N}, steps={steps}): best of {repeats} = {best:.3f}s "
          f"(all: {[f'{t:.3f}' for t in times]})")

    return best

if __name__== "__main__":
    print("Benchmarking...")
    benchmark()