"""Visualización vectorial del cascarón dieléctrico con una carga central.

Uso:
    python visualizacion_campos_cascaron.py
    python visualizacion_campos_cascaron.py --epsilon-r 5 --radio-exterior 2.5

Exporta SVG (vectorial, sin imágenes incrustadas) y PNG de vista previa.
El modelo es electrostático, con q>0 y un dieléctrico lineal, homogéneo
e isótropo. Los campos se evalúan analíticamente sobre puntos de las
líneas integrales radiales; no se simula una dinámica microscópica.

Unidades: R1=1; E*=q/(4*pi*eps0*R1**2), D*=P*=eps0*E*.
Las flechas indican sentido; la magnitud se codifica con el color.
El número de líneas dibujadas no representa el flujo de los campos.
"""

from pathlib import Path
import argparse
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import colors, colormaps
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, Wedge
import numpy as np


def campos(r, epsilon_r=3.0, radio_exterior=2.0):
    """D/D*, E/E*, P/P*; valores laterales, no asignados a interfaces."""
    r = np.asarray(r, dtype=float)
    valido = (r > 0) & ~np.isclose(r, 1.0, atol=1e-12, rtol=0)
    valido &= ~np.isclose(r, radio_exterior, atol=1e-12, rtol=0)
    dentro = (r > 1) & (r < radio_exterior)
    with np.errstate(divide="ignore", invalid="ignore"):
        d = 1.0 / r**2
    e = d / np.where(dentro, epsilon_r, 1.0)
    p = np.where(dentro, (1.0 - 1.0 / epsilon_r) * d, 0.0)
    return tuple(np.where(valido, f, np.nan) for f in (d, e, p))


def verificar_modelo(epsilon_r, radio_exterior):
    radios = np.array([0.6, (1 + radio_exterior) / 2, radio_exterior + 0.4])
    d, e, p = campos(radios, epsilon_r, radio_exterior)
    np.testing.assert_allclose(d, e + p, rtol=1e-12, atol=1e-14)
    alpha = 1.0 - 1.0 / epsilon_r
    sigma1, sigma2 = -alpha, alpha / radio_exterior**2
    np.testing.assert_allclose(sigma1 + radio_exterior**2 * sigma2, 0, atol=1e-14)
    np.testing.assert_allclose(e / d, [1, 1 / epsilon_r, 1])
    np.testing.assert_allclose(p[[0, 2]], 0)
    r_material = np.linspace(1.001, radio_exterior - 0.001, 31)
    np.testing.assert_allclose(r_material**2 * campos(
        r_material, epsilon_r, radio_exterior)[2], alpha, atol=1e-12)
    return sigma1, sigma2


def dibujar_lineas(ax, campo, epsilon_r, radio_exterior, limite, norma, mapa):
    """Curvas integrales exactas: rayos, pues cada campo es puramente radial."""
    tramos = [(0.25, 1), (1, radio_exterior), (radio_exterior, limite)]
    angulos = np.linspace(0, 2 * np.pi, 32, endpoint=False)
    for region, (a, b) in enumerate(tramos):
        if campo == 2 and (region != 1 or epsilon_r == 1):
            continue
        r = np.linspace(a, b, 161)
        r_medio = (r[1:] + r[:-1]) / 2
        valores = campos(r_medio, epsilon_r, radio_exterior)[campo]
        for angulo in angulos:
            puntos = np.column_stack((r * np.cos(angulo), r * np.sin(angulo)))
            segmentos = np.stack((puntos[:-1], puntos[1:]), axis=1)
            lineas = LineCollection(segmentos, cmap=mapa, norm=norma,
                                    linewidths=1.20, zorder=3)
            lineas.set_array(valores)
            ax.add_collection(lineas)

    if campo == 2:
        if epsilon_r == 1:
            return
        radios_flechas = [1 + (radio_exterior - 1) * f for f in (0.25, 0.75)]
    else:
        radios_flechas = [0.63, (1 + radio_exterior) / 2,
                         radio_exterior + (limite - radio_exterior) * 0.58]
    largo = min(0.22, (radio_exterior - 1) * 0.22)
    for radio in radios_flechas:
        valor = float(campos(np.array([radio]), epsilon_r, radio_exterior)[campo][0])
        if valor <= 0:
            continue
        for angulo in angulos[::2]:
            v = np.array([np.cos(angulo), np.sin(angulo)])
            ax.annotate("", xy=(radio + largo / 2) * v,
                        xytext=(radio - largo / 2) * v,
                        arrowprops={"arrowstyle": "-|>", "mutation_scale": 11,
                                    "lw": 1.0, "color": mapa(norma(valor)),
                                    "shrinkA": 0, "shrinkB": 0}, zorder=4)


