"""Visualizaciones vectoriales de los dos ejercicios de repaso.

Uso: python repaso_imagenes_polarizacion_conductores_visualizacion.py
Genera dos SVG en la subcarpeta figuras, sin requerir una instalación LaTeX.
Las cantidades se evalúan en unidades adimensionales; no hay un solver PDE.
"""

from pathlib import Path
import argparse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from matplotlib.patches import Circle, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 13,
    "axes.titlesize": 12.5,
    "axes.labelsize": 13,
    "xtick.labelsize": 11.5,
    "ytick.labelsize": 11.5,
    "svg.fonttype": "path",  # Texto estable al convertir con Inkscape.
    "savefig.facecolor": "white",
})


def campo_plano(x, z):
    """V y E en y=0, con d=q=1 y 1/(4 pi epsilon_0)=1.

    Devuelve V~, Ex~ y Ez~. El semiespacio físico es z>0.
    """
    rmas = np.hypot(x, z - 1)
    rmenos = np.hypot(x, z + 1)
    with np.errstate(divide="ignore", invalid="ignore"):
        v = 1 / rmas - 1 / rmenos
        ex = x / rmas**3 - x / rmenos**3
        ez = (z - 1) / rmas**3 - (z + 1) / rmenos**3
    return v, ex, ez


def campo_cilindro(x, y):
    """V/(E0 R) y componentes E/E0, con x,y en unidades de R.

    En s<=R el potencial y el campo total se fijan a cero.
    """
    s2 = x*x + y*y
    denom = np.maximum(s2, 1.0)
    exterior = s2 > 1
    v = np.where(exterior, -x * (1 - 1 / denom), 0)
    ex = np.where(exterior, 1 + (x*x - y*y) / denom**2, 0)
    ey = np.where(exterior, 2*x*y / denom**2, 0)
    return v, ex, ey


def barra(fig, ax, artist, label, **kwargs):
    pad = kwargs.pop("pad", 0.035)
    cb = fig.colorbar(artist, ax=ax, fraction=0.045, pad=pad, **kwargs)
    if cb.solids is not None:
        cb.solids.set_rasterized(False)
        cb.solids.set_edgecolor("face")
    cb.set_label(label, fontsize=13)
    return cb


def contorno_sin_juntas(artist):
    """Evita líneas blancas entre polígonos al visualizar SVG o PDF."""
    artist.set_edgecolor("face")
    artist.set_linewidth(0.2)


def plano_conductor(ax):
    ax.add_patch(Rectangle((-3.3, -0.14), 6.6, 0.14,
                           facecolor="0.80", edgecolor="none", zorder=5))
    ax.axhline(0, color="0.15", lw=1.3, zorder=6)
    ax.plot(0, 1, "o", ms=7, color="#b2182b", mec="white", mew=1.2, zorder=8)
    ax.annotate("$+q$", (0, 1), xytext=(8, 8), textcoords="offset points",
                fontsize=11.5, bbox={"facecolor": "white", "edgecolor": "none",
                                   "pad": 1}, zorder=9)
    ax.set(xlim=(-3.3, 3.3), ylim=(-0.14, 4.4), xlabel="$x/d$", ylabel="$z/d$")
    ax.set_aspect("equal")


