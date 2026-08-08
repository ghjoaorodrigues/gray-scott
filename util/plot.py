import csv
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output" / "julia"
MANIFEST = OUTPUT_DIR / "manifest.csv"


def load_manifest(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def load_grid(path):
    data = np.fromfile(path, dtype=np.float64)
    N = int(math.isqrt(data.size))
    if N * N != data.size:
        raise ValueError(f"{path}: {data.size} values isn't a perfect square")
    return data.reshape(N, N, order="F")


def plot_grid(rows, out_path):
    n = len(rows)
    cols = int(math.ceil(math.sqrt(n)))
    grid_rows = int(math.ceil(n / cols))

    fig, axes = plt.subplots(grid_rows, cols, figsize=(3 * cols, 3 * grid_rows))
    axes = np.array(axes).reshape(-1)

    for ax, row in zip(axes, rows):
        V = load_grid(OUTPUT_DIR / row["filename"])
        ax.imshow(V, cmap="viridis")
        ax.set_title(f"F={row['F']}, k={row['k']}", fontsize=9)
        ax.axis("off")

    for ax in axes[n:]:
        ax.axis("off")

    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    rows = load_manifest(MANIFEST)
    plot_grid(rows, OUTPUT_DIR / "patterns.png")
