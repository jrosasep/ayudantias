"""Visualizacion numerica del anillo con lambda(varphi)=lambda_0 cos(varphi).

El SVG vectorial usa dos escalas cromaticas independientes: una divergente para
la densidad lineal y otra secuencial para la magnitud del campo electrico. Los
tres paneles comparten esas convenciones para facilitar la comparacion.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm, Normalize
from matplotlib.cm import ScalarMappable


def campo_adimensional(
    x: np.ndarray,
    z: np.ndarray,
    numero_angulos: int = 960,
) -> tuple[np.ndarray, np.ndarray]:
    """Calcula las componentes (Ex, Ez) de E~ en el plano y=0.

    Se usa R=1 y

        E~ = (4*pi*epsilon_0*R/lambda_0) E

    de modo que la integral numerica es completamente adimensional.
    """

    ex = np.zeros_like(x, dtype=float)
    ez = np.zeros_like(z, dtype=float)
    dvarphi = 2.0 * np.pi / numero_angulos

    # Los puntos medios evitan evaluar exactamente sobre las intersecciones
    # singulares del anillo con el plano y=0.
    varphi = (np.arange(numero_angulos) + 0.5) * dvarphi
    for angulo in varphi:
        coseno = np.cos(angulo)
        seno = np.sin(angulo)
        distancia_cuadrada = (x - coseno) ** 2 + seno**2 + z**2
        denominador = distancia_cuadrada**1.5
        ex += coseno * (x - coseno) * dvarphi / denominador
        ez += coseno * z * dvarphi / denominador

    return ex, ez


def campo_adimensional_3d(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    numero_angulos: int = 960,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calcula las tres componentes de E~ en una malla tridimensional."""

    ex = np.zeros_like(x, dtype=float)
    ey = np.zeros_like(y, dtype=float)
    ez = np.zeros_like(z, dtype=float)
    dvarphi = 2.0 * np.pi / numero_angulos
    varphi = (np.arange(numero_angulos) + 0.5) * dvarphi

    for angulo in varphi:
        coseno = np.cos(angulo)
        seno = np.sin(angulo)
        dx = x - coseno
        dy = y - seno
        distancia_cuadrada = dx**2 + dy**2 + z**2
        denominador = distancia_cuadrada**1.5
        ex += coseno * dx * dvarphi / denominador
        ey += coseno * dy * dvarphi / denominador
        ez += coseno * z * dvarphi / denominador

    return ex, ey, ez


def comprobar_resultado_sobre_el_eje() -> None:
    """Compara la integral numerica con el resultado analitico sobre x=0."""

    z = np.linspace(-2.0, 2.0, 17)
    x = np.zeros_like(z)
    ex_numerico, ez_numerico = campo_adimensional(x, z, numero_angulos=4096)
    ex_analitico = -np.pi / (1.0 + z**2) ** 1.5

    error_ex = float(np.max(np.abs(ex_numerico - ex_analitico)))
    error_ez = float(np.max(np.abs(ez_numerico)))
    if error_ex > 2.0e-4 or error_ez > 2.0e-12:
        raise RuntimeError(
            "La comprobacion numerica del campo sobre el eje no fue satisfactoria: "
            f"error Ex={error_ex:.3e}, error Ez={error_ez:.3e}."
        )

    print(
        "Comprobacion sobre el eje superada: "
        f"max|Ex_num-Ex_exacta|={error_ex:.3e}, max|Ez|={error_ez:.3e}"
    )


