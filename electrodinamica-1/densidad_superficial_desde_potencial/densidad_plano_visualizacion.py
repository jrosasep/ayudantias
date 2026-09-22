"""Gráficos numéricos del plano cargado, generados con Matplotlib.

Ejecutar: python densidad_plano_visualizacion.py
Produce un SVG vectorial. Se excluye el disco singular rho/L < 0.6.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize


OUTPUT = Path(__file__).with_name("densidad_plano_visualizacion.svg")
CUT = 0.6


def density(rho):
    with np.errstate(divide="ignore"):
        return -0.5 / np.asarray(rho)**3


def field(x, y, z):
    r2 = x*x + y*y + z*z
    with np.errstate(divide="ignore", invalid="ignore"):
        factor = np.where(z > 0, 1.0, 0.5)
        r5 = r2**2.5
        return (factor*3*x*z/r5, factor*3*y*z/r5,
                factor*(3*z*z-r2)/r5)


def verify():
    rho = np.array([0.6, 0.8, 1.0, 1.5, 2.3])
    h = 1e-6*rho
    ep = field(rho, 0.0, h)
    em = field(rho, 0.0, -h)
    np.testing.assert_allclose(ep[2], -1/rho**3, rtol=1e-9)
    np.testing.assert_allclose(em[2], -0.5/rho**3, rtol=1e-9)
    np.testing.assert_allclose(ep[2]-em[2], density(rho), rtol=1e-9)
    np.testing.assert_allclose(ep[0], -em[0]*2, rtol=1e-9)
    assert max(np.max(abs(ep[0])), np.max(abs(em[0]))) < 2e-5


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

    # (a) Perfil radial. La singularidad queda fuera del intervalo.
    rho = np.linspace(CUT, 2.4, 600)
    ax = axes[0, 0]
    ax.plot(rho, density(rho), lw=2.2, color="#1f5a94")
    ax.axvline(1, color="0.4", lw=0.8, ls="--")
    ax.scatter([1], [-0.5], color="#1f5a94", s=18, zorder=3)
    ax.set(xlim=(CUT, 2.4), ylim=(-2.5, 0.08),
           xlabel=r"$\rho/L$", ylabel=r"$\widetilde\sigma$")
    ax.set_title(r"(a) Densidad superficial $\widetilde\sigma=-1/(2\widetilde\rho^3)$")
    ax.grid(alpha=0.24)

    # (b) Mapa en el plano z=0 con la misma densidad.
    ax = axes[0, 1]
    grid = np.linspace(-2.4, 2.4, 281)
    xx, yy = np.meshgrid(grid, grid)
    rr = np.hypot(xx, yy)
    smap = np.ma.masked_where(rr < CUT, density(rr))
    mesh = ax.pcolormesh(xx, yy, smap, cmap="viridis",
                         norm=Normalize(-2.4, 0.0), shading="auto")
    ax.add_patch(plt.Circle((0, 0), CUT, facecolor="white",
                            edgecolor="0.3", lw=1))
    ax.text(0, 0, "origen\nexcluido", ha="center", va="center", fontsize=8)
    ax.set(xlim=(-2.4, 2.4), ylim=(-2.4, 2.4), aspect="equal",
           xlabel=r"$x/L$", ylabel=r"$y/L$")
    ax.set_title(r"(b) Mapa de $\widetilde\sigma$ en $z=0$")
    fig.colorbar(mesh, ax=ax, fraction=0.046, pad=0.03,
                 label=r"$\widetilde\sigma$")

    # (c) Flechas de dirección del campo en el corte y=0.
    ax = axes[1, 0]
    q = np.linspace(-2.0, 2.0, 17)
    xq, zq = np.meshgrid(q, q)
    ex, _, ez = field(xq, 0.0, zq)
    mag = np.hypot(ex, ez)
    valid = (zq != 0) & (np.hypot(xq, zq) >= CUT)
    ux = np.ma.masked_where(~valid, ex/np.where(mag == 0, 1, mag))
    uz = np.ma.masked_where(~valid, ez/np.where(mag == 0, 1, mag))
    upper = np.ma.masked_where(zq <= 0, ux)
    lower = np.ma.masked_where(zq >= 0, ux)
    ax.quiver(xq, zq, upper, np.ma.masked_where(zq <= 0, uz),
              color="#1f5a94", angles="xy", scale_units="xy", scale=5.3,
              width=0.0039, headwidth=3.7)
    ax.quiver(xq, zq, lower, np.ma.masked_where(zq >= 0, uz),
              color="#168c84", angles="xy", scale_units="xy", scale=5.3,
              width=0.0039, headwidth=3.7)
    ax.axhline(0, color="#b4442d", lw=1.3)
    ax.add_patch(plt.Circle((0, 0), CUT, facecolor="white",
                            edgecolor="0.4", lw=1))
    ax.set(xlim=(-2.2, 2.2), ylim=(-2.2, 2.2), aspect="equal",
           xlabel=r"$x/L$", ylabel=r"$z/L$")
    ax.set_title(r"(c) Campo eléctrico en el corte $y=0$")
    ax.grid(alpha=0.16)
    ax.text(-2.13, 2.0, r"$z>0$", color="#1f5a94", fontsize=9)
    ax.text(-2.13, -2.08, r"$z<0$", color="#168c84", fontsize=9)

    # (d) Los límites normales difieren exactamente en sigma/epsilon0.
    ax = axes[1, 1]
    ax.plot(rho, -1/rho**3, lw=2.2, color="#1f5a94",
            label=r"$\widetilde E_z^+=-1/\widetilde\rho^3$")
    ax.plot(rho, -0.5/rho**3, lw=2.2, color="#168c84",
            label=r"$\widetilde E_z^-=-1/(2\widetilde\rho^3)$")
    ax.set(xlim=(CUT, 2.4), ylim=(-5.0, 0.1),
           xlabel=r"$\rho/L$", ylabel=r"$\widetilde E_z$")
    ax.set_title("(d) Salto del campo normal")
    ax.grid(alpha=0.24)
    ax.legend(loc="lower right", fontsize=8, frameon=False)

    fig.savefig(OUTPUT, bbox_inches="tight")
    plt.close(fig)
    print(f"Figura guardada en: {OUTPUT}")


if __name__ == "__main__":
    main()