def figura_plano():
    fig, axs = plt.subplots(2, 2, figsize=(9.4, 8.6), layout="constrained")
    xx = np.linspace(-3.3, 3.3, 401)
    zz = np.linspace(0, 4.4, 321)
    x, z = np.meshgrid(xx, zz)
    v, ex, ez = campo_plano(x, z)
    excluido = np.hypot(x, z - 1) < 0.16
    vm = np.ma.masked_where(excluido, v)
    exm = np.ma.masked_where(excluido, ex)
    ezm = np.ma.masked_where(excluido, ez)

    ax = axs[0, 0]
    artist = ax.contourf(x, z, vm, levels=np.linspace(0, 3, 81),
                         cmap="magma", extend="max")
    contorno_sin_juntas(artist)
    ax.contour(x, z, vm, levels=[0.1, 0.25, 0.5, 1, 2],
               colors="white", linewidths=0.45, alpha=0.7)
    plano_conductor(ax)
    ax.set_title("(a) Potencial exacto")
    barra(fig, ax, artist, r"$\widetilde V$", ticks=[0, 1, 2, 3])

    ax = axs[0, 1]
    magnitud = np.ma.sqrt(exm**2 + ezm**2)
    lineas = ax.streamplot(xx, zz, exm, ezm, color=magnitud, cmap="viridis",
                          norm=LogNorm(0.025, 30), density=1.7,
                          linewidth=1.15, arrowsize=1.05)
    plano_conductor(ax)
    ax.set_title("(b) Líneas de campo y magnitud")
    barra(fig, ax, lineas.lines, r"$\widetilde E$",
          extend="both")

    ax = axs[1, 0]
    xy = np.linspace(-3.3, 3.3, 401)
    x, y = np.meshgrid(xy, xy)
    sigma = -(1 + x*x + y*y)**(-1.5)
    artist = ax.contourf(x, y, sigma, levels=np.linspace(-1, 0, 81),
                         cmap="RdBu_r", norm=Normalize(-1, 1))
    contorno_sin_juntas(artist)
    ax.contour(x, y, sigma, levels=[-0.8, -0.4, -0.1],
               colors="0.25", linewidths=0.5, alpha=0.65)
    ax.plot(0, 0, "+", color="0.15", ms=8)
    ax.set(title="(c) Carga superficial en el plano", xlabel="$x/d$", ylabel="$y/d$")
    ax.set_aspect("equal")
    barra(fig, ax, artist, r"$\widetilde\sigma$",
          ticks=[-1, -0.75, -0.5, -0.25, 0])

    ax = axs[1, 1]
    radio = np.geomspace(1.3, 80, 600)
    for grados, color in zip([0, 45, 75], ["#0072B2", "#D55E00", "#009E73"]):
        theta = np.deg2rad(grados)
        vexacto, _, _ = campo_plano(radio*np.sin(theta), radio*np.cos(theta))
        vdipolo = 2*np.cos(theta) / radio**2
        error = np.abs(vdipolo-vexacto) / np.abs(vexacto)
        ax.loglog(radio, error, lw=1.8, color=color,
                  label=rf"$\theta={grados}^\circ$")
    ax.set(title="(d) Aproximación dipolar", xlabel="$r/d$",
           ylabel=r"$|V_{\rm dip}-V|/|V|$", xlim=(1.3, 80))
    ax.grid(True, which="both", alpha=0.22)
    ax.legend(frameon=False, fontsize=11.5, loc="lower left")
    return fig


