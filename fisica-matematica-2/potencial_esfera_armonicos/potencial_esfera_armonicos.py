#!/usr/bin/env python3
# Figuras para material de estudio de Fisica Matematica II.
# Genera solamente archivos SVG en ./figures.

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
    "svg.fonttype": "none",
})

def save(fig, name):
    fig.savefig(FIGDIR / f"{name}.svg", format="svg", bbox_inches="tight")
    plt.close(fig)

def signed_norm(Z):
    zmax = np.nanmax(np.abs(Z))
    if not np.isfinite(zmax) or zmax == 0:
        zmax = 1.0
    return colors.TwoSlopeNorm(vmin=-zmax, vcenter=0.0, vmax=zmax)

def add_zero_contour(ax, X, Y, Z):
    try:
        ax.contour(X, Y, Z, levels=[0], colors="k", linewidths=0.8, alpha=0.85)
    except Exception:
        pass

# Cascaron esferico con densidad superficial sigma(theta,varphi).
R0 = 1.0
C0 = 1.0

def angular(theta, varphi):
    return np.sin(theta)**2*np.sin(varphi)*np.cos(varphi)

def phi_inside_xyz(x, y, z):
    return C0*x*y

def phi_outside_xyz(x, y, z):
    r = np.sqrt(x*x + y*y + z*z)
    val = np.full_like(r, np.nan, dtype=float)
    mask = r >= R0
    val[mask] = C0*(R0**5)*x[mask]*y[mask]/r[mask]**5
    return val

# Mapa angular sobre la esfera.
lon = np.linspace(-np.pi, np.pi, 360)
lat = np.linspace(-np.pi/2, np.pi/2, 180)
LON, LAT = np.meshgrid(lon, lat)
TH = np.pi/2 - LAT
SIG = angular(TH, LON)

fig, ax = plt.subplots(figsize=(7.0, 3.2))
im = ax.imshow(SIG, extent=[-180,180,-90,90], origin="lower", aspect="auto", cmap="coolwarm", norm=signed_norm(SIG))
ax.contour(np.degrees(LON), np.degrees(LAT), SIG, levels=[0], colors="k", linewidths=0.8)
ax.set_xlabel(r"longitud $\varphi$ [grados]")
ax.set_ylabel(r"latitud $\lambda=\pi/2-\theta$ [grados]")
ax.set_title(r"Densidad superficial $\sigma(\theta,\varphi)$")
fig.colorbar(im, ax=ax, label=r"$\sigma/\zeta$")
save(fig, "fig_01_sigma_esfera")

fig, ax = plt.subplots(figsize=(7.0, 3.2))
im = ax.imshow(np.abs(SIG), extent=[-180,180,-90,90], origin="lower", aspect="auto", cmap="viridis")
ax.set_xlabel(r"longitud $\varphi$ [grados]")
ax.set_ylabel(r"latitud $\lambda=\pi/2-\theta$ [grados]")
ax.set_title(r"Magnitud angular $|\sigma(\theta,\varphi)|$")
fig.colorbar(im, ax=ax, label=r"$|\sigma|/|\zeta|$")
save(fig, "fig_05_superficie_phi_interior")

# Plano z=0.
x = np.linspace(-2.1, 2.1, 360)
y = np.linspace(-2.1, 2.1, 360)
XX, YY = np.meshgrid(x, y)
ZZ = np.zeros_like(XX)
RR = np.sqrt(XX**2 + YY**2)
Zi = np.full_like(RR, np.nan, dtype=float)
Zi[RR <= R0] = phi_inside_xyz(XX[RR <= R0], YY[RR <= R0], ZZ[RR <= R0])

fig, ax = plt.subplots(figsize=(5.5, 5.0))
im = ax.imshow(Zi, extent=[x.min(), x.max(), y.min(), y.max()], origin="lower", cmap="coolwarm", norm=signed_norm(Zi))
add_zero_contour(ax, XX, YY, Zi)
ax.contour(XX, YY, RR, levels=[R0], colors="k", linewidths=1.0)
ax.axhline(0, color="k", lw=0.7, alpha=0.7)
ax.axvline(0, color="k", lw=0.7, alpha=0.7)
ax.set_aspect("equal")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_title(r"Potencial interior en $z=0$")
fig.colorbar(im, ax=ax, shrink=0.8, label=r"$\phi_i$")
save(fig, "fig_02_potencial_interior_xy")

Ze = phi_outside_xyz(XX, YY, ZZ)
fig, ax = plt.subplots(figsize=(5.5, 5.0))
im = ax.imshow(Ze, extent=[x.min(), x.max(), y.min(), y.max()], origin="lower", cmap="coolwarm", norm=signed_norm(Ze))
add_zero_contour(ax, XX, YY, Ze)
levels = np.linspace(-0.12, 0.12, 9)
ax.contour(XX, YY, Ze, levels=levels, colors="k", linewidths=0.35, alpha=0.6)
ax.contour(XX, YY, RR, levels=[R0], colors="k", linewidths=1.0)
ax.axhline(0, color="k", lw=0.7, alpha=0.7)
ax.axvline(0, color="k", lw=0.7, alpha=0.7)
ax.set_aspect("equal")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_title(r"Potencial exterior en $z=0$")
fig.colorbar(im, ax=ax, shrink=0.8, label=r"$\phi_e$")
save(fig, "fig_03_potencial_exterior_xy")

# Lineas de campo en el exterior del plano z=0.
dx = x[1]-x[0]
dy = y[1]-y[0]
Ey, Ex = np.gradient(-Ze, dy, dx)  # E = -grad phi; np.gradient devuelve d/dy, d/dx.
Ex = np.ma.masked_invalid(Ex)
Ey = np.ma.masked_invalid(Ey)
fig, ax = plt.subplots(figsize=(5.5, 5.0))
im = ax.imshow(Ze, extent=[x.min(), x.max(), y.min(), y.max()], origin="lower", cmap="coolwarm", norm=signed_norm(Ze), alpha=0.85)
ax.streamplot(x, y, Ex, Ey, density=1.2, linewidth=0.7, arrowsize=0.7, color="k")
ax.contour(XX, YY, RR, levels=[R0], colors="k", linewidths=1.0)
ax.set_aspect("equal")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_title(r"Campo exterior en $z=0$")
fig.colorbar(im, ax=ax, shrink=0.8, label=r"$\phi_e$")
save(fig, "fig_04_lineas_campo_xy")
