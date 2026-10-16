"""Figuras del informe de la parte B · 16/10/2026.

b1_bloques.png: el flujo del simulador dibujado con los bloques de AnyLogic que usamos en clase.
b2_dia.png, b3_cola_stress.png: los gráficos del notebook, sacados de las salidas ya calculadas.

Correr desde parte-b/:  python figuras.py simulador.ipynb
"""
import base64
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

AQUI = Path(__file__).parent
FIG = AQUI / "figuras"
FIG.mkdir(exist_ok=True)


def caja(ax, x, y, texto, bloque, color):
    ax.add_patch(FancyBboxPatch((x - 0.82, y - 0.42), 1.64, 0.84, boxstyle="round,pad=0.04",
                                fc=color, ec="#444444", lw=0.9))
    ax.text(x, y + 0.1, texto, ha="center", va="center", fontsize=8.2)
    ax.text(x, y - 0.27, bloque, ha="center", va="center", fontsize=7.2, style="italic", color="#555555")


def flecha(ax, a, b, color="#333333", estilo="-", curva=0.0, texto=None, dx=0.0, dy=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=10, color=color, lw=1.0,
                                 linestyle=estilo, connectionstyle=f"arc3,rad={curva}"))
    if texto:
        ax.text((a[0] + b[0]) / 2 + dx, (a[1] + b[1]) / 2 + dy, texto, ha="center", fontsize=7.2, color=color)


def bloques():
    fig, ax = plt.subplots(figsize=(10, 3.6))
    azul, verde, gris = "#dbe8f6", "#e2f0d9", "#eeeeee"
    arriba, abajo = 2.2, 0.0
    caja(ax, 0, arriba, "publicar\ntasa por hora", "Source", gris)
    caja(ax, 2, arriba, "exponer el frente\n0,15 × seguidores", "Delay 0 · Statistics", azul)
    caja(ax, 4, arriba, "Centinela marca k\nbinomial", "SelectOutput", azul)
    caja(ax, 6, arriba, "frente siguiente\nPoisson de media Λ", "función", azul)
    caja(ax, 8, arriba, "demora entre gen.\ngamma (0,55; 128)", "Delay", azul)
    caja(ax, 10, arriba, "frente vacío:\nla publicación muere", "Sink", gris)
    caja(ax, 4, abajo, "piso de latencia\n90 min fijos", "Delay", verde)
    caja(ax, 6, abajo, "bandeja FIFO\nlargo = VE cola", "Queue", verde)
    caja(ax, 8, abajo, "revisión Erlang\n(k fases de 20 s)", "Service + ResourcePool (c)", verde)
    caja(ax, 10, abajo, "remoción\nbinomial (k, p)", "Sink", gris)
    for x in (0, 2, 4):
        flecha(ax, (x + 0.86, arriba), (x + 1.14, arriba))
    flecha(ax, (6.86, arriba), (7.14, arriba))
    flecha(ax, (6.3, arriba + 0.46), (9.7, arriba + 0.46), curva=-0.25, texto="sin hijos", dy=0.62)
    flecha(ax, (8, arriba + 0.46), (2, arriba + 0.46), curva=0.3, texto="con hijos: saltar de generación, g + 1", dy=1.0)
    flecha(ax, (4, arriba - 0.46), (4, abajo + 0.46), texto="si k > 0, nace un ítem", dx=0.95)
    flecha(ax, (4.86, abajo), (5.14, abajo))
    flecha(ax, (6.86, abajo), (7.14, abajo))
    flecha(ax, (8.86, abajo), (9.14, abajo))
    flecha(ax, (9.6, abajo + 0.46), (6.5, arriba - 0.46), color="#c0392b", estilo="--", curva=0.15,
           texto="fracción removida f\nachica Λ", dx=1.0, dy=-0.1)
    ax.text(-0.85, arriba + 0.75, "entidad publicación", fontsize=8.5, weight="bold", color="#2b5d8a")
    ax.text(-0.85, abajo + 0.75, "entidad ítem de moderación", fontsize=8.5, weight="bold", color="#3d7a2a")
    ax.set_xlim(-1, 11)
    ax.set_ylim(-0.6, 4.0)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(FIG / "b1_bloques.png", dpi=200)


def del_notebook(ruta):
    """Guarda en orden los PNG de las salidas del notebook: el día entero y la cola del stress test."""
    nb = json.loads(Path(ruta).read_text())
    imagenes = [o["data"]["image/png"] for c in nb["cells"] if c["cell_type"] == "code"
                for o in c.get("outputs", []) if "image/png" in o.get("data", {})]
    for nombre, png in zip(["b2_dia.png", "b3_cola_stress.png"], imagenes):
        (FIG / nombre).write_bytes(base64.b64decode(png))
    return len(imagenes)


if __name__ == "__main__":
    bloques()
    if len(sys.argv) > 1:
        print("imágenes del notebook:", del_notebook(sys.argv[1]))
