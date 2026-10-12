"""Diagramas del informe TP3A: IDEF0, lógica de eventos e influencias · 26/9/2026.

Correr desde parte-a/:  python diagramas.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon

FIG = Path(__file__).parent / "figuras"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 7, "figure.dpi": 220, "savefig.bbox": "tight"})
AZUL, GRIS, ROJO = "#2f5d8a", "#555555", "#b8483b"


def flecha(ax, xy1, xy2, color=GRIS, ls="-", lw=0.8, texto=None, tpos=0.5, dx=0, dy=0, ha="center",
           va="center", size=6.3):
    ax.annotate("", xy=xy2, xytext=xy1,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls, mutation_scale=7,
                                shrinkA=0, shrinkB=0))
    if texto:
        x = xy1[0] + (xy2[0] - xy1[0]) * tpos + dx
        y = xy1[1] + (xy2[1] - xy1[1]) * tpos + dy
        ax.text(x, y, texto, ha=ha, va=va, fontsize=size, color=color)


def linea(ax, pts, color=GRIS, ls="-", lw=0.8):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, ls=ls, lw=lw)


# ======================= IDEF0 =======================
def idef0():
    fig, ax = plt.subplots(figsize=(7.2, 4.9))
    ax.set_xlim(0, 116)
    ax.set_ylim(0, 74)
    ax.axis("off")
    W, H = 15, 7
    cajas = {"A1": (8, 58, "Publicar"), "A2": (30, 47, "Exponer\nel frente"), "A3": (52, 36, "Clasificar"),
             "A4": (74, 25, "Saltar de\ngeneración"), "A5": (52, 11, "Revisar"), "A6": (80, 1.5, "Remover")}
    for k, (x, y, t) in cajas.items():
        ax.add_patch(plt.Rectangle((x, y), W, H, fill=False, lw=1, ec="black"))
        ax.text(x + W / 2, y + H / 2 + 0.4, t, ha="center", va="center", fontsize=7)
        ax.text(x + W - 0.6, y + 0.5, k, ha="right", va="bottom", fontsize=5.8)
    (x1, y1, _), (x2, y2, _), (x3, y3, _) = cajas["A1"], cajas["A2"], cajas["A3"]
    (x4, y4, _), (x5, y5, _), (x6, y6, _) = cajas["A4"], cajas["A5"], cajas["A6"]
    T = 6.2
    # A1
    flecha(ax, (0, y1 + H / 2), (x1, y1 + H / 2))
    ax.text(0, y1 + H / 2 + 0.8, "rumor\nnuevo", fontsize=T, va="bottom")
    flecha(ax, (x1 + W / 2, y1 + H + 5), (x1 + W / 2, y1 + H))
    ax.text(x1 + W / 2, y1 + H + 5.6, "tasa según hora y día", fontsize=T, ha="center", va="bottom", color=GRIS)
    flecha(ax, (x1 + W / 2, y1 - 5), (x1 + W / 2, y1))
    ax.text(x1 + W / 2, y1 - 5.6, "cuenta que publica", fontsize=T, ha="center", va="top", color=GRIS)
    linea(ax, [(x1 + W, y1 + H / 2), (x2 + 3, y1 + H / 2)])
    flecha(ax, (x2 + 3, y1 + H / 2), (x2 + 3, y2 + H))
    ax.text(x1 + W + 0.8, y1 + H / 2 + 0.6, "publicación\n(g = 0)", fontsize=T, va="bottom")
    # A2
    flecha(ax, (x2 + W - 3, y2 + H + 5), (x2 + W - 3, y2 + H))
    ax.text(x2 + W - 2.2, y2 + H + 2.6, "degradación (VD)", fontsize=T, va="center", color=GRIS)
    flecha(ax, (x2 + W / 2, y2 - 5), (x2 + W / 2, y2))
    ax.text(x2 + W / 2, y2 - 5.6, "Muro · Grupos ·\nHistorias · MD", fontsize=T, ha="center", va="top", color=GRIS)
    flecha(ax, (x2 + W, y2 + H - 1.2), (x2 + W + 9, y2 + H - 1.2), color=AZUL)
    ax.text(x2 + W + 9.6, y2 + H - 1.2, "impresiones nocivas\ny legítimas", fontsize=T, va="center", color=AZUL)
    linea(ax, [(x2 + W, y2 + 1.5), (x3 + 3, y2 + 1.5)])
    flecha(ax, (x3 + 3, y2 + 1.5), (x3 + 3, y3 + H))
    ax.text(x3 + 3.8, y2 + 0.8, "frente", fontsize=T, va="top")
    # A3
    flecha(ax, (x3 + W - 2.5, y3 + H + 4), (x3 + W - 2.5, y3 + H))
    ax.text(x3 + W - 1.5, y3 + H + 2.2, "precisión y recall\n(VD clasificador)", fontsize=T, va="center", color=GRIS)
    flecha(ax, (x3 + W / 2, y3 - 5), (x3 + W / 2, y3))
    ax.text(x3 + W / 2, y3 - 5.6, "Centinela", fontsize=T, ha="center", va="top", color=GRIS)
    linea(ax, [(x3 + W, y3 + H / 2), (x4 + 3, y3 + H / 2)])
    flecha(ax, (x4 + 3, y3 + H / 2), (x4 + 3, y4 + H))
    ax.text(x3 + W + 0.8, y3 + H / 2 + 0.6, "frente", fontsize=T, va="bottom")
    linea(ax, [(x3 + 2, y3), (x3 + 2, y3 - 2.5), (x5 - 5, y3 - 2.5), (x5 - 5, y5 + H / 2)])
    flecha(ax, (x5 - 5, y5 + H / 2), (x5, y5 + H / 2))
    ax.text(x5 - 5.8, y5 + H + 5, "ítem de\nmoderación\n(k marcados),\n90 min después", fontsize=T, ha="right",
            va="center")
    # A4
    flecha(ax, (x4 + W - 2.5, y4 + H + 4), (x4 + W - 2.5, y4 + H))
    ax.text(x4 + W - 1.5, y4 + H + 2.4, "límite de reenvíos (VD)\ndecaimiento δ(g)", fontsize=T, va="center",
            color=GRIS)
    flecha(ax, (x4 + W / 2, y4 - 4), (x4 + W / 2, y4))
    ax.text(x4 + W / 2 - 1, y4 - 4.4, "cuentas del frente", fontsize=T, ha="center", va="top", color=GRIS)
    flecha(ax, (x4 + W, y4 + 2), (x4 + W + 9, y4 + 2))
    ax.text(x4 + W + 9.6, y4 + 2, "publicación\nextinguida", fontsize=T, va="center")
    linea(ax, [(x4 + W, y4 + H - 1.5), (x4 + W + 5, y4 + H - 1.5), (x4 + W + 5, 69), (x2 + 7, 69)], color=AZUL)
    flecha(ax, (x2 + 7, 69), (x2 + 7, y2 + H), color=AZUL)
    ax.text(x4 + W + 5.8, 50, "frente g + 1,\ndespués de la\ndemora entre\ngeneraciones", fontsize=T,
            color=AZUL, va="center")
    # A5
    flecha(ax, (x5 + W / 2, y5 + H + 4), (x5 + W / 2, y5 + H))
    ax.text(x5 + W / 2, y5 + H + 4.5, "FIFO o prioridad", fontsize=T, ha="center", va="bottom", color=GRIS)
    flecha(ax, (x5 + W / 2, y5 - 5), (x5 + W / 2, y5))
    ax.text(x5 + W / 2, y5 - 5.5, "moderadores (c, VD)", fontsize=T, ha="center", va="top", color=GRIS)
    linea(ax, [(x5 + W, y5 + H / 2), (x6 - 5, y5 + H / 2), (x6 - 5, y6 + H / 2)])
    flecha(ax, (x6 - 5, y6 + H / 2), (x6, y6 + H / 2))
    ax.text(x5 + W + 0.8, y5 + H / 2 - 0.6, "decisión", fontsize=T, va="top")
    # A6
    flecha(ax, (x6 + 3, y6 + H + 4), (x6 + 3, y6 + H))
    ax.text(x6 + 3.8, y6 + H + 2.6, "p de remoción: tema,\ntoxicidad, verificada", fontsize=T, va="center",
            color=GRIS)
    flecha(ax, (x6 + W, y6 + 1.8), (x6 + W + 6, y6 + 1.8), color=AZUL)
    ax.text(x6 + W + 6.6, y6 + 1.8, "publicaciones\nbuenas bajadas", fontsize=T, va="center", color=AZUL)
    linea(ax, [(x6 + W, y6 + H - 1.5), (x6 + W + 8.5, y6 + H - 1.5), (x6 + W + 8.5, y4 - 2), (x4 + W - 2, y4 - 2)],
          color=ROJO, ls="--")
    flecha(ax, (x4 + W - 2, y4 - 2), (x4 + W - 2, y4), color=ROJO, ls="--")
    ax.text(x6 + W + 9.3, y6 + H + 6.5, "fracción\nremovida", fontsize=T, color=ROJO, va="center")
    fig.savefig(FIG / "d1_idef0.png")


# ======================= lógica de eventos =======================
FS = 5.8
LH = 1.55  # alto de una línea, en unidades del eje


def alto(t, dec=False):
    n = t.count("\n") + 1
    return n * LH + (3.2 if dec else 1.4)


def caja(ax, x, ytop, t, w=23, color="black", fc="white", rounded=False):
    h = alto(t)
    st = "round,pad=0.2" if rounded else "square,pad=0"
    ax.add_patch(FancyBboxPatch((x - w / 2, ytop - h), w, h, boxstyle=st, fc=fc, ec=color, lw=0.8))
    ax.text(x, ytop - h / 2, t, ha="center", va="center", fontsize=FS, linespacing=1.15)
    return ytop - h


def rombo(ax, x, ytop, t, w=23):
    h = alto(t, dec=True)
    y = ytop - h / 2
    ax.add_patch(Polygon([(x, ytop), (x + w / 2, y), (x, ytop - h), (x - w / 2, y)], closed=True, fc="white",
                         ec="black", lw=0.8))
    ax.text(x, y, t, ha="center", va="center", fontsize=FS, linespacing=1.1)
    return ytop - h, y


def etq(ax, x, y, t, ha="left", color=GRIS):
    ax.text(x, y, t, fontsize=FS - 0.3, ha=ha, va="center", color=color)


def logica():
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(15, 88)
    ax.axis("off")
    G = 2.6
    c1, c2, c3, c4 = 12.5, 37.5, 62.5, 87.5
    top = 87
    for x, t in [(c1, "Publicar (exógeno)"), (c2, "Saltar de generación"), (c3, "Ítem llega a la bandeja"),
                 (c4, "Fin de revisión")]:
        caja(ax, x, top, t, fc="#e8eef5", color=AZUL, rounded=True)
    y0 = top - alto("x") - G

    def seq(x, y, textos):
        for t in textos:
            flecha(ax, (x, y + G), (x, y))
            y = caja(ax, x, y, t) - G
        return y

    # --- Publicar
    seq(c1, y0, ["crear la publicación:\ntema, toxicidad, coordinada", "sortear el tipo de cuenta\nde la semilla",
                 "frente = 1 cuenta · g = 0", "programar el próximo publicar\n(exponencial, λ según la hora)",
                 "ejecutar ya «saltar\nde generación»"])
    # --- Saltar de generación
    y = seq(c2, y0, ["impresiones del frente =\nΣ 0,15 × seguidores\n(× factor si está degradada)",
                     "sumar a nocivas o a\nlegítimas según el tema",
                     "Centinela: k marcados\n~ Binomial(n, p según\ntema y toxicidad)"])
    flecha(ax, (c2, y + G), (c2, y))
    yb, ym = rombo(ax, c2, y, "¿k > 0?")
    flecha(ax, (c2 + 11.5, ym), (c2 + 15, ym))
    etq(ax, c2 + 12, ym + 1.8, "sí: programar «ítem llega")
    etq(ax, c2 + 15.5, ym, "a la bandeja»")
    etq(ax, c2 + 12, ym - 1.8, "en t + 90 min")
    etq(ax, c2 + 1, yb - 1.1, "no, o después del sí")
    y = seq(c2, yb - G, ["hijos N ~ Poisson(Λ)\nΛ = Σ nᵢ Rᵢ δ(g)\n× (1 − reducción si ≥ umbral)\n× (1 − fracción removida)"])
    flecha(ax, (c2, y + G), (c2, y))
    yb, ym = rombo(ax, c2, y, "¿N = 0?")
    linea(ax, [(c2 - 11.5, ym), (c1, ym)])
    etq(ax, c2 - 12, ym + 1.4, "sí", ha="right")
    flecha(ax, (c1, ym), (c1, ym - 2))
    caja(ax, c1, ym - 2, "la publicación se extingue:\nregistrar tamaño,\nprofundidad e impresiones", color=ROJO)
    etq(ax, c2 + 1, yb - 1.1, "no")
    seq(c2, yb - G, ["repartir N en tipos de cuenta\n(multinomial) · g ← g + 1",
                     "programar el próximo salto:\nt + demora entre generaciones"])
    # --- Ítem llega a la bandeja
    flecha(ax, (c3, y0 + G), (c3, y0))
    yb, ym = rombo(ax, c3, y0, "¿hay un\nmoderador libre?")
    etq(ax, c3 + 1, yb - 1.1, "no")
    y = seq(c3, yb - G, ["entrar a la cola\n(FIFO, o prioridad\nen el escenario)"])
    linea(ax, [(c3 + 11.5, ym), (c3 + 11.9, ym), (c3 + 11.9, y + 0.8), (c3, y + 0.8)])
    etq(ax, c3 + 11.9, ym + 1.4, "sí", ha="right")
    flecha(ax, (c3, y + 0.8), (c3, y - 0.6))
    y_ocupar = caja(ax, c3, y - 0.6, "ocupar al moderador y\nprogramar el fin de revisión:\nt + Erlang(k, 20 s)")
    # --- Fin de revisión
    y = seq(c4, y0, ["para cada uno de los k:\nremover con p según tema,\ntoxicidad y verificada",
                     "fracción removida de la\npublicación += removidos / n"])
    flecha(ax, (c4, y + G), (c4, y))
    yb, ym = rombo(ax, c4, y, "¿removió contenido\nlegítimo?")
    etq(ax, c4 + 1, yb - 1.1, "sí")
    y = caja(ax, c4, yb - G, "publicación buena bajada:\nse pierden sus impresiones\nfuturas", color=AZUL)
    flecha(ax, (c4, yb), (c4, yb - G))
    linea(ax, [(c4 + 11.5, ym), (c4 + 11.9, ym), (c4 + 11.9, y - 1.3), (c4, y - 1.3)])
    etq(ax, c4 + 11.9, ym + 1.4, "no", ha="right")
    flecha(ax, (c4, y), (c4, y - G))
    yb, ym = rombo(ax, c4, y - G, "¿la cola\nestá vacía?")
    etq(ax, c4 + 1, yb - 1.1, "sí")
    flecha(ax, (c4, yb), (c4, yb - G))
    caja(ax, c4, yb - G, "liberar al moderador")
    flecha(ax, (c4 - 11.5, ym), (c3 + 11.5, ym))
    etq(ax, c3 + 12.3, ym + 1.4, "no")
    caja(ax, c3, ym + alto("a\nb") / 2, "tomar el siguiente ítem y\nprogramar su fin de revisión")
    fig.savefig(FIG / "d2_eventos.png")


# ======================= influencias =======================
def influencias():
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 50)
    ax.axis("off")
    nodos = {
        "hora": (8, 46, "hora del día y\ndía de la semana"), "tasa": (8, 32, "tasa de publicar"),
        "tipo": (27, 46, "tipo de cuenta"), "seg": (27, 32, "seguidores"), "imp": (27, 18, "impresiones\ndel evento"),
        "gen": (46, 46, "generación g"), "R": (46, 32, "hijos por\nevento (R)"), "sup": (46, 18, "superficie"),
        "c2": (65, 46, "campaña\ncoordinada"), "nueva": (65, 32, "cuentas nuevas\nen 2 horas"),
        "det": (65, 18, "detección de\ncoordinada"),
        "tema": (84, 46, "tema"), "marca": (84, 32, "probabilidad\nde marca"), "k": (84, 18, "ítems marcados k"),
        "rev": (84, 4, "tiempo de\nrevisión"),
        "tox": (102, 46, "toxicidad"), "rem": (102, 18, "probabilidad\nde remoción"), "ver": (102, 4, "verificada"),
    }
    for k, (x, y, t) in nodos.items():
        ax.add_patch(Ellipse((x, y), 16, 7.4, fc="#e8eef5", ec=AZUL, lw=0.8))
        ax.text(x, y, t, ha="center", va="center", fontsize=6)

    def ar(a, b, c=GRIS):
        (x1, y1, _), (x2, y2, _) = nodos[a], nodos[b]
        import math
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        # recortar en el borde de las elipses (aprox.)
        def off(dx, dy):
            import math
            t = 1 / math.sqrt((dx / 8) ** 2 + (dy / 3.7) ** 2)
            return dx * t, dy * t
        ox, oy = off(dx, dy)
        flecha(ax, (x1 + ox, y1 + oy), (x2 - ox, y2 - oy), color=c)

    for a, b in [("hora", "tasa"), ("tipo", "seg"), ("seg", "imp"), ("tipo", "R"), ("gen", "R"), ("sup", "R"),
                 ("c2", "R"), ("c2", "nueva"), ("nueva", "det"), ("tema", "marca"), ("tox", "marca"),
                 ("tox", "rem"), ("tema", "rem"), ("ver", "rem"), ("marca", "k"), ("k", "rev")]:
        ar(a, b)
    fig.savefig(FIG / "d3_influencias.png")


idef0()
logica()
influencias()
