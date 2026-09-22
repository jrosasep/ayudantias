"""Visualización adimensional del cilindro hueco infinito.

La figura usa a=L, b=2L y rho0>0. Se guarda como SVG vectorial en el mismo
directorio que este script para incorporarla directamente en la guía LaTeX.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize


OUTPUT = Path(__file__).with_name("cilindro_hueco_visualizacion.svg")
A = 1.0
B = 2.0
R_MAX = 4.0


def density_tilde(radius: np.ndarray) -> np.ndarray:
    """Devuelve rho L/rho0 para a=L y b=2L."""
    radius = np.asarray(radius, dtype=float)
    result = np.zeros_like(radius)
    shell = (radius > A) & (radius < B)
    result[shell] = 1.0 / radius[shell]
    return result


def field_tilde(radius: np.ndarray) -> np.ndarray:
    """Devuelve epsilon0 E/rho0."""
    radius = np.asarray(radius, dtype=float)
    result = np.zeros_like(radius)
    shell = (radius >= A) & (radius <= B)
    exterior = radius > B
    result[shell] = 1.0 - A / radius[shell]
    result[exterior] = (B - A) / radius[exterior]
    return result


def potential_tilde(radius: np.ndarray) -> np.ndarray:
    """Devuelve epsilon0 phi/(rho0 L), con phi(b)=0."""
    radius = np.asarray(radius, dtype=float)
    result = np.empty_like(radius)
    cavity = radius <= A
    shell = (radius > A) & (radius <= B)
    exterior = radius > B
    result[cavity] = (B - A) + A * np.log(A / B)
    result[shell] = (B - radius[shell]) + A * np.log(radius[shell] / B)
    result[exterior] = -(B - A) * np.log(radius[exterior] / B)
    return result


def mark_regions(axis: plt.Axes) -> None:
    """Marca la cavidad y el cascarón en un perfil radial."""
    axis.axvspan(0.0, A, color="0.94", zorder=0)
    axis.axvspan(A, B, facecolor="#dbe9f6", alpha=0.65, hatch="///", zorder=0)
    axis.axvline(A, color="0.25", linestyle="--", linewidth=0.9)
    axis.axvline(B, color="0.25", linestyle="--", linewidth=0.9)
    y0, y1 = axis.get_ylim()
    axis.text(A, y1, r"$a/L=1$", ha="right", va="top", fontsize=8)
    axis.text(B, y1, r"$b/L=2$", ha="left", va="top", fontsize=8)
    axis.set_ylim(y0, y1)


def main() -> None:
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "mathtext.fontset": "stix",
            "font.family": "serif",
            "figure.dpi": 160,
        }
    )

    radius = np.linspace(0.0, R_MAX, 1000)
    figure, axes = plt.subplots(2, 2, figsize=(10.2, 7.4), constrained_layout=True)

    # (a) Densidad: se separan los intervalos para no dibujar saltos espurios.
    axis = axes[0, 0]
    left = radius < A
    shell = (radius > A) & (radius < B)
    right = radius > B
    axis.plot(radius[left], np.zeros(np.count_nonzero(left)), color="#1f5a94", lw=2.1)
    axis.plot(radius[shell], 1.0 / radius[shell], color="#1f5a94", lw=2.1)
    axis.plot(radius[right], np.zeros(np.count_nonzero(right)), color="#1f5a94", lw=2.1)
    axis.set(xlim=(0, R_MAX), ylim=(-0.05, 1.08), xlabel=r"$r/L$", ylabel=r"$\widetilde\rho$")
    axis.set_title(r"(a) Densidad volumétrica $\widetilde\rho=\rho L/\rho_0$")
    axis.grid(alpha=0.24)
    mark_regions(axis)

    # (b) Campo eléctrico radial.
    axis = axes[0, 1]
    axis.plot(radius, field_tilde(radius), color="#b4442d", lw=2.2)
    axis.set(xlim=(0, R_MAX), ylim=(-0.03, 0.56), xlabel=r"$r/L$", ylabel=r"$\widetilde E$")
    axis.set_title(r"(b) Campo radial $\widetilde E=\varepsilon_0E/\rho_0$")
    axis.grid(alpha=0.24)
    mark_regions(axis)

    # (c) Potencial con referencia en r=b.
    axis = axes[1, 0]
    axis.plot(radius, potential_tilde(radius), color="#2e7d52", lw=2.2)
    axis.axhline(0.0, color="0.35", linewidth=0.8)
    axis.set(xlim=(0, R_MAX), xlabel=r"$r/L$", ylabel=r"$\widetilde\phi$")
    axis.set_title(r"(c) Potencial $\widetilde\phi=\varepsilon_0\phi/(\rho_0L)$")
    axis.grid(alpha=0.24)
    mark_regions(axis)

    # (d) Corte transversal. El color representa rho y las flechas representan E.
    axis = axes[1, 1]
    grid = np.linspace(-3.15, 3.15, 321)
    xx, yy = np.meshgrid(grid, grid)
    rr = np.hypot(xx, yy)
    rho_map = np.ma.masked_where((rr <= A) | (rr >= B), density_tilde(rr))
    norm = Normalize(vmin=1.0 / B, vmax=1.0 / A)
    mesh = axis.pcolormesh(xx, yy, rho_map, cmap="viridis", norm=norm, shading="auto")

    qgrid = np.linspace(-3.0, 3.0, 19)
    qx, qy = np.meshgrid(qgrid, qgrid)
    qr = np.hypot(qx, qy)
    qe = field_tilde(qr)
    safe_r = np.where(qr == 0.0, 1.0, qr)
    ex = np.ma.masked_where(qe <= 1.0e-12, qe * qx / safe_r)
    ey = np.ma.masked_where(qe <= 1.0e-12, qe * qy / safe_r)
    axis.quiver(
        qx,
        qy,
        ex,
        ey,
        color="0.12",
        angles="xy",
        scale_units="xy",
        scale=1.7,
        width=0.0042,
        headwidth=3.5,
        headlength=4.7,
    )
    for radius_boundary, style in ((A, "--"), (B, "-")):
        axis.add_patch(
            plt.Circle((0.0, 0.0), radius_boundary, fill=False, color="black", lw=1.2, ls=style)
        )
    axis.text(A / np.sqrt(2), A / np.sqrt(2), r"$a$", fontsize=9, ha="left", va="bottom")
    axis.text(B / np.sqrt(2), B / np.sqrt(2), r"$b$", fontsize=9, ha="left", va="bottom")
    axis.set(
        xlim=(-3.2, 3.2),
        ylim=(-3.2, 3.2),
        aspect="equal",
        xlabel=r"$x/L$",
        ylabel=r"$y/L$",
    )
    axis.set_title("(d) Densidad y campo en el plano transversal")
    colorbar = figure.colorbar(mesh, ax=axis, fraction=0.047, pad=0.035)
    colorbar.set_label(r"$\widetilde\rho$")

    figure.savefig(OUTPUT, bbox_inches="tight")
    print(f"Figura guardada en: {OUTPUT}")


if __name__ == "__main__":
    main()
