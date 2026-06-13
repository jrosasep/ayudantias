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

# Laplace 2D en un cuarto de anillo.
a = 1.0
b = 2.0
coef_f = {1: 1.0, 2: 0.55, 3: -0.35, 4: 0.20}

def f(phi):
    total = np.zeros_like(phi)
    for n, c in coef_f.items():
        total += c*np.sin(2*n*phi)
    return total

def radial(n, r):
    return r**(2*n) - a**(4*n)*r**(-2*n)

def A_n(n):
    c = coef_f.get(n, 0.0)
    return c / (b**(2*n) - a**(4*n)*b**(-2*n))

def mode(n, r, phi):
    return radial(n, r)*np.sin(2*n*phi)

def psi(r, phi):
    total = np.zeros_like(r)
    for n in coef_f:
        total += A_n(n)*mode(n, r, phi)
    return total

# Malla cartesiana del dominio fisico. Usamos imshow para obtener SVG livianos:
# el campo se guarda como imagen raster embebida y las curvas nodales como trazos.
Nxy = 340
x = np.linspace(0, b, Nxy)
y = np.linspace(0, b, Nxy)
XX, YY = np.meshgrid(x, y)
RR = np.sqrt(XX**2 + YY**2)
PP = np.arctan2(YY, XX)
mask_domain = (RR >= a) & (RR <= b) & (PP >= 0) & (PP <= np.pi/2)
ZZ = np.full_like(RR, np.nan, dtype=float)
ZZ[mask_domain] = psi(RR[mask_domain], PP[mask_domain])
# Malla polar auxiliar para dibujar contornos de modos con la misma grilla cartesiana.
phi = np.linspace(0, np.pi/2, 400)

# 1. Condicion de borde en r=b.
ph = np.linspace(0, np.pi/2, 500)
fig, ax = plt.subplots(figsize=(6.2, 3.1))
ax.plot(ph, f(ph), lw=2)
ax.axhline(0, lw=0.8)
ax.set_xlabel(r"$\phi$")
ax.set_ylabel(r"$f(\phi)$")
ax.set_title(r"Condición de borde en $r=b$")
ax.set_xticks([0, np.pi/8, np.pi/4, 3*np.pi/8, np.pi/2])
ax.set_xticklabels([r"$0$", r"$\pi/8$", r"$\pi/4$", r"$3\pi/8$", r"$\pi/2$"])
ax.grid(True, alpha=0.25)
save(fig, "fig_01_condicion_borde")

# 2. Mapa 2D de la solucion truncada en el cuarto de anillo.
fig, ax = plt.subplots(figsize=(5.5, 5.0))
pm = ax.imshow(ZZ, extent=[0, b, 0, b], origin="lower", cmap="coolwarm", norm=signed_norm(ZZ))
add_zero_contour(ax, XX, YY, ZZ)
ax.plot(a*np.cos(phi), a*np.sin(phi), "k", lw=1.0)
ax.plot(b*np.cos(phi), b*np.sin(phi), "k", lw=1.0)
ax.plot([a,b],[0,0], "k", lw=1.0)
ax.plot([0,0],[a,b], "k", lw=1.0)
ax.set_aspect("equal")
ax.set_xlabel(r"$x=r\cos\phi$")
ax.set_ylabel(r"$y=r\sin\phi$")
ax.set_title(r"Mapa 2D de $\Psi(r,\phi)$")
fig.colorbar(pm, ax=ax, shrink=0.8, label=r"$\Psi$")
save(fig, "fig_02_modo_n1")

# 3. Primer modo separable.
Z1 = np.full_like(RR, np.nan, dtype=float)
Z1[mask_domain] = mode(1, RR[mask_domain], PP[mask_domain])
fig, ax = plt.subplots(figsize=(5.5, 5.0))
pm = ax.imshow(Z1, extent=[0, b, 0, b], origin="lower", cmap="coolwarm", norm=signed_norm(Z1))
add_zero_contour(ax, XX, YY, Z1)
ax.plot(a*np.cos(phi), a*np.sin(phi), "k", lw=1.0)
ax.plot(b*np.cos(phi), b*np.sin(phi), "k", lw=1.0)
ax.plot([a,b],[0,0], "k", lw=1.0)
ax.plot([0,0],[a,b], "k", lw=1.0)
ax.set_aspect("equal")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_title(r"Primer modo separable, $n=1$")
fig.colorbar(pm, ax=ax, shrink=0.8, label=r"$R_1(r)\sin(2\phi)$")
save(fig, "fig_03_modo_n2")

# 4. Segundo modo separable, con nodos angulares adicionales.
Z2 = np.full_like(RR, np.nan, dtype=float)
Z2[mask_domain] = mode(2, RR[mask_domain], PP[mask_domain])
fig, ax = plt.subplots(figsize=(5.5, 5.0))
pm = ax.imshow(Z2, extent=[0, b, 0, b], origin="lower", cmap="coolwarm", norm=signed_norm(Z2))
add_zero_contour(ax, XX, YY, Z2)
ax.plot(a*np.cos(phi), a*np.sin(phi), "k", lw=1.0)
ax.plot(b*np.cos(phi), b*np.sin(phi), "k", lw=1.0)
ax.plot([a,b],[0,0], "k", lw=1.0)
ax.plot([0,0],[a,b], "k", lw=1.0)
ax.set_aspect("equal")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_title(r"Segundo modo separable, $n=2$")
fig.colorbar(pm, ax=ax, shrink=0.8, label=r"$R_2(r)\sin(4\phi)$")
save(fig, "fig_04_superposicion_contornos")

# 5. Perfiles radiales de algunos modos normalizados.
fig, ax = plt.subplots(figsize=(6.2, 3.4))
rr = np.linspace(a, b, 600)
for n in [1,2,3,4]:
    prof = radial(n, rr)
    prof = prof/np.max(np.abs(prof))
    ax.plot(rr, prof, lw=1.8, label=rf"$n={n}$")
ax.axhline(0, lw=0.8)
ax.set_xlabel(r"$r$")
ax.set_ylabel(r"$R_n(r)/\max |R_n|$")
ax.set_title("Perfiles radiales normalizados")
ax.legend(ncol=4, frameon=True)
ax.grid(True, alpha=0.25)
save(fig, "fig_05_superficie_3d")
