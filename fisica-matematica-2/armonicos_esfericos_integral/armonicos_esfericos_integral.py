#!/usr/bin/env python3
# Figuras para: armonicos esfericos e integral angular.
# Genera solamente archivos SVG en ./figures.
# Las figuras usan mapas 2D sobre la esfera unitaria. La coordenada horizontal
# es varphi y la coordenada vertical es la latitud angular lambda = pi/2-theta.

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import colors

BASE = Path(__file__).resolve().parent
FIGDIR = BASE / "figures"
FIGDIR.mkdir(parents=True, exist_ok=True)
for old in FIGDIR.glob("*.svg"):
    old.unlink()

plt.rcParams.update({
    "font.size": 10,
    "axes.grid": False,
    "figure.constrained_layout.use": True,
})

# Malla angular: longitud phi y latitud lambda = pi/2 - theta.
# Resolucion moderada: el SVG queda ligero porque el campo se guarda como imagen
# raster embebida, y las curvas nodales como trazos vectoriales.
lon = np.linspace(-np.pi, np.pi, 320)
lat = np.linspace(-np.pi/2, np.pi/2, 160)
LON, LAT = np.meshgrid(lon, lat)

X = np.cos(LAT) * np.cos(LON)
Y = np.cos(LAT) * np.sin(LON)
Z = np.sin(LAT)

F = X + Y + 2*Z
F_norm = F / np.max(np.abs(F))
F_abs = np.abs(F_norm)

Y10 = np.sqrt(3/(4*np.pi)) * Z
ReY1m1 = np.sqrt(3/(8*np.pi)) * X
ImY1m1 = -np.sqrt(3/(8*np.pi)) * Y
Y20 = np.sqrt(5/(16*np.pi)) * (2*Z**2 - X**2 - Y**2)
Y22_re = np.sqrt(15/(32*np.pi)) * (X**2 - Y**2)

D_y1x = F_norm * (ReY1m1 / np.max(np.abs(ReY1m1)))
D_y10 = F_norm * (Y10 / np.max(np.abs(Y10)))
D_y20 = F_norm * (Y20 / np.max(np.abs(Y20)))

EXTENT = [-np.pi, np.pi, -np.pi/2, np.pi/2]
XTICKS = [-np.pi, -np.pi/2, 0, np.pi/2, np.pi]
XTICKLABELS = [r"$-\pi$", r"$-\pi/2$", r"$0$", r"$\pi/2$", r"$\pi$"]
YTICKS = [-np.pi/2, 0, np.pi/2]
YTICKLABELS = [r"$-\pi/2$", r"$0$", r"$\pi/2$"]


def save(fig, name):
    fig.savefig(FIGDIR / f"{name}.svg", format="svg", bbox_inches="tight")
    plt.close(fig)


def format_axis(ax):
    ax.set_xlabel(r"$\varphi$")
    ax.set_ylabel(r"latitud $\lambda=\pi/2-\theta$")
    ax.set_xticks(XTICKS, XTICKLABELS)
    ax.set_yticks(YTICKS, YTICKLABELS)
    ax.grid(True, alpha=0.25, linewidth=0.6)


def map_single(C, title, cbar_label, name, cmap="coolwarm", symmetric=True, zero_contour=True):
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    if symmetric:
        vmax = float(np.nanmax(np.abs(C)))
        norm = colors.TwoSlopeNorm(vmin=-vmax, vcenter=0.0, vmax=vmax)
    else:
        norm = colors.Normalize(vmin=float(np.nanmin(C)), vmax=float(np.nanmax(C)))
    im = ax.imshow(C, origin="lower", extent=EXTENT, aspect="auto", cmap=cmap, norm=norm, interpolation="bilinear")
    if zero_contour:
        ax.contour(LON, LAT, C, levels=[0.0], linewidths=1.1, colors="black")
    ax.set_title(title)
    format_axis(ax)
    cbar = fig.colorbar(im, ax=ax, orientation="vertical", pad=0.025, shrink=0.92)
    cbar.set_label(cbar_label)
    save(fig, name)


def map_panel(fields, titles, name, cmap="coolwarm", symmetric=True, zero_contour=True):
    n = len(fields)
    fig, axes = plt.subplots(1, n, figsize=(4.4*n, 3.3), sharex=True, sharey=True)
    if n == 1:
        axes = [axes]
    if symmetric:
        vmax = max(float(np.nanmax(np.abs(C))) for C in fields)
        norm = colors.TwoSlopeNorm(vmin=-vmax, vcenter=0.0, vmax=vmax)
    else:
        norm = colors.Normalize(vmin=min(float(np.nanmin(C)) for C in fields), vmax=max(float(np.nanmax(C)) for C in fields))
    im = None
    for ax, C, title in zip(axes, fields, titles):
        im = ax.imshow(C, origin="lower", extent=EXTENT, aspect="auto", cmap=cmap, norm=norm, interpolation="bilinear")
        if zero_contour:
            ax.contour(LON, LAT, C, levels=[0.0], linewidths=0.9, colors="black")
        ax.set_title(title)
        format_axis(ax)
    fig.colorbar(im, ax=axes, orientation="vertical", pad=0.02, shrink=0.88)
    save(fig, name)


# 1. Mapa firmado de la funcion angular.
map_single(
    F_norm,
    r"Mapa angular de $(x+y+2z)/r$",
    r"$(x+y+2z)/(r\max|\cdot|)$",
    "fig_01_mapa_funcion_angular",
    cmap="coolwarm",
    symmetric=True,
    zero_contour=True,
)

# 2. Mapa de magnitud de la funcion angular.
map_single(
    F_abs,
    r"Magnitud angular de $(x+y+2z)/r$",
    r"$|(x+y+2z)/r|/\max|\cdot|$",
    "fig_02_mapa_magnitud_funcion_angular",
    cmap="viridis",
    symmetric=False,
    zero_contour=False,
)

# 3. Mapas de la base real de l=1.
map_panel(
    [ReY1m1, ImY1m1, Y10],
    [r"$\operatorname{Re}Y_1^{-1}\propto x/r$", r"$\operatorname{Im}Y_1^{-1}\propto -y/r$", r"$Y_1^0\propto z/r$"],
    "fig_03_mapas_base_l1",
    cmap="coolwarm",
    symmetric=True,
    zero_contour=True,
)

# 4. Modos con l=2: topologia angular distinta.
map_panel(
    [Y20, Y22_re],
    [r"$Y_2^0$", r"$\operatorname{Re}Y_2^2$"],
    "fig_04_mapas_l2",
    cmap="coolwarm",
    symmetric=True,
    zero_contour=True,
)

# 5. Densidades angulares del producto que se integra.
map_panel(
    [D_y1x, D_y10, D_y20],
    [r"$(x+y+2z)\operatorname{Re}Y_1^{-1}$", r"$(x+y+2z)Y_1^0$", r"$(x+y+2z)Y_2^0$"],
    "fig_05_densidades_integracion",
    cmap="coolwarm",
    symmetric=True,
    zero_contour=True,
)
