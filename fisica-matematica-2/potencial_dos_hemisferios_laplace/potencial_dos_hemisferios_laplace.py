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

# Esfera conductora formada por dos hemisferios a potencial opuesto.
from scipy.special import eval_legendre

a = 1.0
V0 = 1.0
Nmax = 29

def coef(n):
    if n % 2 == 0:
        return 0.0
    return ((2*n + 1)*V0/(n + 1))*eval_legendre(n-1, 0.0)

def f_boundary(theta):
    return np.where(theta <= np.pi/2, V0, -V0)

def series_boundary(theta, N):
    x = np.cos(theta)
    total = np.zeros_like(theta, dtype=float)
    for n in range(1, N+1):
        total += coef(n)*eval_legendre(n, x)
    return total

def phi_inside(r, theta, N=Nmax):
    x = np.cos(theta)
    total = np.zeros_like(r, dtype=float)
    for n in range(1, N+1):
        total += coef(n)*(r/a)**n*eval_legendre(n, x)
    return total

def phi_outside(r, theta, N=Nmax):
    x = np.cos(theta)
    total = np.zeros_like(r, dtype=float)
    for n in range(1, N+1):
        total += coef(n)*(a/r)**(n+1)*eval_legendre(n, x)
    return total

# 1. Condicion de borde y truncaciones.
th = np.linspace(0, np.pi, 700)
fig, ax = plt.subplots(figsize=(6.4, 3.4))
ax.plot(th, f_boundary(th), lw=2.2, label="C.d.B.")
for N in [1,3,7,15]:
    ax.plot(th, series_boundary(th, N), lw=1.2, label=rf"$N={N}$")
ax.set_xlabel(r"$\theta$")
ax.set_ylabel(r"$\phi(a,\theta)$")
ax.set_title("C.d.B. y truncaciones de Legendre")
ax.set_xticks([0, np.pi/2, np.pi])
ax.set_xticklabels([r"$0$", r"$\pi/2$", r"$\pi$"])
ax.legend(ncol=3, fontsize=8)
ax.grid(True, alpha=0.25)
save(fig, "fig_01_cdb_truncaciones")

# 2. Coeficientes de Legendre.
ns = np.arange(0, 20)
cs = np.array([coef(int(n)) for n in ns])
fig, ax = plt.subplots(figsize=(6.4, 3.1))
ax.bar(ns, cs, width=0.75)
ax.axhline(0, lw=0.8)
ax.set_xlabel(r"$n$")
ax.set_ylabel(r"$A_n$")
ax.set_title("Coeficientes no nulos de la expansión")
ax.grid(True, axis="y", alpha=0.25)
save(fig, "fig_02_coeficientes_legendre")

# Malla meridiana.
x = np.linspace(-2.2, 2.2, 340)
z = np.linspace(-2.2, 2.2, 340)
XX, ZZ = np.meshgrid(x, z)
RR = np.sqrt(XX**2 + ZZ**2)
TH = np.arccos(np.clip(ZZ/np.where(RR == 0, 1, RR), -1, 1))

# 3. Mapa 2D sobre la frontera: longitud-latitud.
lon = np.linspace(-np.pi, np.pi, 360)
lat = np.linspace(-np.pi/2, np.pi/2, 180)
LON, LAT = np.meshgrid(lon, lat)
Theta = np.pi/2 - LAT
B = f_boundary(Theta)
fig, ax = plt.subplots(figsize=(7.0, 3.2))
im = ax.imshow(B, extent=[-180, 180, -90, 90], origin="lower", aspect="auto", cmap="coolwarm", norm=signed_norm(B))
ax.axhline(0, color="k", lw=0.8)
ax.set_xlabel(r"longitud $\varphi$ [grados]")
ax.set_ylabel(r"latitud $\lambda=\pi/2-\theta$ [grados]")
ax.set_title("Potencial impuesto sobre la esfera")
fig.colorbar(im, ax=ax, label=r"$\phi(a,\theta)$")
save(fig, "fig_05_esfera_hemisferios")

# 4. Interior en corte meridiano.
Zi = np.full_like(RR, np.nan, dtype=float)
mask_i = RR <= a
Zi[mask_i] = phi_inside(RR[mask_i], TH[mask_i])
fig, ax = plt.subplots(figsize=(5.5, 5.0))
im = ax.imshow(Zi, extent=[x.min(), x.max(), z.min(), z.max()], origin="lower", cmap="coolwarm", norm=signed_norm(Zi))
add_zero_contour(ax, XX, ZZ, Zi)
ax.contour(XX, ZZ, RR, levels=[a], colors="k", linewidths=1.0)
ax.axhline(0, color="k", lw=0.8, alpha=0.7)
ax.set_aspect("equal")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$z$")
ax.set_title("Potencial interior, corte meridiano")
fig.colorbar(im, ax=ax, shrink=0.8, label=r"$\phi_i$")
save(fig, "fig_03_potencial_interior")

# 5. Exterior con lineas equipotenciales en corte meridiano.
Ze = np.full_like(RR, np.nan, dtype=float)
mask_e = RR >= a
Ze[mask_e] = phi_outside(RR[mask_e], TH[mask_e])
fig, ax = plt.subplots(figsize=(5.5, 5.0))
im = ax.imshow(Ze, extent=[x.min(), x.max(), z.min(), z.max()], origin="lower", cmap="coolwarm", norm=signed_norm(Ze))
add_zero_contour(ax, XX, ZZ, Ze)
levels = np.linspace(-0.8, 0.8, 9)
ax.contour(XX, ZZ, Ze, levels=levels, colors="k", linewidths=0.35, alpha=0.6)
ax.contour(XX, ZZ, RR, levels=[a], colors="k", linewidths=1.0)
ax.axhline(0, color="k", lw=0.8, alpha=0.7)
ax.set_aspect("equal")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$z$")
ax.set_title("Potencial exterior, corte meridiano")
fig.colorbar(im, ax=ax, shrink=0.8, label=r"$\phi_e$")
save(fig, "fig_04_potencial_exterior")
