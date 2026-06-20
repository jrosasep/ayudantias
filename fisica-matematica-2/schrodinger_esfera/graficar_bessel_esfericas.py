"""
Graficos vectoriales de funciones esfericas de Bessel ordinarias y modificadas.

Genera:
- bessel_esfericas_ordinarias.svg 
- bessel_esfericas_modificadas.svg 

Requiere scipy, numpy y matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import spherical_jn, spherical_yn, spherical_in, spherical_kn


# Dominio adimensional x = sqrt(|gamma|) r.
# Se comienza muy cerca de cero, pero no exactamente en cero,
# porque y_l(x) y k_l(x) divergen en x=0.
x_ordinary = np.linspace(1.0e-3, 25.0, 4000)
x_modified = np.linspace(1.0e-3, 8.0, 4000)
orders = range(0, 6)  # l = 0, 1, ..., 5

# Estilo general sobrio para insertar en apuntes.
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 12,
    "legend.fontsize": 8,
    "figure.dpi": 180,
    "savefig.bbox": "tight",
})


def plot_ordinary():
    fig, ax = plt.subplots(figsize=(8.0, 4.8))

    for ell in orders:
        ax.plot(x_ordinary, spherical_jn(ell, x_ordinary), linewidth=1.4,
                label=rf"$j_{ell}(x)$")

    for ell in orders:
        ax.plot(x_ordinary, spherical_yn(ell, x_ordinary), linestyle="--",
                linewidth=1.2, label=rf"$y_{ell}(x)$")

    ax.axhline(0.0, linewidth=0.8)
    ax.set_xlim(0.0, 25.0)
    ax.set_ylim(-1.6, 1.6)
    ax.set_xlabel(r"$x=\sqrt{\gamma}\,r$")
    ax.set_ylabel(r"valor de la función")
    ax.set_title(r"Funciones esféricas de Bessel ordinarias")
    ax.grid(True, alpha=0.25)
    ax.legend(ncol=4, frameon=True)

    fig.savefig("/mnt/data/bessel_esfericas_ordinarias.svg")
    plt.close(fig)


def plot_modified():
    fig, ax = plt.subplots(figsize=(8.0, 4.8))

    for ell in orders:
        ax.plot(x_modified, spherical_in(ell, x_modified), linewidth=1.4,
                label=rf"$i_{ell}(x)$")

    for ell in orders:
        ax.plot(x_modified, spherical_kn(ell, x_modified), linestyle="--",
                linewidth=1.2, label=rf"$k_{ell}(x)$")

    ax.axhline(0.0, linewidth=0.8)
    ax.set_xlim(0.0, 8.0)
    # La escala vertical se recorta para que el comportamiento cerca de cero sea visible.
    # Las k_l divergen en x=0 y las i_l crecen exponencialmente.
    ax.set_ylim(-0.2, 6.0)
    ax.set_xlabel(r"$x=\sqrt{-\gamma}\,r$")
    ax.set_ylabel(r"valor de la función")
    ax.set_title(r"Funciones esféricas de Bessel modificadas")
    ax.grid(True, alpha=0.25)
    ax.legend(ncol=4, frameon=True)

    fig.savefig("/mnt/data/bessel_esfericas_modificadas.svg")
    plt.close(fig)


if __name__ == "__main__":
    plot_ordinary()
    plot_modified()
