"""Escenarios de volumen y campañas y sensibilidad de los supuestos (decisiones 10 y 11): para cada condición,
el costo y las legítimas perdidas de las finalistas contra hoy en la misma condición, y la diferencia apareada
entre las dos más baratas. Corre con las condiciones que ya terminaron.

Uso, desde parte-c/:  ../.venv/bin/python analisis_sensibilidad.py
"""
import json, os
import numpy as np, pandas as pd
from scipy import stats

for celda in json.load(open("simulador.ipynb"))["cells"]:
    if "modelo" in celda["metadata"].get("tags", []):
        exec("".join(celda["source"]), globals())

TOPE = 0.15
NOMBRES = {"c2+dg+cl": "2 moderadores + degradación + clasificador", "c2+fr+cl": "2 moderadores + fricción + clasificador",
           "c2+cl": "2 moderadores + clasificador"}
CONDICIONES = {"base": "Base (ronda 2)", "volumen_0.9": "Volumen ×0,9 (conservador)", "campanias_R0.99": "Campañas con R 0,99 (pesimista)",
               "remocion_x0.5": "Remoción ×0,5", "remocion_x1.5": "Remoción ×1,5", "revision_10s": "Revisión de 10 s",
               "revision_40s": "Revisión de 40 s", "demora_mezcla": "Demora entre generaciones: mezcla"}

def leer(cond, combo):
    if cond == "base":
        df = pd.read_csv(f"resultados/ronda2/{combo}.csv")
        viejo = {"hoy": "hoy", "c2+cl": "clasificador_95_90_c2"}.get(combo)
        if viejo:
            df = pd.concat([pd.read_csv(f"resultados/ronda1/{viejo}.csv"), df])
        return df[df.semilla < 130].set_index("semilla")          # las mismas 30 semillas que la sensibilidad
    ruta = f"resultados/sensibilidad/{cond}/{combo}.csv"
    return pd.read_csv(ruta).set_index("semilla") if os.path.exists(ruta) else None

def condicion(cond):
    hoy = leer(cond, "hoy")
    if hoy is None:
        return None
    filas, costos = [], {}
    for combo in NOMBRES:
        a = leer(cond, combo)
        if a is None:
            continue
        s = hoy.index.intersection(a.index)
        costo = pd.Series([costo_mes(a.loc[i], hoy.loc[i], P["C"]) for i in s], index=s) / 1e3
        perd = pd.Series([legitimas_perdidas(hoy.loc[i], a.loc[i]) / hoy.loc[i, "legitimas"] for i in s], index=s)
        costos[combo] = costo
        filas.append(dict(condicion=CONDICIONES[cond], alternativa=NOMBRES[combo], costo=costo.mean(), perdidas=100 * perd.mean(),
                          dentro=perd.mean() <= TOPE))
    t = pd.DataFrame(filas)
    if t.empty:
        return None
    ok = t[t.dentro].sort_values("costo")
    if len(ok) >= 2:
        a, b = [k for k, v in NOMBRES.items() if v in ok.alternativa.iloc[:2].tolist()]
        a, b = (a, b) if NOMBRES[a] == ok.alternativa.iloc[0] else (b, a)
        d = costos[b] - costos[a]
        h = stats.t.ppf(0.975, len(d) - 1) * d.std(ddof=1) / np.sqrt(len(d))
        t["gana"] = ok.alternativa.iloc[0]
        t["ventaja"] = f"{d.mean():.1f} ± {h:.1f}"
    return t

if __name__ == "__main__":
    pd.set_option("display.width", 220)
    tablas = [t for t in (condicion(c) for c in CONDICIONES) if t is not None]
    todo = pd.concat(tablas, ignore_index=True)
    print(todo.round(1).to_string(index=False))
    todo.to_csv("resultados/sensibilidad_resumen.csv", index=False)