def decorar_corte(ax, radio_exterior, limite):
    ax.add_patch(Wedge((0, 0), radio_exterior, 0, 360,
                      width=radio_exterior - 1, facecolor="#ececec",
                      edgecolor="none", zorder=0))
    for radio in (1, radio_exterior):
        ax.add_patch(Circle((0, 0), radio, fill=False, edgecolor="#333333",
                            linewidth=0.9, zorder=5))
    ax.add_patch(Circle((0, 0), 0.25, facecolor="white", edgecolor="none", zorder=7))
    ax.plot(0, 0, "o", color="black", ms=4.2, zorder=8)
    ax.text(0, -0.14, r"$q$", ha="center", va="top", fontsize=15, zorder=8,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.3})
    ax.set(xlim=(-limite, limite), ylim=(-limite, limite), aspect="equal")
    ax.set_xticks([-radio_exterior, 0, radio_exterior])
    ax.set_yticks([-radio_exterior, 0, radio_exterior])
    ax.tick_params(length=3, labelsize=11)
    ax.set_xlabel(r"$x/R_1$", fontsize=13, labelpad=2)
    for espina in ax.spines.values():
        espina.set_visible(False)


def crear_figura(epsilon_r=3.0, radio_exterior=2.0):
    sigma1, sigma2 = verificar_modelo(epsilon_r, radio_exterior)
    plt.rcParams.update({
        "font.family": "DejaVu Serif", "mathtext.fontset": "dejavuserif",
        "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 13,
        "svg.fonttype": "path", "savefig.facecolor": "white",
        "axes.spines.top": False, "axes.spines.right": False,
    })
    fig = plt.figure(figsize=(11.6, 8.6), facecolor="white")
    gs = fig.add_gridspec(3, 4, height_ratios=[1, 0.065, 0.72],
                          width_ratios=[1, 1, 1, 0.045],
                          left=0.065, right=0.94, bottom=0.11, top=0.90,
                          wspace=0.23, hspace=0.41)
    axs = [fig.add_subplot(gs[0, i]) for i in range(3)]
    limite = radio_exterior * 1.48
    norma = colors.LogNorm(vmin=0.05 / (radio_exterior / 2)**2, vmax=16)
    mapa = colors.ListedColormap(colormaps["viridis"](np.linspace(0.06, 0.87, 256)))
    titulos = [r"Desplazamiento $\vec D$", r"Campo eléctrico $\vec E$",
               r"Polarización $\vec P$"]
    for i, ax in enumerate(axs):
        decorar_corte(ax, radio_exterior, limite)
        dibujar_lineas(ax, i, epsilon_r, radio_exterior, limite, norma, mapa)
        ax.set_title(titulos[i], fontsize=15, pad=12)
    axs[0].set_ylabel(r"$z/R_1$", fontsize=13, labelpad=0)
    for ax in axs[1:]:
        ax.set_yticklabels([])

    mapa_sigma = colormaps["coolwarm"]
    norma_sigma = colors.Normalize(vmin=-1, vmax=1)
    for radio, sigma in [(1, sigma1), (radio_exterior, sigma2)]:
        axs[2].add_patch(Circle((0, 0), radio, fill=False,
                               edgecolor=mapa_sigma(norma_sigma(sigma)),
                               lw=4.0, zorder=6))
    axs[2].text(0, 0.56, r"$\vec P=\vec 0$", ha="center", fontsize=12, zorder=8)
    axs[2].text(0, radio_exterior + 0.55 * (limite - radio_exterior),
                r"$\vec P=\vec 0$", ha="center", fontsize=12)

    axs[2].text(0, -(radio_exterior + 0.61 * (limite - radio_exterior)),
                r"$\rho_b=0$ en el material" + "\n" + r"$Q_{b,1}+Q_{b,2}=0$",
                ha="center", va="center", fontsize=10.5, linespacing=1.4)

    cax_sigma = fig.add_subplot(gs[0, 3])
    barra_sigma = fig.colorbar(plt.cm.ScalarMappable(norm=norma_sigma, cmap=mapa_sigma),
                               cax=cax_sigma, ticks=[-1, -0.5, 0, 0.5, 1])
    barra_sigma.set_label(r"Carga superficial $\sigma_b/\sigma_*$", fontsize=12, labelpad=10)
    barra_sigma.ax.tick_params(labelsize=10)
    barra_sigma.solids.set_rasterized(False)
    barra_sigma.solids.set_edgecolor("face")

    cax = fig.add_subplot(gs[1, :3])
    barra = fig.colorbar(plt.cm.ScalarMappable(norm=norma, cmap=mapa), cax=cax,
                         orientation="horizontal", ticks=[0.05, 0.1, 0.3, 1, 3, 10, 16])
    barra.ax.set_xticklabels(["0.05", "0.1", "0.3", "1", "3", "10", "16"])
    barra.ax.minorticks_off()
    barra.ax.tick_params(labelsize=10, length=3)
    barra.set_label(r"Magnitud relativa: $|\vec D|/D_*$, $|\vec E|/E_*$, "
                    r"$|\vec P|/P_*$ (escala logarítmica)",
                    fontsize=12, labelpad=4)
    barra.solids.set_rasterized(False)
    barra.solids.set_edgecolor("face")

    ax = fig.add_subplot(gs[2, :3])
    ax.axvspan(1, radio_exterior, color="#ececec", zorder=0)
    for radio, texto in [(1, r"$R_1$"), (radio_exterior, r"$R_2$")]:
        ax.axvline(radio, color="0.55", ls=":", lw=1)
        ax.text(radio, 1.02, texto, transform=ax.get_xaxis_transform(),
                ha="center", va="bottom", fontsize=12)
    xmax = max(3.4, radio_exterior * 1.65)
    tramos = [(0.75, 1 - 1e-7), (1 + 1e-7, radio_exterior - 1e-7),
              (radio_exterior + 1e-7, xmax)]
    estilos = [("#333333", "--", r"$D_r/D_*$"),
               ("#0072B2", "-", r"$E_r/E_*$"),
               ("#B56B00", "-.", r"$P_r/P_*$")]
    for j, (a, b) in enumerate(tramos):
        r = np.linspace(a, b, 600)
        for valores, (color, estilo, etiqueta) in zip(campos(r, epsilon_r, radio_exterior), estilos):
            ax.plot(r, valores, color=color, ls=estilo, lw=2.0,
                    label=etiqueta if j == 1 else None,
                    zorder=5 if estilo == "--" else 4)
    ax.set(xlim=(0.75, xmax), ylim=(-0.045, 1.85),
           xlabel=r"$r/R_1$", ylabel="Componente radial / escala")
    ax.tick_params(labelsize=11)
    ax.grid(axis="y", color="0.9", lw=0.6)
    ax.legend(loc="upper right", frameon=False, ncol=3, fontsize=12,
              handlelength=2.6, columnspacing=1.3)
    ax.text((1 + radio_exterior) / 2, 0.91, "Dieléctrico",
            transform=ax.get_xaxis_transform(), ha="center", fontsize=12)
    ax.text(0.98, 0.61, r"$\vec D=\varepsilon_0\vec E+\vec P$",
            transform=ax.transAxes, ha="right", fontsize=15)

    fig.suptitle(rf"Cascarón esférico: $q>0$, $\varepsilon_r={epsilon_r:g}$, "
                 rf"$R_2/R_1={radio_exterior:g}$", fontsize=17, y=0.985)
    fig.text(0.5, 0.025,
             r"$E_*=\dfrac{q}{4\pi\varepsilon_0R_1^2},\qquad "
             r"D_*=P_*=\sigma_*=\varepsilon_0E_*$",
             ha="center", va="center", fontsize=15)
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epsilon-r", type=float, default=3.0)
    parser.add_argument("--radio-exterior", type=float, default=2.0,
                        help="Radio exterior en unidades de R1.")
    parser.add_argument("--salida", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    if not np.isfinite(args.epsilon_r) or args.epsilon_r < 1:
        parser.error("Se requiere epsilon_r finita y mayor o igual a 1.")
    if not np.isfinite(args.radio_exterior) or args.radio_exterior <= 1.002:
        parser.error("Se requiere R2/R1 mayor que 1.002.")
    args.salida.mkdir(parents=True, exist_ok=True)
    fig = crear_figura(args.epsilon_r, args.radio_exterior)
    destino = args.salida / "visualizacion_campos_cascaron"
    fig.savefig(destino.with_suffix(".svg"), format="svg", bbox_inches="tight")
    fig.savefig(destino.with_suffix(".png"), dpi=200, bbox_inches="tight")
    plt.close(fig)
    raiz = ET.parse(destino.with_suffix(".svg")).getroot()
    if raiz.findall(".//{http://www.w3.org/2000/svg}image"):
        raise RuntimeError("El SVG contiene una imagen rasterizada inesperada.")
    print("Modelo comprobado: D=epsilon_0 E+P, carga ligada total nula y r^2 P constante.")
    print("SVG vectorial sin imagenes incrustadas:", destino.with_suffix(".svg"))
    print("Vista previa:", destino.with_suffix(".png"))


if __name__ == "__main__":
    main()
