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

# Problema de Dirichlet en una esfera.
R0 = 1.0

def phi_inside(r, theta):
    return -2.0 + (r/R0)*np.cos(theta) + (r/R0)**2*(3*np.cos(theta)**2 - 1)

def phi_outside(r, theta):
    return -2.0*(R0/r) + (R0/r)**2*np.cos(theta) + (R0/r)**3*(3*np.cos(theta)**2 - 1)

def boundary(theta):
    return np.cos(theta) - 3*np.sin(theta)**2

# 1. Condicion de borde y componentes.
th = np.linspace(0, np.pi, 700)
fig, ax = plt.subplots(figsize=(6.4, 3.4))
ax.plot(th, boundary(th), lw=2.2, label=r"$f(\theta)$")
ax.plot(th, -2*np.ones_like(th), lw=1.0, ls="--", label=r"$-2$")
ax.plot(th, np.cos(th), lw=1.0, ls="--", label=r"$\cos\theta$")
ax.plot(th, 3*np.cos(th)**2 - 1, lw=1.0, ls="--", label=r"$3\cos^2\theta-1$")
ax.set_xlabel(r"$\theta$")
ax.set_ylabel(r"$\phi(R,\theta)$")
ax.set_xticks([0, np.pi/2, np.pi])
ax.set_xticklabels([r"$0$", r"$\pi/2$", r"$\pi$"])
ax.set_title("Condición de borde y descomposición")
ax.legend(ncol=2, fontsize=8)
ax.grid(True, alpha=0.25)
save(fig, "fig_01_condicion_borde")

# 2. Mapa angular sobre la esfera.
lon = np.linspace(-np.pi, np.pi, 360)
lat = np.linspace(-np.pi/2, np.pi/2, 180)
LON, LAT = np.meshgrid(lon, lat)
Theta = np.pi/2 - LAT
B = boundary(Theta)
fig, ax = plt.subplots(figsize=(7.0, 3.2))
im = ax.imshow(B, extent=[-180,180,-90,90], origin="lower", aspect="auto", cmap="coolwarm", norm=signed_norm(B))
zero_lats = []
# zeros of 3c^2 + c - 3 = 0, c=cos theta
roots = np.roots([3,1,-3])
for c in roots:
    if abs(c.imag) < 1e-12 and -1 <= c.real <= 1:
        theta0 = np.arccos(c.real)
        zero_lats.append(90 - np.degrees(theta0))
for la in zero_lats:
    ax.axhline(la, color="k", lw=0.8)
ax.set_xlabel(r"longitud $\varphi$ [grados]")
ax.set_ylabel(r"latitud $\lambda=\pi/2-\theta$ [grados]")
ax.set_title(r"Mapa angular de $\phi(R,\theta)$")
fig.colorbar(im, ax=ax, label=r"$\phi(R,\theta)$")
save(fig, "fig_05_esfera_coloreada")

# Malla meridiana.
x = np.linspace(-2.2, 2.2, 340)
z = np.linspace(-2.2, 2.2, 340)
XX, ZZ = np.meshgrid(x, z)
RR = np.sqrt(XX**2 + ZZ**2)
TH = np.arccos(np.clip(ZZ/np.where(RR == 0, 1, RR), -1, 1))

Zi = np.full_like(RR, np.nan, dtype=float)
Zi[RR <= R0] = phi_inside(RR[RR <= R0], TH[RR <= R0])
fig, ax = plt.subplots(figsize=(5.5, 5.0))
im = ax.imshow(Zi, extent=[x.min(), x.max(), z.min(), z.max()], origin="lower", cmap="coolwarm", norm=signed_norm(Zi))
ax.contour(XX, ZZ, Zi, levels=9, colors="k", linewidths=0.35, alpha=0.55)
add_zero_contour(ax, XX, ZZ, Zi)
ax.contour(XX, ZZ, RR, levels=[R0], colors="k", linewidths=1.0)
ax.set_aspect("equal")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$z$")
ax.set_title("Potencial interior, corte meridiano")
fig.colorbar(im, ax=ax, shrink=0.8, label=r"$\phi_i$")
save(fig, "fig_02_potencial_interior")

Ze = np.full_like(RR, np.nan, dtype=float)
mask = RR >= R0
Ze[mask] = phi_outside(RR[mask], TH[mask])
fig, ax = plt.subplots(figsize=(5.5, 5.0))
im = ax.imshow(Ze, extent=[x.min(), x.max(), z.min(), z.max()], origin="lower", cmap="coolwarm", norm=signed_norm(Ze))
ax.contour(XX, ZZ, Ze, levels=9, colors="k", linewidths=0.35, alpha=0.55)
add_zero_contour(ax, XX, ZZ, Ze)
ax.contour(XX, ZZ, RR, levels=[R0], colors="k", linewidths=1.0)
ax.set_aspect("equal")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$z$")
ax.set_title("Extensión exterior, corte meridiano")
fig.colorbar(im, ax=ax, shrink=0.8, label=r"$\phi_e$")
save(fig, "fig_03_potencial_exterior")

# 5. Perfiles radiales en direcciones fijas.
rr_i = np.linspace(0, R0, 300)
rr_e = np.linspace(R0, 2.5*R0, 400)
angles = [(0, r"$\theta=0$"), (np.pi/2, r"$\theta=\pi/2$"), (np.pi, r"$\theta=\pi$")]
fig, ax = plt.subplots(figsize=(6.4, 3.4))
for th0, lab in angles:
    ax.plot(rr_i, phi_inside(rr_i, th0), lw=1.8, label=lab + r" int.")
    ax.plot(rr_e, phi_outside(rr_e, th0), lw=1.4, ls="--", label=lab + r" ext.")
ax.axvline(R0, lw=0.8, color="k")
ax.set_xlabel(r"$r/R$")
ax.set_ylabel(r"$\phi(r,\theta)$")
ax.set_title("Perfiles radiales interiores y exteriores")
ax.grid(True, alpha=0.25)
ax.legend(ncol=2, fontsize=7)
save(fig, "fig_04_descomposicion_frontera")
