"""
Figuras para el problema: difusión del calor 2D en un rectángulo.

El script genera únicamente archivos SVG en la carpeta ./figuras.
La normalización y los parámetros son los mismos que se usan en el texto:
    0 < x < a, 0 < y < b,
    alpha > 0,
    psi = sum_{n,m} A_nm sin(n*pi*x/a) sin(m*pi*y/b) exp(-gamma_nm t),
    gamma_nm = alpha*pi^2(n^2/a^2 + m^2/b^2).

Para la evolución temporal se usa una condición inicial suave y localizada,
compatible con las condiciones de borde homogéneas:
    f(x,y) = T0 sin(pi*x/a) sin(pi*y/b)
             exp(-((x-x0)^2/(2 sigma_x^2) + (y-y0)^2/(2 sigma_y^2))).
Los coeficientes A_nm se calculan con la fórmula de Fourier seno obtenida en
el desarrollo analítico.
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Parámetros físicos y geométricos del ejemplo
# ---------------------------------------------------------------------------
a = 1.0          # ancho del rectángulo en la dirección x
b = 2.0          # alto del rectángulo en la dirección y
alpha = 1.0      # difusividad térmica
T0 = 1.0         # escala de temperatura inicial
x0 = 0.60 * a    # centro de la perturbación inicial
y0 = 0.70 * b
sigma_x = 0.12 * a
sigma_y = 0.13 * b

# Resolución espacial usada para las figuras.
Nx = 220
Ny = 260
x = np.linspace(0.0, a, Nx)
y = np.linspace(0.0, b, Ny)
X, Y = np.meshgrid(x, y, indexing="xy")

OUT = Path(__file__).resolve().parent / "figuras"
OUT.mkdir(parents=True, exist_ok=True)


def save_svg(fig: plt.Figure, filename: str) -> None:
    """Guardar una figura exclusivamente en formato SVG."""
    path = OUT / filename
    fig.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)


def modo(n: int, m: int) -> np.ndarray:
    """Autofunción espacial X_n(x)Y_m(y)."""
    return np.sin(n * np.pi * X / a) * np.sin(m * np.pi * Y / b)


def gamma_nm(n: int, m: int) -> float:
    """Tasa de decaimiento del modo (n,m)."""
    return alpha * np.pi**2 * (n**2 / a**2 + m**2 / b**2)


# ---------------------------------------------------------------------------
# Figura 1: primer modo espacial permitido por el borde homogéneo.
# ---------------------------------------------------------------------------
Z11 = modo(1, 1)
fig, ax = plt.subplots(figsize=(5.2, 6.2))
im = ax.imshow(
    Z11,
    origin="lower",
    extent=(0, a, 0, b),
    aspect="equal",
    interpolation="bicubic",
)
cs = ax.contour(X, Y, Z11, levels=8, linewidths=0.7)
ax.clabel(cs, inline=True, fontsize=7, fmt="%.2f")
ax.set_title(r"Modo espacial $(n,m)=(1,1)$")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_xticks([0, a / 2, a])
ax.set_yticks([0, b / 2, b])
ax.text(0.02, b - 0.12, r"$\psi=0$ en el borde", fontsize=9, va="top")
fig.colorbar(im, ax=ax, label=r"$X_1(x)Y_1(y)$")
save_svg(fig, "calor_2d_modo_11.svg")


# ---------------------------------------------------------------------------
# Figura 2: evolución temporal obtenida desde la serie doble truncada.
# ---------------------------------------------------------------------------
def condicion_inicial() -> np.ndarray:
    envolvente = np.exp(
        -0.5 * (((X - x0) / sigma_x) ** 2 + ((Y - y0) / sigma_y) ** 2)
    )
    # El factor seno fuerza f=0 en los cuatro bordes, tal como exige el problema.
    return T0 * np.sin(np.pi * X / a) * np.sin(np.pi * Y / b) * envolvente


f0 = condicion_inicial()

# Coeficientes de Fourier seno. La integral se evalúa por cuadratura trapezoidal
# sobre la misma malla usada para graficar. Para el propósito didáctico de estas
# figuras, nmax=mmax=36 entrega una reconstrucción suficientemente estable.
nmax = 36
mmax = 36
A = np.zeros((nmax, mmax))
for n in range(1, nmax + 1):
    sx = np.sin(n * np.pi * x / a)
    for m in range(1, mmax + 1):
        sy = np.sin(m * np.pi * y / b)
        integrand = f0 * sy[:, None] * sx[None, :]
        # Integrar primero en y y luego en x.
        integral_y = np.trapezoid(integrand, y, axis=0)
        integral_xy = np.trapezoid(integral_y, x)
        A[n - 1, m - 1] = 4.0 * integral_xy / (a * b)


def psi_truncada(t: float) -> np.ndarray:
    Z = np.zeros_like(X)
    for n in range(1, nmax + 1):
        sx = np.sin(n * np.pi * X / a)
        for m in range(1, mmax + 1):
            sy = np.sin(m * np.pi * Y / b)
            Z += A[n - 1, m - 1] * sx * sy * np.exp(-gamma_nm(n, m) * t)
    return Z


tiempos = [0.0, 0.0025, 0.01, 0.04]
soluciones = [psi_truncada(t) for t in tiempos]
vmax = max(np.max(Z) for Z in soluciones)
vmin = min(np.min(Z) for Z in soluciones)

fig, axes = plt.subplots(1, 4, figsize=(13.2, 3.6), constrained_layout=True)
for ax, t, Z in zip(axes, tiempos, soluciones):
    im = ax.imshow(
        Z,
        origin="lower",
        extent=(0, a, 0, b),
        aspect="equal",
        interpolation="bicubic",
        vmin=vmin,
        vmax=vmax,
    )
    ax.plot([x0], [y0], marker="o", markersize=4, color="black")
    ax.set_title(rf"$t={t:.4f}$")
    ax.set_xlabel(r"$x$")
    if ax is axes[0]:
        ax.set_ylabel(r"$y$")
    else:
        ax.set_yticklabels([])
    ax.set_xticks([0, a / 2, a])
    ax.set_yticks([0, b / 2, b])
fig.colorbar(im, ax=axes, shrink=0.82, label=r"$\psi(x,y,t)$")
save_svg(fig, "calor_2d_evolucion_seno_gaussiana.svg")


# ---------------------------------------------------------------------------
# Figura 3: matriz de tasas de decaimiento gamma_nm.
# ---------------------------------------------------------------------------
Nshow = 5
G = np.zeros((Nshow, Nshow))
for n in range(1, Nshow + 1):
    for m in range(1, Nshow + 1):
        G[m - 1, n - 1] = gamma_nm(n, m)

fig, ax = plt.subplots(figsize=(6.2, 5.2))
im = ax.imshow(G, origin="lower", aspect="equal")
ax.set_title(r"Tasas de decaimiento $\gamma_{nm}$")
ax.set_xlabel(r"índice $n$ en $x$")
ax.set_ylabel(r"índice $m$ en $y$")
ax.set_xticks(np.arange(Nshow), labels=np.arange(1, Nshow + 1))
ax.set_yticks(np.arange(Nshow), labels=np.arange(1, Nshow + 1))
for j in range(Nshow):
    for i in range(Nshow):
        ax.text(i, j, f"{G[j, i]:.1f}", ha="center", va="center", fontsize=8)
fig.colorbar(im, ax=ax, label=r"$\gamma_{nm}=\alpha\pi^2(n^2/a^2+m^2/b^2)$")
save_svg(fig, "calor_2d_tasas_decaimiento.svg")

print(f"Figuras SVG generadas en: {OUT}")
