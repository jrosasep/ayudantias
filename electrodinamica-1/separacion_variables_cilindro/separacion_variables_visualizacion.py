"""Visualización del modo cilíndrico m=2 con Matplotlib y NumPy.

Ejecutar: python separacion_variables_visualizacion.py
Guarda el gráfico en SVG vectorial.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm


OUTPUT = Path(__file__).with_name("separacion_variables_visualizacion.svg")


def solution(x, y):
    """Devuelve V/V0 y las componentes ER/V0 para R=V0=1."""
    r = np.hypot(x, y)
    phi = np.arctan2(y, x)
    inside = r <= 1
    safe = np.where(r == 0, 1.0, r)
    s, c = np.sin(2*phi), np.cos(2*phi)
    v = np.where(inside, r**2*s, s/safe**2)
    er = np.where(inside, -2*r*s, 2*s/safe**3)
    ephi = np.where(inside, -2*r*c, -2*c/safe**3)
    ex = er*np.cos(phi)-ephi*np.sin(phi)
    ey = er*np.sin(phi)+ephi*np.cos(phi)
    return v, ex, ey


def verify():
    phi = np.linspace(0, 2*np.pi, 300, endpoint=False)
    rin = 1-1e-7
    rout = 1+1e-7
    vin, _, _ = solution(rin*np.cos(phi), rin*np.sin(phi))
    vout, _, _ = solution(rout*np.cos(phi), rout*np.sin(phi))
    np.testing.assert_allclose(vin, np.sin(2*phi), atol=2.1e-7)
    np.testing.assert_allclose(vout, np.sin(2*phi), atol=2.1e-7)
    np.testing.assert_allclose(vin, vout, atol=4.1e-7)


def main():
    verify()
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "stix",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "figure.dpi": 160,
        "svg.fonttype": "path",
    })
    fig, axes = plt.subplots(2, 2, figsize=(10.2, 7.4),
                             constrained_layout=True)
    grid = np.linspace(-2.05, 2.05, 201)
    xx, yy = np.meshgrid(grid, grid)
    vv, _, _ = solution(xx, yy)

    ax = axes[0, 0]
    norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
    image = ax.pcolormesh(xx, yy, vv, cmap="RdBu_r", norm=norm,
                          shading="auto")
    ax.add_patch(plt.Circle((0, 0), 1, fill=False, color="black", lw=1.4))
    ax.set(xlim=(-2.05, 2.05), ylim=(-2.05, 2.05), aspect="equal",
           xlabel=r"$x/R$", ylabel=r"$y/R$")
    ax.set_title(r"(a) Potencial $V/V_0$")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.03, label=r"$V/V_0$")

    ax = axes[0, 1]
    q = np.linspace(-1.95, 1.95, 19)
    xq, yq = np.meshgrid(q, q)
    _, ex, ey = solution(xq, yq)
    mag = np.hypot(ex, ey)
    direction_x = ex/np.where(mag == 0, 1, mag)
    direction_y = ey/np.where(mag == 0, 1, mag)
    image = ax.pcolormesh(xx, yy, np.hypot(*solution(xx, yy)[1:]),
                          cmap="viridis", vmin=0, vmax=2.2,
                          shading="auto")
    ax.quiver(xq, yq, direction_x, direction_y, color="0.12",
              angles="xy", scale_units="xy", scale=5.7, width=0.0037,
              headwidth=3.6)
    ax.add_patch(plt.Circle((0, 0), 1, fill=False, color="white", lw=1.5))
    ax.set(xlim=(-2.05, 2.05), ylim=(-2.05, 2.05), aspect="equal",
           xlabel=r"$x/R$", ylabel=r"$y/R$")
    ax.set_title(r"(b) Campo $|\mathbf{E}|R/V_0$ y dirección")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.03,
                 label=r"$|\mathbf{E}|R/V_0$")

    phi = np.linspace(0, 2*np.pi, 600)
    ax = axes[1, 0]
    ax.plot(np.degrees(phi), np.sin(2*phi), color="#1f5a94", lw=2.2)
    ax.axhline(0, color="0.4", lw=0.8)
    ax.set(xlim=(0, 360), ylim=(-1.1, 1.1),
           xticks=[0, 90, 180, 270, 360],
           xlabel=r"$\phi$ (grados)", ylabel=r"$V(R,\phi)/V_0$")
    ax.set_title("(c) Condición de borde")
    ax.grid(alpha=0.24)

    ax = axes[1, 1]
    ax.plot(np.degrees(phi), np.sin(2*phi), color="#b4442d", lw=2.2)
    ax.axhline(0, color="0.4", lw=0.8)
    ax.set(xlim=(0, 360), ylim=(-1.1, 1.1),
           xticks=[0, 90, 180, 270, 360],
           xlabel=r"$\phi$ (grados)",
           ylabel=r"$\sigma R/(4\varepsilon_0 V_0)$")
    ax.set_title("(d) Densidad superficial")
    ax.grid(alpha=0.24)

    fig.savefig(OUTPUT, bbox_inches="tight")
    plt.close(fig)
    print(f"Figura guardada en: {OUTPUT}")


if __name__ == "__main__":
    main()
