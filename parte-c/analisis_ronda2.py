"""Análisis de la ronda 2 (decisiones 9, 10, 12 y 13 del grupo). Se copia al notebook de experimentos
cuando la ronda termina; mientras tanto corre con las combinaciones que ya están.

Uso, desde parte-c/:  ../.venv/bin/python analisis_ronda2.py
"""
import itertools, json, os
import numpy as np, pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

for celda in json.load(open("simulador.ipynb"))["cells"]:
    if "modelo" in celda["metadata"].get("tags", []):
        exec("".join(celda["source"]), globals())

TOPE = 0.15
DE_RONDA1 = {"hoy": "hoy", "c2": "c2", "fr": "friccion_u20_r3", "dg": "degradacion_3", "c2+cl": "clasificador_95_90_c2"}
NOMBRES = {"hoy": "Hoy", "c2": "2 moderadores", "fr": "Fricción", "dg": "Degradación", "cl": "Clasificador 95/90"}
ORDEN = ["hoy", "dg", "fr", "fr+dg", "c2", "c2+dg", "c2+fr", "c2+fr+dg", "c2+cl", "c2+dg+cl", "c2+fr+cl", "c2+fr+dg+cl"]

def legible(combo):
    return "Hoy" if combo == "hoy" else " + ".join(NOMBRES[p] for p in combo.split("+"))

def cargar():
    partes = []
    for combo in ORDEN:
        ruta = f"resultados/ronda2/{combo}.csv"
        if not os.path.exists(ruta):
            continue
        r2 = pd.read_csv(ruta).assign(alternativa=combo)
        if combo in DE_RONDA1:
            r1 = pd.read_csv(f"resultados/ronda1/{DE_RONDA1[combo]}.csv").assign(alternativa=combo)
            r2 = pd.concat([r1, r2])
        partes.append(r2)
    return pd.concat(partes, ignore_index=True)

def por_replica(df, combo, C):
    b = df[df.alternativa == "hoy"].set_index("semilla")
    a = df[df.alternativa == combo].set_index("semilla")
    semillas = b.index.intersection(a.index)
    costo = pd.Series([costo_mes(a.loc[s], b.loc[s], C) for s in semillas], index=semillas)
    perdidas = pd.Series([legitimas_perdidas(b.loc[s], a.loc[s]) / b.loc[s, "legitimas"] for s in semillas], index=semillas)
    return costo, perdidas, a.loc[semillas]

def ic(x, alfa=0.05):
    x = np.asarray(x); h = stats.t.ppf(1 - alfa / 2, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x))
    return x.mean(), h

def resumen(df, C):
    filas, costos = [], {}
    for combo in [c for c in ORDEN if c in set(df.alternativa)]:
        costo, perd, a = por_replica(df, combo, C)
        costos[combo] = costo
        (cm, ch), (nm, nh), (pm, ph) = ic(costo / 1e3), ic(a.nocivas / 1e6), ic(perd * 100)
        filas.append(dict(combo=combo, alternativa=legible(combo), N=len(costo), costo=cm, ic_costo=ch, nocivas=nm, ic_nocivas=nh,
                          perdidas=pm, ic_perdidas=ph, latencia=a.lat_mediana.median(), dentro=pm / 100 <= TOPE))
    return pd.DataFrame(filas), costos

def comparar(tabla, costos):
    """Diferencias apareadas de costo de cada alternativa dentro del tope contra la más barata, con Bonferroni."""
    ok = tabla[tabla.dentro].sort_values("costo")
    mejor = ok.combo.iloc[0]
    k = len(ok) - 1
    filas = []
    for combo in ok.combo.iloc[1:]:
        s = costos[combo].index.intersection(costos[mejor].index)
        d = (costos[combo].loc[s] - costos[mejor].loc[s]) / 1e3
        m, h = ic(d, alfa=0.05 / max(k, 1))
        filas.append(dict(alternativa=legible(combo), diferencia=m, ic=h, distinguible=(m - h) > 0))
    comunes = sorted(set.intersection(*[set(costos[c].index) for c in ok.combo]))
    fr = stats.friedmanchisquare(*[costos[c].loc[comunes].values for c in ok.combo]) if len(ok) >= 3 else None
    rangos = pd.DataFrame({legible(c): costos[c].loc[comunes].values for c in ok.combo}).rank(axis=1).mean().sort_values()
    return mejor, pd.DataFrame(filas), fr, rangos

def escenarios(df, tabla):
    """Decisión 10: el costo de la impresión nociva entre 0,0011 y 0,098 USD, sin volver a simular."""
    base = P["C"]["nociva"]
    filas = []
    for nombre, valor in (("conservador", 0.0011), ("intermedio", base), ("pesimista", 0.098)):
        C2 = dict(P["C"], nociva=valor)
        t, _ = resumen(df, C2)
        ok = t[t.dentro].sort_values("costo")
        filas.append(dict(escenario=nombre, costo_nociva=valor, mejor=ok.alternativa.iloc[0], costo_mejor=ok.costo.iloc[0],
                          segunda=ok.alternativa.iloc[1] if len(ok) > 1 else "", costo_segunda=ok.costo.iloc[1] if len(ok) > 1 else np.nan))
    return pd.DataFrame(filas)