def crear_figura(ruta_salida: Path) -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "mathtext.fontset": "stix",
            "font.size": 11.4,
            "axes.titlesize": 11.8,
            "axes.labelsize": 10.8,
            "legend.fontsize": 9.2,
            "figure.dpi": 140,
            "savefig.dpi": 220,
        }
    )

    figura = plt.figure(figsize=(10.4, 6.35))
    rejilla = figura.add_gridspec(
        2,
        2,
        width_ratios=[0.86, 1.34],
        height_ratios=[1.0, 1.0],
        wspace=0.16,
        hspace=0.38,
    )
    ax_densidad = figura.add_subplot(rejilla[0, 0])
    ax_campo = figura.add_subplot(rejilla[1, 0])
    ax_campo_3d = figura.add_subplot(rejilla[:, 1], projection="3d")

    # ------------------------------------------------------------------
    # Panel (a): densidad lineal sobre el anillo.
    # ------------------------------------------------------------------
    varphi_continuo = np.linspace(0.0, 2.0 * np.pi, 720)
    ax_densidad.plot(
        np.cos(varphi_continuo),
        np.sin(varphi_continuo),
        color="0.65",
        linewidth=1.1,
        zorder=1,
    )

    mapa_densidad = plt.get_cmap("coolwarm")
    norma_densidad = Normalize(vmin=-1.0, vmax=1.0)
    mapa_campo = plt.get_cmap("viridis")
    norma_campo = LogNorm(vmin=0.08, vmax=25.0)

    varphi_muestras = np.linspace(0.0, 2.0 * np.pi, 144, endpoint=False)
    x_anillo = np.cos(varphi_muestras)
    y_anillo = np.sin(varphi_muestras)
    densidad = np.cos(varphi_muestras)
    ax_densidad.scatter(
        x_anillo,
        y_anillo,
        s=39,
        c=densidad,
        cmap=mapa_densidad,
        norm=norma_densidad,
        edgecolors="none",
        zorder=3,
    )

    ax_densidad.axhline(0.0, color="0.72", linewidth=0.7, zorder=0)
    ax_densidad.axvline(0.0, color="0.72", linewidth=0.7, zorder=0)
    ax_densidad.annotate(
        "",
        xy=(1.42, 0.0),
        xytext=(-1.42, 0.0),
        arrowprops={"arrowstyle": "->", "color": "black", "linewidth": 0.85},
    )
    ax_densidad.annotate(
        "",
        xy=(0.0, 1.42),
        xytext=(0.0, -1.42),
        arrowprops={"arrowstyle": "->", "color": "black", "linewidth": 0.85},
    )
    ax_densidad.text(1.45, -0.10, r"$x$", ha="left", va="top")
    ax_densidad.text(0.07, 1.43, r"$y$", ha="left", va="bottom")
    ax_densidad.text(0.43, 0.35, r"$\lambda>0$", ha="center", color="#8b0000")
    ax_densidad.text(-0.43, -0.35, r"$\lambda<0$", ha="center", color="#003c8f")
    ax_densidad.text(
        0.0,
        -1.38,
        r"$\lambda(\varphi')/\lambda_0=\cos\varphi'$",
        ha="center",
        va="top",
    )

    ax_densidad.set_aspect("equal")
    ax_densidad.set_xlim(-1.60, 1.60)
    ax_densidad.set_ylim(-1.56, 1.60)
    ax_densidad.set_xticks([])
    ax_densidad.set_yticks([])
    for borde in ax_densidad.spines.values():
        borde.set_visible(False)
    ax_densidad.set_title("(a) Densidad lineal sobre el anillo", pad=5)

    # ------------------------------------------------------------------
    # Panel (b): campo electrico en el plano meridiano y=0.
    # ------------------------------------------------------------------
    coordenadas = np.linspace(-2.35, 2.35, 169)
    x, z = np.meshgrid(coordenadas, coordenadas)
    ex, ez = campo_adimensional(x, z)
    magnitud = np.hypot(ex, ez)

    # En este plano el anillo corta en (x/R,z/R)=(+/-1,0). Se enmascara una
    # pequena vecindad de cada interseccion para evitar las singularidades.
    distancia_positiva = np.hypot(x - 1.0, z)
    distancia_negativa = np.hypot(x + 1.0, z)
    mascara = np.minimum(distancia_positiva, distancia_negativa) < 0.135

    ex_m = np.ma.array(ex, mask=mascara)
    ez_m = np.ma.array(ez, mask=mascara)
    magnitud_m = np.ma.array(magnitud, mask=mascara)

    ax_campo.streamplot(
        coordenadas,
        coordenadas,
        ex_m,
        ez_m,
        density=1.24,
        color=magnitud_m,
        cmap=mapa_campo,
        norm=norma_campo,
        linewidth=0.82,
        arrowsize=0.82,
        arrowstyle="->",
        broken_streamlines=True,
        maxlength=5.0,
        zorder=2,
    )

    ax_campo.axhline(0.0, color="0.55", linewidth=0.65, zorder=1)
    ax_campo.axvline(0.0, color="0.55", linewidth=0.65, zorder=1)
    ax_campo.scatter(
        [1.0, -1.0], [0.0, 0.0], s=94, c=[1.0, -1.0],
        cmap=mapa_densidad, norm=norma_densidad, edgecolor="black", zorder=5
    )
    ax_campo.text(1.0, 0.0, "+", color="white", ha="center", va="center", zorder=6)
    ax_campo.text(-1.0, 0.0, "-", color="white", ha="center", va="center", zorder=6)

    ax_campo.annotate(
        r"en $x=0$: $\widetilde{\mathbf{E}}\parallel-\hat{\mathbf{x}}$",
        xy=(0.0, 1.10),
        xytext=(-0.68, 1.92),
        arrowprops={"arrowstyle": "->", "linewidth": 0.75, "color": "0.25"},
        ha="center",
        va="center",
        fontsize=9.2,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.88, "pad": 1.5},
    )
    ax_campo.text(
        0.98,
        0.02,
        "flechas: dirección\ncolor: magnitud",
        transform=ax_campo.transAxes,
        ha="right",
        va="bottom",
        fontsize=8.8,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.88, "pad": 2.0},
    )
    ax_campo.set_xlabel(r"$x/R$")
    ax_campo.set_ylabel(r"$z/R$")
    ax_campo.set_xlim(-2.35, 2.35)
    ax_campo.set_ylim(-2.35, 2.35)
    ax_campo.set_aspect("equal")
    ax_campo.set_title(r"(b) Campo eléctrico en el plano $y=0$", pad=5)
    ax_campo.tick_params(direction="in", top=True, right=True, length=3.5)

    # ------------------------------------------------------------------
    # Panel (c): campo vectorial tridimensional.
    # ------------------------------------------------------------------
    # Ocho muestras por dirección producen una nube de hasta 8^3 vectores.
    # La malla anterior usaba 6^3 puntos; esta versión hace visible la
    # estructura espacial del campo sin convertir el panel en una mancha.
    coordenadas_3d = np.linspace(-1.8, 1.8, 8)
    x_3d, y_3d, z_3d = np.meshgrid(
        coordenadas_3d,
        coordenadas_3d,
        coordenadas_3d,
        indexing="ij",
    )
    ex_3d, ey_3d, ez_3d = campo_adimensional_3d(x_3d, y_3d, z_3d)
    magnitud_3d = np.sqrt(ex_3d**2 + ey_3d**2 + ez_3d**2)

    # La distancia tubular al anillo permite retirar los puntos demasiado
    # cercanos a la singularidad de la distribución lineal ideal.
    distancia_al_anillo = np.sqrt(
        (np.hypot(x_3d, y_3d) - 1.0) ** 2 + z_3d**2
    )
    validos = (distancia_al_anillo > 0.31) & np.isfinite(magnitud_3d)

    log_3d = np.log10(magnitud_3d[validos])
    minimo_3d, maximo_3d = np.percentile(log_3d, [10.0, 94.0])
    escala_3d = np.clip(
        (np.log10(magnitud_3d) - minimo_3d) / (maximo_3d - minimo_3d),
        0.0,
        1.0,
    )
    # Al aumentar el número de flechas se acorta cada una y se afina su trazo
    # para conservar separaciones legibles en la proyección tridimensional.
    longitud_3d = 0.14 + 0.25 * escala_3d
    denominador_3d = np.where(magnitud_3d > 0.0, magnitud_3d, 1.0)
    u_3d = ex_3d * longitud_3d / denominador_3d
    v_3d = ey_3d * longitud_3d / denominador_3d
    w_3d = ez_3d * longitud_3d / denominador_3d

    colores_campo_3d = mapa_campo(norma_campo(magnitud_3d[validos]))
    ax_campo_3d.quiver(
        x_3d[validos],
        y_3d[validos],
        z_3d[validos],
        u_3d[validos],
        v_3d[validos],
        w_3d[validos],
        color=colores_campo_3d,
        linewidth=0.43,
        alpha=0.68,
        arrow_length_ratio=0.32,
        normalize=False,
    )

    # El anillo 3D conserva la misma escala cromatica del panel (a).
    varphi_3d = np.linspace(0.0, 2.0 * np.pi, 360)
    ax_campo_3d.plot(
        np.cos(varphi_3d),
        np.sin(varphi_3d),
        np.zeros_like(varphi_3d),
        color="0.55",
        linewidth=1.0,
        zorder=4,
    )
    varphi_cargas = np.linspace(0.0, 2.0 * np.pi, 72, endpoint=False)
    densidad_3d = np.cos(varphi_cargas)
    ax_campo_3d.scatter(
        np.cos(varphi_cargas),
        np.sin(varphi_cargas),
        np.zeros_like(varphi_cargas),
        s=25,
        c=densidad_3d,
        cmap=mapa_densidad,
        norm=norma_densidad,
        edgecolors="none",
        depthshade=False,
        zorder=6,
    )

    ax_campo_3d.set_xlim(-2.08, 2.08)
    ax_campo_3d.set_ylim(-2.08, 2.08)
    ax_campo_3d.set_zlim(-2.08, 2.08)
    ax_campo_3d.set_xticks([-2, 0, 2])
    ax_campo_3d.set_yticks([-2, 0, 2])
    ax_campo_3d.set_zticks([-2, 0, 2])
    ax_campo_3d.set_xlabel(r"$x/R$", labelpad=4)
    ax_campo_3d.set_ylabel(r"$y/R$", labelpad=4)
    ax_campo_3d.set_zlabel(r"$z/R$", labelpad=2)
    ax_campo_3d.set_box_aspect((1.0, 1.0, 0.92))
    ax_campo_3d.view_init(elev=25, azim=-54)
    ax_campo_3d.set_title("(c) Campo vectorial tridimensional", pad=10)
    ax_campo_3d.grid(True, color="0.85", linewidth=0.45)
    ax_campo_3d.xaxis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
    ax_campo_3d.yaxis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
    ax_campo_3d.zaxis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
    ax_campo_3d.text2D(
        0.50,
        0.015,
        "flechas: dirección; color: magnitud",
        transform=ax_campo_3d.transAxes,
        ha="center",
        va="bottom",
        fontsize=9.0,
    )

    figura.suptitle(
        r"Anillo con densidad $\lambda(\varphi')=\lambda_0\cos\varphi'$",
        y=0.985,
        fontsize=12.2,
    )
    # Barras comunes: la primera se aplica al anillo de (a) y (c); la segunda,
    # al campo de (b) y (c).
    barra_densidad = ScalarMappable(norm=norma_densidad, cmap=mapa_densidad)
    barra_campo = ScalarMappable(norm=norma_campo, cmap=mapa_campo)
    eje_barra_densidad = figura.add_axes([0.075, 0.045, 0.32, 0.022])
    eje_barra_campo = figura.add_axes([0.565, 0.045, 0.33, 0.022])
    cbar_densidad = figura.colorbar(barra_densidad, cax=eje_barra_densidad, orientation="horizontal")
    cbar_densidad.set_label(r"densidad lineal $\lambda/\lambda_0$")
    cbar_densidad.set_ticks([-1.0, 0.0, 1.0])
    cbar_campo = figura.colorbar(barra_campo, cax=eje_barra_campo, orientation="horizontal")
    cbar_campo.set_label(r"intensidad del campo $|\widetilde{\mathbf{E}}|$")

    figura.subplots_adjust(left=0.045, right=0.985, bottom=0.15, top=0.91)
    figura.savefig(ruta_salida, format="svg", bbox_inches="tight", pad_inches=0.04)
    plt.close(figura)


if __name__ == "__main__":
    directorio = Path(__file__).resolve().parent
    salida = directorio / "campo_y_densidad_anillo_matplotlib.svg"
    comprobar_resultado_sobre_el_eje()
    crear_figura(salida)
    print(f"Figura guardada en: {salida}")
