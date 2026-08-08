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