def figura_cilindro():
    fig = plt.figure(figsize=(9.4, 8.6), layout="constrained")
    ax_v = fig.add_subplot(2, 2, 1)
    ax_e = fig.add_subplot(2, 2, 2)
    ax_s = fig.add_subplot(2, 2, 3, projection="3d")
    ax_p = fig.add_subplot(2, 2, 4)
    xy = np.linspace(-3.2, 3.2, 401)
    x, y = np.meshgrid(xy, xy)
    v, ex, ey = campo_cilindro(x, y)
    interior = x*x + y*y <= 1

    artist = ax_v.contourf(x, y, np.ma.masked_where(interior, v),
                           levels=np.linspace(-3.2, 3.2, 81), cmap="RdBu_r")
    contorno_sin_juntas(artist)
    ax_v.contour(x, y, np.ma.masked_where(interior, v),
                 levels=[-2, -1, -0.5, 0.5, 1, 2], colors="0.2",
                 linewidths=0.5, alpha=0.55)
    ax_v.add_patch(Circle((0, 0), 1, facecolor="0.86", edgecolor="0.2", lw=1.2))
    ax_v.text(0, 0, "$V=0$", ha="center", va="center", fontsize=11.5)
    ax_v.set(title="(a) Potencial total", xlabel="$x/R$", ylabel="$y/R$",
             xlim=(-3.2, 3.2), ylim=(-3.2, 3.2), aspect="equal")
    barra(fig, ax_v, artist, "$V/(E_0R)$", ticks=[-3, -1.5, 0, 1.5, 3])

    exm = np.ma.masked_where(interior, ex)
    eym = np.ma.masked_where(interior, ey)
    magnitud = np.ma.sqrt(exm**2 + eym**2)
    lineas = ax_e.streamplot(xy, xy, exm, eym, color=magnitud,
                            cmap="viridis", norm=Normalize(0, 2),
                            density=1.6, linewidth=1.15, arrowsize=1.05)
    ax_e.add_patch(Circle((0, 0), 1, facecolor="0.86", edgecolor="0.2", lw=1.2))
    ax_e.text(0, 0, r"$\vec{E}=\vec{0}$", ha="center", va="center", fontsize=11.5)
    ax_e.set(title="(b) Líneas de campo y magnitud", xlabel="$x/R$", ylabel="$y/R$",
             xlim=(-3.2, 3.2), ylim=(-3.2, 3.2), aspect="equal")
    barra(fig, ax_e, lineas.lines, r"$|\vec{E}|/E_0$", ticks=[0, 0.5, 1, 1.5, 2])

    phi = np.linspace(0, 2*np.pi, 241)
    norma = Normalize(-1, 1)
    mapa = plt.colormaps["RdBu_r"]
    # La densidad es constante en z. Usamos caras verticales, sin tapas.
    # Una superposición angular mínima evita juntas blancas en SVG y PDF.
    margen = 0.50 * (phi[1] - phi[0])
    caras = []
    colores = []
    for a, b in zip(phi[:-1], phi[1:]):
        lo, hi = a-margen, b+margen
        caras.append([(np.cos(lo), np.sin(lo), -1.5),
                      (np.cos(hi), np.sin(hi), -1.5),
                      (np.cos(hi), np.sin(hi), 1.5),
                      (np.cos(lo), np.sin(lo), 1.5)])
        colores.append(mapa(norma(np.cos((a+b)/2))))
    superficie = Poly3DCollection(caras, facecolors=colores,
                                  edgecolors="none", linewidths=0,
                                  antialiaseds=False, zsort="average")
    ax_s.add_collection3d(superficie)
    ax_s.set(title="(c) Densidad sobre el cilindro", xlabel="$x/R$", ylabel="$y/R$",
             zlabel="$z/R$", xlim=(-1.35, 1.35), ylim=(-1.35, 1.35), zlim=(-1.6, 1.6))
    ax_s.set_xticks([-1, 0, 1])
    ax_s.set_yticks([-1, 0, 1])
    ax_s.set_zticks([-1, 0, 1])
    ax_s.set_box_aspect((1, 1, 1.2))
    ax_s.view_init(elev=20, azim=-65)
    ax_s.tick_params(labelsize=11, pad=0)
    for axis in [ax_s.xaxis, ax_s.yaxis, ax_s.zaxis]:
        axis.pane.fill = False
    barra(fig, ax_s, plt.cm.ScalarMappable(norm=norma, cmap=mapa),
          r"$\widetilde\sigma$", shrink=0.78,
          ticks=[-1, -0.5, 0, 0.5, 1], pad=0.11)

    grados = np.linspace(0, 360, 721)
    densidad = np.cos(np.deg2rad(grados))
    ax_p.fill_between(grados, 0, densidad, where=densidad>=0,
                       color=mapa(norma(0.8)), alpha=0.35, interpolate=True)
    ax_p.fill_between(grados, 0, densidad, where=densidad<=0,
                       color=mapa(norma(-0.8)), alpha=0.35, interpolate=True)
    ax_p.plot(grados, densidad, color="0.15", lw=1.8)
    ax_p.axhline(0, color="0.35", lw=0.8)
    ax_p.set(title="(d) Perfil angular de la carga", xlabel=r"$\phi$ (grados)",
             ylabel=r"$\sigma/(2\varepsilon_0E_0)$", xlim=(0, 360), ylim=(-1.1, 1.1))
    ax_p.set_xticks([0, 90, 180, 270, 360])
    ax_p.grid(alpha=0.20)
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parent / "figuras")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for nombre, crear in [("carga_plano_visualizacion", figura_plano),
                          ("cilindro_uniforme_visualizacion", figura_cilindro)]:
        fig = crear()
        destino = args.output_dir / f"{nombre}.svg"
        fig.savefig(destino, format="svg", bbox_inches="tight")
        plt.close(fig)
        print(destino)


if __name__ == "__main__":
    main()
