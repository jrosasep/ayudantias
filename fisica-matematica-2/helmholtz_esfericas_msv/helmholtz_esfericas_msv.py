"""
Figuras para el problema: separación de variables de Helmholtz en coordenadas
esféricas.

El script genera únicamente archivos SVG en la carpeta ./figuras. Las figuras
ilustran tres objetos que aparecen directamente en el desarrollo analítico:

1. La periodicidad azimutal que exige m entero.
2. El sector axial m=0, donde la ecuación polar produce P_l(cos(theta)).
3. El caso alpha=0, donde la ecuación radial de Laplace tiene soluciones
   r^l y r^{-(l+1)} cuando Q=l(l+1).
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.legendre import legval

OUT = Path(__file__).resolve().parent / "figuras"
OUT.mkdir(parents=True, exist_ok=True)


def save_svg(fig: plt.Figure, filename: str) -> None:
    """Guardar una figura exclusivamente en formato SVG."""
    path = OUT / filename
    fig.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figura 1: periodicidad azimutal Phi(phi)=e^{im phi}.
# ---------------------------------------------------------------------------
phi = np.linspace(0.0, 2.0 * np.pi, 800)
fig, ax = plt.subplots(figsize=(8.0, 4.4))
for m in [0, 1, 2, 3]:
    ax.plot(phi / np.pi, np.cos(m * phi), label=rf"$m={m}$")
ax.axvline(0.0, linestyle="--", linewidth=0.8)
ax.axvline(2.0, linestyle="--", linewidth=0.8)
ax.set_title(r"Parte real de $\Phi_m(\phi)=e^{im\phi}$")
ax.set_xlabel(r"$\phi/\pi$")
ax.set_ylabel(r"$\mathrm{Re}\,\Phi_m(\phi)$")
ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0])
ax.set_ylim(-1.15, 1.15)
ax.grid(True, alpha=0.25)
ax.legend(loc="upper right", ncols=2)
ax.text(0.02, -1.05, r"Los extremos $0$ y $2\pi$ representan el mismo punto angular.", fontsize=9)
save_svg(fig, "helmholtz_azimutal_periodicidad.svg")


# ---------------------------------------------------------------------------
# Figura 2: sector axial m=0 y polinomios de Legendre P_l(cos theta).
# ---------------------------------------------------------------------------
theta = np.linspace(0.0, np.pi, 800)
x = np.cos(theta)
fig, ax = plt.subplots(figsize=(8.0, 4.4))
for ell in range(0, 5):
    coeffs = np.zeros(ell + 1)
    coeffs[ell] = 1.0
    Pell = legval(x, coeffs)
    ax.plot(theta / np.pi, Pell, label=rf"$\ell={ell}$, $Q={ell*(ell+1)}$")
ax.set_title(r"Soluciones polares axiales $\Theta_\ell(\theta)=P_\ell(\cos\theta)$")
ax.set_xlabel(r"$\theta/\pi$")
ax.set_ylabel(r"$P_\ell(\cos\theta)$")
ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_ylim(-1.15, 1.15)
ax.grid(True, alpha=0.25)
ax.legend(loc="lower left", ncols=2, fontsize=8)
save_svg(fig, "helmholtz_polar_legendre_axial.svg")


# ---------------------------------------------------------------------------
# Figura 3: caso alpha=0. Soluciones radiales independientes de Laplace.
# ---------------------------------------------------------------------------
r = np.linspace(0.35, 2.0, 600)
fig, ax = plt.subplots(figsize=(8.0, 4.4))
for ell in [0, 1, 2, 3]:
    interior = r**ell
    exterior = r ** (-(ell + 1))
    # Normalización visual: no cambia la forma funcional ni la dependencia radial.
    interior = interior / interior.max()
    exterior = exterior / exterior.max()
    ax.plot(r, interior, label=rf"$r^{ell}$, $\ell={ell}$")
    ax.plot(r, exterior, linestyle="--", label=rf"$r^{{-{ell+1}}}$, $\ell={ell}$")
ax.set_title(r"Caso $\alpha=0$: ramas radiales de Laplace")
ax.set_xlabel(r"$r$")
ax.set_ylabel("amplitud normalizada")
ax.set_xlim(r.min(), r.max())
ax.set_ylim(-0.02, 1.05)
ax.grid(True, alpha=0.25)
ax.legend(loc="center right", fontsize=7, ncols=2)
ax.text(0.38, 0.06, r"Ramas asociadas a $Q=\ell(\ell+1)$.", fontsize=9)
save_svg(fig, "helmholtz_radial_laplace_alpha_cero.svg")

print(f"Figuras SVG generadas en: {OUT}")
