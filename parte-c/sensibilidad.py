"""Escenarios de volumen y campañas (decisión 10) y sensibilidad de los supuestos (decisión 11), sólo
sobre las finalistas de la ronda 2 y hoy, con 30 réplicas de un mes y las mismas semillas.

Uso, desde parte-c/:  ../.venv/bin/python sensibilidad.py c2+dg+cl c2+cl
(los argumentos son combinaciones de la ronda 2; hoy se agrega siempre)
"""
import json, sys

for celda in json.load(open("simulador.ipynb"))["cells"]:
    if "modelo" in celda["metadata"].get("tags", []):
        exec("".join(celda["source"]), globals())
for celda in json.load(open("experimentos.ipynb"))["cells"]:
    src = "".join(celda["source"])
    if celda["cell_type"] == "code" and "def correr_ronda" in src:
        exec(src, globals())                       # ALTERNATIVAS, SEMILLAS, replica y correr_ronda; no corre nada

PALANCAS = {"c2": dict(c=2), "fr": dict(umbral=20, reduccion=.3), "dg": dict(degradar=True, d=.3), "cl": dict(clasificador=(.95, .9))}

def vd(combo):
    v = dict(c=1)
    if combo != "hoy":
        for p in combo.split("+"):
            v.update(PALANCAS[p])
    return v

# Lo que la empresa no decide. m = 1,215 lleva el R medio de las campañas a 0,99 (R orgánico medio 0,815).
CONDICIONES = {
    "volumen_0.9": dict(volumen=0.9),                # escenario conservador
    "campanias_R0.99": dict(m_coord=1.215),          # escenario pesimista
    "remocion_x0.5": dict(factor_remocion=0.5),
    "remocion_x1.5": dict(factor_remocion=1.5),
    "revision_10s": dict(tiempo_revision_seg=10),
    "revision_40s": dict(tiempo_revision_seg=40),
    "demora_mezcla": dict(demora="mezcla"),
}

if __name__ == "__main__":
    combos = ["hoy"] + [c for c in sys.argv[1:] if c != "hoy"]
    for nombre, esc in CONDICIONES.items():
        correr_ronda(f"resultados/sensibilidad/{nombre}", {c: vd(c) for c in combos}, SEMILLAS, escenario=esc)