def quiebre(df):
    """Decisión 13: el costo de la impresión nociva desde el cual cada alternativa le gana a hoy.
    El costo es lineal en ese precio: costo = resto + precio × nocivas."""
    filas = []
    C0 = dict(P["C"], nociva=0.0)
    hoy = df[df.alternativa == "hoy"].set_index("semilla")
    for combo in [c for c in ORDEN if c != "hoy" and c in set(df.alternativa)]:
        costo0, _, a = por_replica(df, combo, C0)
        resto_hoy = pd.Series([costo_mes(hoy.loc[s], hoy.loc[s], C0) for s in costo0.index], index=costo0.index)
        d_resto = (costo0 - resto_hoy).mean()
        d_noc = (hoy.loc[costo0.index, "nocivas"] - a.nocivas).mean()
        filas.append(dict(alternativa=legible(combo), quiebre_usd=d_resto / d_noc if d_noc > 0 else np.inf))
    return pd.DataFrame(filas).sort_values("quiebre_usd")

CORTO = {"hoy": "hoy", "c2": "2 mod.", "fr": "fricción", "dg": "degradación", "cl": "clasif."}

def corto(combo):
    return "hoy" if combo == "hoy" else " + ".join(CORTO[p] for p in combo.split("+"))

def figuras(tabla):
    t = tabla.sort_values("costo").assign(et=lambda d: d.combo.map(corto))
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    colores = ["#2f5d8a" if d else "#b0b0b0" for d in t.dentro]
    ax.barh(t.et, t.costo, xerr=t.ic_costo, color=colores, capsize=3)
    ax.invert_yaxis(); ax.set_xlabel("Costo total por mes (miles de USD), con IC del 95 %")
    ax.set_xlim(t.costo.min() * 0.97, t.costo.max() * 1.01)
    ax.text(0.99, 0.98, "en gris, pierden más del 15 %\nde las impresiones legítimas", transform=ax.transAxes,
            ha="right", va="top", fontsize=8, color="#555555")
    fig.tight_layout(); fig.savefig("figuras/c3_costo_combinaciones.png", dpi=200); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.5, 5))
    ax.errorbar(t.perdidas, t.nocivas, xerr=t.ic_perdidas, yerr=t.ic_nocivas, fmt="o",
                color="#2f5d8a", ecolor="#2f5d8a")
    desvio = {"dg": (6, 4), "c2+dg": (6, -10), "c2+fr+cl": (-6, -12), "fr+dg": (6, 4), "c2+fr+dg": (6, -10),
              "fr": (6, 4), "c2+fr": (6, -10)}
    for _, r in t.iterrows():
        dx, dy = desvio.get(r.combo, (6, 4))
        ax.annotate(r.et, (r.perdidas, r.nocivas), fontsize=8, xytext=(dx, dy), textcoords="offset points",
                    ha="right" if dx < 0 else "left")
    ax.axvline(TOPE * 100, ls="--", color="#b8483b"); ax.text(TOPE * 100 + 0.3, t.nocivas.max(), "tope 15 %", color="#b8483b", fontsize=8)
    ax.set_xlim(-4, 34)
    ax.set_xlabel("Impresiones legítimas perdidas (% de las de hoy)"); ax.set_ylabel("Impresiones nocivas por mes (millones)")
    ax.text(0.01, 0.02, "2 mod. = 2 moderadores · clasif. = clasificador 95/90", transform=ax.transAxes,
            ha="left", va="bottom", fontsize=8, color="#555555")
    fig.tight_layout(); fig.savefig("figuras/c4_nocivas_vs_legitimas.png", dpi=200); plt.close(fig)

if __name__ == "__main__":
    df = cargar()
    print("combinaciones:", sorted(set(df.alternativa)), " réplicas:", df.groupby("alternativa").semilla.nunique().to_dict())
    tabla, costos = resumen(df, P["C"])
    pd.set_option("display.width", 200)
    print(tabla.round(1).to_string(index=False))
    mejor, comp, fr, rangos = comparar(tabla, costos)
    print("\nmás barata dentro del tope:", legible(mejor))
    print(comp.round(1).to_string(index=False))
    if fr: print("\nFriedman:", round(fr.statistic, 1), "p =", fr.pvalue)
    print("rango medio:\n", rangos.round(2).to_string())
    print("\n", escenarios(df, tabla).round(4).to_string(index=False))
    print("\n", quiebre(df).round(5).to_string(index=False))
    figuras(tabla)
    tabla.to_csv("resultados/ronda2_resumen.csv", index=False)
