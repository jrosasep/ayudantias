"""Visualizacion numerica de un plano cargado inferido desde el potencial.

Se adoptan unidades adimensionales con una longitud de referencia L=1:

    E~ = E L^3 / V0,
    sigma~ = sigma L^3 / (epsilon_0 V0).

La singularidad del potencial en el origen se excluye de todas las mallas.
El script genera un PDF vectorial junto al archivo fuente.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LogNorm, Normalize


def campo_adimensional(
    x: np.ndarray, y: np.ndarray, z: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Devuelve el campo adimensional en las regiones z>0 y z<0."""

    r2 = x**2 + y**2 + z**2
    r5 = r2**2.5
    factor = np.where(z > 0.0, 1.0, 0.5)
    with np.errstate(divide="ignore", invalid="ignore"):
        ex = factor * 3.0 * x * z / r5
        ey = factor * 3.0 * y * z / r5
        ez = factor * (3.0 * z**2 - r2) / r5
    return ex, ey, ez


def densidad_adimensional(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Densidad sigma~=sigma L^3/(epsilon_0 V0) sobre z=0."""

    rho = np.hypot(x, y)
    with np.errstate(divide="ignore", invalid="ignore"):
        return -0.5 / rho**3


def comprobar_frontera() -> None:
    """Verifica numericamente los limites normales y su salto."""

    rho = np.array([0.45, 0.75, 1.0, 1.4, 2.0])
    delta = 1.0e-6
    x = rho
    y = np.zeros_like(rho)
    _, _, ez_mas = campo_adimensional(x, y, np.full_like(rho, delta))
    _, _, ez_menos = campo_adimensional(x, y, np.full_like(rho, -delta))
    esperado_mas = -1.0 / rho**3
    esperado_menos = -0.5 / rho**3
    salto_esperado = -0.5 / rho**3

    error = max(
        float(np.max(np.abs(ez_mas - esperado_mas))),
        float(np.max(np.abs(ez_menos - esperado_menos))),
        float(np.max(np.abs((ez_mas - ez_menos) - salto_esperado))),
    )
    if error > 2.0e-9:
        raise RuntimeError(f"Fallo en la comprobacion de frontera: error={error:.3e}")
    print(f"Comprobacion de frontera superada: error maximo={error:.3e}")


def crear_figura(ruta_salida: Path) -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "mathtext.fontset": "stix",
            "font.size": 11.1,
            "axes.titlesize": 11.6,
            "axes.labelsize": 10.7,
            "figure.dpi": 140,
            "savefig.dpi": 220,
        }
    )

    figura = plt.figure(figsize=(10.6, 6.4))
    rejilla = figura.add_gridspec(
        2,
        2,
        width_ratios=[0.88, 1.35],
        height_ratios=[1.0, 1.0],
        wspace=0.20,
        hspace=0.36,
    )
    ax_sigma = figura.add_subplot(rejilla[0, 0])
    ax_corte = figura.add_subplot(rejilla[1, 0])
    ax_3d = figura.add_subplot(rejilla[:, 1], projection="3d")

    mapa_sigma = plt.get_cmap("plasma")
    norma_sigma = Normalize(vmin=-1.70, vmax=-0.01)
    mapa_campo = plt.get_cmap("viridis")
    norma_campo = LogNorm(vmin=0.035, vmax=22.0)

    # --------------------------------------------------------------
    # Panel (a): densidad superficial sobre el plano.
    # --------------------------------------------------------------
    coordenadas = np.linspace(-2.25, 2.25, 260)
    x, y = np.meshgrid(coordenadas, coordenadas)
    rho = np.hypot(x, y)
    sigma = densidad_adimensional(x, y)
    sigma_m = np.ma.array(sigma, mask=rho < 0.33)
    imagen = ax_sigma.pcolormesh(
        x,
        y,
        np.clip(sigma_m, norma_sigma.vmin, norma_sigma.vmax),
        cmap=mapa_sigma,
        norm=norma_sigma,
        shading="auto",
    )
    ax_sigma.add_patch(plt.Circle((0.0, 0.0), 0.33, fill=False, color="white", lw=1.1))
    ax_sigma.text(
        0.0,
        0.0,
        "origen\nexcluido",
        ha="center",
        va="center",
        color="black",
        fontsize=7.4,
        linespacing=0.92,
    )
    ax_sigma.contour(x, y, rho, levels=[0.6, 1.0, 1.5, 2.0], colors="white", linewidths=0.45)
    ax_sigma.set_aspect("equal")
    ax_sigma.set_xlabel(r"$x/L$")
    ax_sigma.set_ylabel(r"$y/L$")
    ax_sigma.set_title(r"(a) Densidad superficial $\widetilde{\sigma}<0$")

    # --------------------------------------------------------------
    # Panel (b): campo en el corte meridiano y=0.
    # --------------------------------------------------------------
    coord_corte = np.linspace(-2.25, 2.25, 185)
    xc, zc = np.meshgrid(coord_corte, coord_corte)
    yc = np.zeros_like(xc)
    ex, _, ez = campo_adimensional(xc, yc, zc)
    magnitud = np.hypot(ex, ez)
    mascara = np.hypot(xc, zc) < 0.24
    ex_m = np.ma.array(ex, mask=mascara)
    ez_m = np.ma.array(ez, mask=mascara)
    magnitud_m = np.ma.array(magnitud, mask=mascara)
    ax_corte.streamplot(
        coord_corte,
        coord_corte,
        ex_m,
        ez_m,
        color=magnitud_m,
        cmap=mapa_campo,
        norm=norma_campo,
        density=1.20,
        linewidth=0.82,
        arrowsize=0.85,
        broken_streamlines=True,
    )
    ax_corte.axhline(0.0, color="#d62728", lw=1.5)
    ax_corte.text(1.95, 0.09, r"$z=0$", color="#b2182b", ha="right", va="bottom")
    ax_corte.text(-2.08, 1.88, r"$z>0$", ha="left", va="top")
    ax_corte.text(-2.08, -1.88, r"$z<0$", ha="left", va="bottom")
    ax_corte.add_patch(plt.Circle((0.0, 0.0), 0.24, fill=False, color="white", lw=1.0))
    ax_corte.set_aspect("equal")
    ax_corte.set_xlim(-2.25, 2.25)
    ax_corte.set_ylim(-2.25, 2.25)
    ax_corte.set_xlabel(r"$x/L$")
    ax_corte.set_ylabel(r"$z/L$")
    ax_corte.set_title(r"(b) Campo eléctrico en el plano $y=0$")

    # --------------------------------------------------------------
    # Panel (c): plano coloreado y campo tridimensional.
    # --------------------------------------------------------------
    plano = np.linspace(-1.85, 1.85, 55)
    xp, yp = np.meshgrid(plano, plano)
    zp = np.zeros_like(xp)
    rhop = np.hypot(xp, yp)
    sigmap = densidad_adimensional(xp, yp)
    colores_plano = mapa_sigma(norma_sigma(np.clip(sigmap, norma_sigma.vmin, norma_sigma.vmax)))
    colores_plano[rhop < 0.30, 3] = 0.0
    ax_3d.plot_surface(
        xp,
        yp,
        zp,
        facecolors=colores_plano,
        rstride=1,
        cstride=1,
        linewidth=0.0,
        antialiased=False,
        shade=False,
        alpha=0.78,
    )

    xy_3d = np.linspace(-1.65, 1.65, 7)
    z_3d = np.array([-1.65, -1.10, -0.55, 0.55, 1.10, 1.65])
    x3, y3, z3 = np.meshgrid(xy_3d, xy_3d, z_3d, indexing="ij")
    ex3, ey3, ez3 = campo_adimensional(x3, y3, z3)
    mag3 = np.sqrt(ex3**2 + ey3**2 + ez3**2)
    validos = np.isfinite(mag3) & (np.sqrt(x3**2 + y3**2 + z3**2) > 0.40)
    escala = np.clip((np.log10(mag3) + 1.45) / 2.70, 0.0, 1.0)
    longitud = 0.13 + 0.24 * escala
    denom = np.where(mag3 > 0.0, mag3, 1.0)
    u3 = ex3 * longitud / denom
    v3 = ey3 * longitud / denom
    w3 = ez3 * longitud / denom
    colores_flechas = mapa_campo(norma_campo(mag3[validos]))
    ax_3d.quiver(
        x3[validos],
        y3[validos],
        z3[validos],
        u3[validos],
        v3[validos],
        w3[validos],
        color=colores_flechas,
        linewidth=0.48,
        alpha=0.82,
        arrow_length_ratio=0.32,
        normalize=False,
    )
    ax_3d.set_xlim(-1.95, 1.95)
    ax_3d.set_ylim(-1.95, 1.95)
    ax_3d.set_zlim(-1.95, 1.95)
    ax_3d.set_xticks([-1.5, 0.0, 1.5])
    ax_3d.set_yticks([-1.5, 0.0, 1.5])
    ax_3d.set_zticks([-1.5, 0.0, 1.5])
    ax_3d.set_xlabel(r"$x/L$", labelpad=4)
    ax_3d.set_ylabel(r"$y/L$", labelpad=4)
    ax_3d.set_zlabel(r"$z/L$", labelpad=2)
    ax_3d.set_box_aspect((1.0, 1.0, 0.92))
    ax_3d.view_init(elev=25, azim=-54)
    ax_3d.set_title("(c) Plano cargado y campo tridimensional", pad=9)
    ax_3d.xaxis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
    ax_3d.yaxis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
    ax_3d.zaxis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))

    barra_sigma = ScalarMappable(norm=norma_sigma, cmap=mapa_sigma)
    barra_campo = ScalarMappable(norm=norma_campo, cmap=mapa_campo)
    eje_barra_sigma = figura.add_axes([0.075, 0.045, 0.32, 0.022])
    eje_barra_campo = figura.add_axes([0.565, 0.045, 0.33, 0.022])
    cbar_sigma = figura.colorbar(barra_sigma, cax=eje_barra_sigma, orientation="horizontal")
    cbar_sigma.set_label(r"densidad $\widetilde{\sigma}=\sigma L^3/(\varepsilon_0V_0)$")
    cbar_campo = figura.colorbar(barra_campo, cax=eje_barra_campo, orientation="horizontal")
    cbar_campo.set_label(r"intensidad $|\widetilde{\mathbf{E}}|=|\mathbf{E}|L^3/V_0$")

    figura.suptitle("Condiciones de frontera sobre el plano $z=0$", y=0.985, fontsize=12.3)
    figura.subplots_adjust(left=0.055, right=0.985, bottom=0.15, top=0.91)
    figura.savefig(ruta_salida, format="svg", bbox_inches="tight", pad_inches=0.04)
    plt.close(figura)


if __name__ == "__main__":
    directorio = Path(__file__).resolve().parent
    salida = directorio / "densidad_plano_visualizacion.svg"
    comprobar_frontera()
    crear_figura(salida)
    print(f"Figura guardada en: {salida}")
