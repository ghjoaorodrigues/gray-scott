import csv
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from gray_scott import simulate

N, STEPS = 256, 5000
F_VALUES = np.linspace(0.030, 0.062, 4)
K_VALUES = np.linspace(0.055, 0.065, 4)

OUTDIR = Path(__file__).resolve().parent.parent.parent / "output" / "python"
OUTDIR.mkdir(parents=True, exist_ok=True)


def main():
    with open(OUTDIR / "manifest.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "F", "k", "filename"])

        idx = 0
        for F in F_VALUES:
            for k in K_VALUES:
                idx += 1
                Fr, kr = round(float(F), 3), round(float(k), 3)
                print(f"[{idx}/16] F={Fr}, k={kr} ... ", end="", flush=True)

                t0 = time.perf_counter()
                V = simulate(N, STEPS, Fr, kr)
                elapsed = time.perf_counter() - t0

                fname = f"V_F{Fr}_k{kr}.bin"
                # order='F' matches Julia's column-major write(io, V),
                # so util/plot.py can read either source the same way
                V.flatten(order="F").tofile(OUTDIR / fname)

                print(f"done in {elapsed:.2f}s -> {fname}")
                writer.writerow([idx, Fr, kr, fname])

    print(f"\nWrote 16 V-grids + manifest.csv to {OUTDIR}")


if __name__ == "__main__":
    main()