"""IDEF0 corregido para el TP3C: nivel A-0 (el sistema entero) y nivel A0 (las seis actividades).

Correcciones del tutor a la parte A: las entradas entran por la izquierda, los controles por arriba,
los mecanismos por abajo y las salidas salen por la derecha; las etiquetas no llevan tiempos; las
entidades se llaman como en el modelo (publicación e ítem de moderación); se agrega la caja A-0.

Correr desde parte-c/:  python diagramas.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIG = Path(__file__).parent / "figuras"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 7, "figure.dpi": 220, "savefig.bbox": "tight", "font.family": "DejaVu Sans"})
NEGRO, GRIS, AZUL, ROJO = "#111111", "#555555", "#2f5d8a", "#b8483b"
TXT = 6.4


def camino(ax, pts, color=GRIS, ls="-", lw=0.8, punta=True):
    """Polilínea ortogonal; la última tramo lleva la punta de flecha."""
    xs, ys = zip(*pts)
    if len(pts) > 2:
        ax.plot(xs[:-1], ys[:-1], color=color, ls=ls, lw=lw, solid_capstyle="butt")
    ax.annotate("", xy=pts[-1], xytext=pts[-2],
                arrowprops=dict(arrowstyle="-|>" if punta else "-", color=color, lw=lw, ls=ls,
                                mutation_scale=7, shrinkA=0, shrinkB=0))


def texto(ax, x, y, s, ha="left", va="center", color=GRIS, size=TXT):
    ax.text(x, y, s, ha=ha, va=va, fontsize=size, color=color, linespacing=1.15)


def caja(ax, x, y, w, h, nombre, codigo, size=7.2):
    ax.add_patch(plt.Rectangle((x, y), w, h, fill=False, lw=1.1, ec=NEGRO))
    ax.text(x + w / 2, y + h / 2 + 0.5, nombre, ha="center", va="center", fontsize=size, color=NEGRO)
    ax.text(x + w - 0.6, y + 0.6, codigo, ha="right", va="bottom", fontsize=5.8, color=NEGRO)


def a_menos_0():
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    ax.set_xlim(0, 124); ax.set_ylim(0, 56); ax.axis("off")
    x, y, w, h = 22, 19, 58, 16
    caja(ax, x, y, w, h, "Contener la difusión\nde publicaciones nocivas en RedBaires", "A0", size=7.8)
    camino(ax, [(0, 27), (x, 27)]); texto(ax, 0, 29, "publicaciones nuevas", va="bottom")
    for cx, s in ((28, "variables de decisión:\nmoderadores, fricción,\ndegradación, clasificador"),
                  (51, "parámetros de la\nmuestra y de costos"),
                  (74, "escenario: volumen\ny campañas coordinadas")):
        camino(ax, [(cx, 45), (cx, y + h)]); texto(ax, cx, 46, s, ha="center", va="bottom")
    for sy, s, c in ((31, "impresiones nocivas servidas", AZUL), (27, "impresiones legítimas perdidas", AZUL),
                     (23, "publicaciones buenas bajadas", GRIS)):
        camino(ax, [(x + w, sy), (x + w + 8, sy)], color=c); texto(ax, x + w + 9, sy, s, color=c)
    for mx, s in ((28, "Centinela\n(clasificador)"), (51, "moderadores"), (74, "cuentas y canales:\nMuro, Grupos, Historias, MD")):
        camino(ax, [(mx, 9), (mx, y)]); texto(ax, mx, 8, s, ha="center", va="top")
    fig.savefig(FIG / "c1_idef0_a-0.png")
    plt.close(fig)


def a0():
    fig, ax = plt.subplots(figsize=(8.6, 5.8))
    ax.set_xlim(-4, 168); ax.set_ylim(-12, 90); ax.axis("off")
    W, H = 17, 8
    B = {"A1": (6, 70, "Publicar"), "A2": (28, 57, "Exponer"), "A3": (54, 44, "Clasificar"),
         "A4": (80, 31, "Revisar"), "A5": (106, 18, "Remover"), "A6": (132, 5, "Reenviar")}
    for k, (x, y, t) in B.items():
        caja(ax, x, y, W, H, t, k)
    R = lambda k: B[k][0] + W
    L = lambda k: B[k][0]
    T = lambda k: B[k][1] + H
    D = lambda k: B[k][1]
    cx = lambda k: B[k][0] + W / 2

    # A1 Publicar
    camino(ax, [(-4, 74), (L("A1"), 74)]); texto(ax, -4, 75, "publicación\nnueva", va="bottom")
    camino(ax, [(cx("A1"), 85), (cx("A1"), T("A1"))]); texto(ax, cx("A1"), 86, "tasa por hora y día\ny volumen del escenario", ha="center", va="bottom")
    camino(ax, [(cx("A1"), 64), (cx("A1"), D("A1"))]); texto(ax, cx("A1"), 63, "cuenta que\npublica", ha="center", va="top")
    camino(ax, [(R("A1"), 74), (25.5, 74), (25.5, 62), (L("A2"), 62)], color=NEGRO)
    texto(ax, 26.1, 73.2, "publicación,\ngeneración 0", color=NEGRO, va="top")
    # A2 Exponer
    camino(ax, [(42, 71), (42, T("A2"))]); texto(ax, 43, 71, "degradación (VD)", va="bottom")
    camino(ax, [(cx("A2"), 51), (cx("A2"), D("A2"))]); texto(ax, cx("A2"), 50, "Muro, Grupos,\nHistorias, MD", ha="center", va="top")
    camino(ax, [(R("A2"), 63), (50.5, 63)], color=AZUL); texto(ax, 51, 63, "impresiones nocivas\ny legítimas", color=AZUL)
    camino(ax, [(R("A2"), 59.5), (50, 59.5), (50, 48), (L("A3"), 48)], color=NEGRO)
    texto(ax, 50.6, 58.6, "publicación\nexpuesta", color=NEGRO, va="top")
    # A3 Clasificar
    camino(ax, [(66, 57), (66, T("A3"))]); texto(ax, 67, 57, "precisión y recall (VD)", va="bottom")
    camino(ax, [(cx("A3"), 38), (cx("A3"), D("A3"))]); texto(ax, cx("A3"), 37, "Centinela", ha="center", va="top")
    camino(ax, [(R("A3"), 50), (76, 50), (76, 35), (L("A4"), 35)], color=NEGRO)
    texto(ax, 76.6, 49.2, "ítem de\nmoderación", color=NEGRO, va="top")
    camino(ax, [(R("A3"), 46), (73, 46), (73, 9), (L("A6"), 9)], color=NEGRO)
    texto(ax, 75, 9.6, "publicación clasificada", color=NEGRO, va="bottom")
    # A4 Revisar
    camino(ax, [(cx("A4"), 48), (cx("A4"), T("A4"))]); texto(ax, cx("A4") + 1, 48, "cola FIFO", va="bottom")
    camino(ax, [(cx("A4"), 25), (cx("A4"), D("A4"))]); texto(ax, cx("A4"), 24, "moderadores (VD)", ha="center", va="top")
    camino(ax, [(R("A4"), 35), (102, 35), (102, 22), (L("A5"), 22)], color=NEGRO)
    texto(ax, 102.6, 34.2, "ítem\nrevisado", color=NEGRO, va="top")
    # A5 Remover
    camino(ax, [(cx("A5"), 34), (cx("A5"), T("A5"))]); texto(ax, cx("A5") + 1, 34.5, "probabilidad de remoción:\ntema, toxicidad, verificada", va="bottom")
    camino(ax, [(R("A5"), 25), (127, 25)], color=AZUL); texto(ax, 127.5, 25, "publicaciones\nbuenas bajadas", color=AZUL)
    camino(ax, [(R("A5"), 20), (135, 20), (135, T("A6"))], color=ROJO, ls="--")
    texto(ax, 136, 16, "fracción\nremovida", color=ROJO, size=6)
    # A6 Sortear la generación siguiente
    camino(ax, [(146, 18), (146, T("A6"))]); texto(ax, 147, 18, "fricción (VD) y\ndecaimiento δ(g)", va="bottom")
    camino(ax, [(cx("A6"), -1), (cx("A6"), D("A6"))]); texto(ax, cx("A6"), -1.6, "cuentas del frente", ha="center", va="top")
    camino(ax, [(R("A6"), 11), (157, 11)], color=NEGRO); texto(ax, 157.5, 11, "publicación\nextinguida", color=NEGRO)
    camino(ax, [(R("A6"), 7), (162, 7), (162, -9), (22, -9), (22, 59.5), (L("A2"), 59.5)], color=AZUL)
    texto(ax, 92, -8.4, "publicación, generación siguiente", color=AZUL, ha="center", va="bottom")
    fig.savefig(FIG / "c2_idef0_a0.png")
    plt.close(fig)


if __name__ == "__main__":
    a_menos_0()
    a0()
