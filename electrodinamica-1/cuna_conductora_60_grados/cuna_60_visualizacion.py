"""Visualización de la cuña conductora de 60 grados con Matplotlib.

Ejecutar: python cuna_60_visualizacion.py
Produce un SVG vectorial. Unidades: d=q=4*pi*epsilon0=1.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize


OUTPUT = Path(__file__).with_name("cuna_60_visualizacion.svg")
ALPHA = np.pi/3
PHI0 = np.pi/6
PLUS = PHI0 + 2*np.arange(3)*ALPHA
MINUS = -PHI0 + 2*np.arange(3)*ALPHA


def potential(s, phi, z):
    """4*pi*epsilon0*d*V/q dentro de la cuña para d=1."""
    value = np.zeros(np.broadcast_shapes(np.shape(s), np.shape(phi),
                                         np.shape(z)), dtype=float)
    for angle in PLUS:
        r = np.sqrt(s*s+1-2*s*np.cos(phi-angle)+z*z)
        value += 1/r
    for angle in MINUS:
        r = np.sqrt(s*s+1-2*s*np.cos(phi-angle)+z*z)
        value -= 1/r
    return value


def sigma(s, z):
    """4*pi*d**2*sigma/q, idéntica sobre ambos semiplanos."""
    c = s*s+1+z*z
    a = c-np.sqrt(3)*s
    b = c+np.sqrt(3)*s
    return -(a**-1.5+b**-1.5-2*c**-1.5)


def verify():
    s = np.array([0.2, 0.5, 1.0, 1.8, 3.0])
    z = np.array([-1.2, -0.5, 0.0, 0.5, 1.2])
    np.testing.assert_allclose(potential(s, 0.0, z), 0, atol=1e-12)
    np.testing.assert_allclose(potential(s, ALPHA, z), 0, atol=1e-12)
    h = 1e-5
    lower = -(potential(s, h, z)-potential(s, 0.0, z))/(s*h)
    upper = (potential(s, ALPHA, z)-potential(s, ALPHA-h, z))/(s*h)
    np.testing.assert_allclose(lower, sigma(s, z), rtol=5e-5, atol=1e-6)
    np.testing.assert_allclose(upper, sigma(s, z), rtol=5e-5, atol=1e-6)
    assert np.all(sigma(s, z) < 0)
    np.testing.assert_allclose(sigma(0.0, z), 0, atol=1e-14)


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

    # (a) Posición real e imágenes, con la cuña física sombreada.
    ax = axes[0, 0]
    ax.fill([0, 1.4, 0.7], [0, 0, 1.4*np.sin(ALPHA)],
            color="#e8f2f8", zorder=0)
    ax.add_patch(plt.Circle((0, 0), 1, fill=False, ls="--",
                            color="0.65", lw=1))
    for ang in PLUS:
        x, y = np.cos(ang), np.sin(ang)
        ax.scatter(x, y, c="#b4442d", s=70, zorder=3)
        ax.text(1.16*x, 1.16*y, r"$+q$", color="#b4442d",
                ha="center", va="center", fontsize=9)
    for ang in MINUS:
        x, y = np.cos(ang), np.sin(ang)
        ax.scatter(x, y, c="#1f5a94", s=70, zorder=3)
        ax.text(1.16*x, 1.16*y, r"$-q$", color="#1f5a94",
                ha="center", va="center", fontsize=9)
    ax.plot([0, 1.37], [0, 0], color="black", lw=1.3)
    ax.plot([0, 1.37*np.cos(ALPHA)], [0, 1.37*np.sin(ALPHA)],
            color="black", lw=1.3)
    ax.text(0.60, 0.73, "real", color="#b4442d", fontsize=9)
    ax.set(xlim=(-1.4, 1.4), ylim=(-1.4, 1.4), aspect="equal",
           xlabel=r"$x/d$", ylabel=r"$y/d$")
    ax.set_title("(a) Carga real y cinco imágenes")
    ax.grid(alpha=0.14)

    # (b) Potencial dentro de la cuña; se excluye el polo real.
    ax = axes[0, 1]
    x = np.linspace(0, 2.7, 221)
    y = np.linspace(0, 2.4, 201)
    xx, yy = np.meshgrid(x, y)
    ss, phi = np.hypot(xx, yy), np.arctan2(yy, xx)
    dist = np.hypot(xx-np.cos(PHI0), yy-np.sin(PHI0))
    valid = (phi <= ALPHA) & (ss <= 2.7) & (dist >= 0.12)
    v = np.ma.masked_where(~valid, potential(ss, phi, 0.0))
    image = ax.pcolormesh(xx, yy, v, cmap="viridis",
                          norm=Normalize(0, 2.5), shading="auto")
    ax.plot([0, 2.7], [0, 0], color="black", lw=1.2)
    ax.plot([0, 2.7*np.cos(ALPHA)], [0, 2.7*np.sin(ALPHA)],
            color="black", lw=1.2)
    ax.scatter([np.cos(PHI0)], [np.sin(PHI0)], color="#b4442d",
               s=18, zorder=3)
    ax.set(xlim=(0, 2.7), ylim=(0, 2.4), aspect="equal",
           xlabel=r"$x/d$", ylabel=r"$y/d$")
    ax.set_title(r"(b) Potencial $4\pi\varepsilon_0 dV/q$")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.03,
                 label=r"$4\pi\varepsilon_0 dV/q$")

    # (c) El perfil sobre las dos caras coincide por simetría.
    ax = axes[1, 0]
    s = np.linspace(0, 4, 600)
    profile = sigma(s, 0.0)
    ax.plot(s, profile, color="#1f5a94", lw=2.2,
            label=r"$\phi=0$")
    ax.plot(s[::18], profile[::18], linestyle="none", marker="o",
            ms=2.8, color="#b4442d", label=r"$\phi=\pi/3$")
    ax.axhline(0, color="0.4", lw=0.8)
    ax.set(xlim=(0, 4), xlabel=r"$s/d$",
           ylabel=r"$4\pi d^2\sigma/q$")
    ax.set_title(r"(c) Densidad inducida en $z=0$")
    ax.grid(alpha=0.24)
    ax.legend(loc="lower right", fontsize=8, frameon=False)

    # (d) Distribución sobre una cara: s>=0 y coordenada axial z.
    ax = axes[1, 1]
    sg = np.linspace(0, 3.5, 241)
    zg = np.linspace(-2, 2, 241)
    sgrid, zgrid = np.meshgrid(sg, zg)
    smap = sigma(sgrid, zgrid)
    image = ax.pcolormesh(sgrid, zgrid, smap, cmap="viridis",
                          norm=Normalize(vmin=-7.0, vmax=0),
                          shading="auto")
    ax.set(xlim=(0, 3.5), ylim=(-2, 2), aspect="auto",
           xlabel=r"$s/d$", ylabel=r"$z/d$")
    ax.set_title(r"(d) Densidad sobre una cara")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.03,
                 label=r"$4\pi d^2\sigma/q$")

    fig.savefig(OUTPUT, bbox_inches="tight")
    plt.close(fig)
    print(f"Figura guardada en: {OUTPUT}")


if __name__ == "__main__":
    main()
