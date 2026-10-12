"""Números y figuras del informe TP3A (IO II, RedBaires) · 26/9/2026.

Lee la muestra desde ../datos/ (fuera de git) y escribe figuras/ y numeros.txt.
Correr desde parte-a/:  python analisis.py
"""
from math import factorial, log
from pathlib import Path

import matplotlib
import matplotlib.ticker
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

AQUI = Path(__file__).parent
DATOS = AQUI.parent / "datos" / "muestra_cascadas_REDBAIRES.csv"
FIG = AQUI / "figuras"
FIG.mkdir(exist_ok=True)
out = open(AQUI / "numeros.txt", "w")


def say(*a):
    print(*a)
    print(*a, file=out)


plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 200, "savefig.bbox": "tight"})
AZUL, GRIS, ROJO = "#2f5d8a", "#9a9a9a", "#b8483b"
COMA = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))

# ---------- limpieza mínima ----------
df = pd.read_csv(DATOS)
d = df.drop_duplicates().drop_duplicates("event_id").copy()
d["t"] = pd.to_datetime(d.forward_datetime, errors="coerce", format="mixed")
trunc = d.groupby("cascade_id").size().loc[lambda x: x >= 500].index
d = d[d.t.dt.year < 2090]
for c in ["account_type_code", "platform_surface_code", "content_type_code"]:
    d[c] = d[c].str.upper()
hijos = d.parent_event_id.value_counts()
d["hijos"] = d.event_id.map(hijos).fillna(0).astype(int)
d["nocivo"] = d.topic_code.str.startswith("DISARM")
size = d.groupby("cascade_id").size()
d["c2"] = d.hashtag_cluster_ref.str.endswith("-C2")
say("eventos limpios", len(d), "cascadas", size.size, "truncadas", len(trunc))

# ---------- Fig 1: tamaño de cascadas (CCDF) ----------
s = np.sort(size.values)
ccdf = 1 - np.arange(len(s)) / len(s)
fig, ax = plt.subplots(figsize=(3.2, 2.2))
ax.loglog(s, ccdf, ".", ms=2, color=AZUL)
ax.set_xlabel("tamaño de la cascada (eventos)")
ax.set_ylabel("P(tamaño ≥ x)")
ax.axvline(500, color=GRIS, lw=0.8, ls="--")
ax.text(480, 0.3, "tope del\nexport", ha="right", fontsize=7, color=GRIS)
fig.savefig(FIG / "f1_tamanos.png")
say("tamaño: 1 evento", (size == 1).mean().round(4), "p50", size.median(), "p90", size.quantile(.9),
    "p99", size.quantile(.99))
imp_c = d.groupby("cascade_id").impressions.sum().sort_values(ascending=False)
k = len(imp_c) // 100
say("1% de cascadas concentra", round(imp_c.iloc[:k].sum() / imp_c.sum(), 3), "de las impresiones")

# ---------- Fig 2: llegadas por hora ----------
seeds = d[d.seed_flag == 1]
dias = (seeds.t.max() - seeds.t.min()).days + 1
por_hora = seeds.groupby(seeds.t.dt.hour).size() / dias
fig, ax = plt.subplots(figsize=(3.2, 2.2))
ax.bar(por_hora.index, por_hora.values, color=AZUL, width=0.8)
ax.axhline(por_hora.mean(), color=GRIS, lw=0.8, ls="--")
ax.set_xlabel("hora del día")
ax.set_ylabel("publicaciones por hora")
ax.yaxis.set_major_formatter(COMA)
fig.savefig(FIG / "f2_llegadas.png")
say("días", dias, "tasa media/h", round(por_hora.mean(), 3), "min", round(por_hora.min(), 2),
    "max", round(por_hora.max(), 2))
dow = seeds.groupby(seeds.t.dt.dayofweek).size()
say("semillas por día de semana (lun=0)", dow.to_dict())
# ¿exponencial el tiempo entre semillas, dentro de una franja?
ts = seeds.t.sort_values()
gap = ts.diff().dt.total_seconds().dropna() / 3600
franja = ts.dt.hour.iloc[1:].values
g = gap[(franja >= 10) & (franja < 19)]
say("entre semillas 10-19h: media h", round(g.mean(), 3), "CV", round(g.std() / g.mean(), 2),
    "KS expon D", round(stats.kstest(g, "expon", args=(0, g.mean())).statistic, 3))

# ---------- Fig 3: tiempo entre generaciones ----------
x = d.loc[(d.seed_flag == 0) & (d.inter_event_time_min > 0), "inter_event_time_min"].values
a, loc, sc = stats.gamma.fit(x, floc=0)
say("gamma forma", round(a, 3), "escala", round(sc, 1), "media", round(x.mean(), 1), "mediana",
    np.median(x), "n", len(x), "KS", round(stats.kstest(x, "gamma", args=(a, 0, sc)).statistic, 3))
fig, ax = plt.subplots(figsize=(3.2, 2.2))
bins = np.linspace(0, 400, 81)
ax.hist(x, bins=bins, density=True, color=AZUL, alpha=0.6, label="datos")
xx = np.linspace(1, 400, 400)
ax.plot(xx, stats.gamma.pdf(xx, a, 0, sc), color=ROJO, lw=1.2, label=f"gamma ({a:.2f}; {sc:.0f} min)".replace(".", ","))
ax.plot(xx, stats.expon.pdf(xx, 0, x.mean()), color=GRIS, lw=1, ls="--", label="exponencial")
ax.set_xlabel("minutos entre un reenvío y su hijo")
ax.set_ylabel("densidad")
ax.set_ylim(0, 0.03)
ax.yaxis.set_major_formatter(COMA)
ax.legend(frameon=False, fontsize=7)
fig.savefig(FIG / "f3_generaciones.png")

# ---------- Fig 4: latencia de moderación ----------
m = d[d.moderation_flag == 1]
lat = m.moderation_latency_min
lat = lat[(lat > 0) & (lat <= 24 * 60)]
say("latencia: n", len(lat), "min", lat.min(), "p10", lat.quantile(.1), "mediana", lat.median(),
    "media", round(lat.mean(), 1), "p90", lat.quantile(.9))
w = lat - 90
say("latencia − 90: mediana", w.median(), "media", round(w.mean(), 1), "p90", w.quantile(.9),
    "CV", round(w.std() / w.mean(), 2))
fig, ax = plt.subplots(figsize=(3.2, 2.2))
ax.hist(lat, bins=np.arange(80, 800, 10), color=AZUL, alpha=0.7)
ax.axvline(90, color=ROJO, lw=1)
ax.text(95, ax.get_ylim()[1] * 0.85, "piso de 90 min", color=ROJO, fontsize=7)
ax.set_xlabel("minutos entre la marca y la acción")
ax.set_ylabel("ítems marcados")
fig.savefig(FIG / "f4_latencia.png")

# ¿la latencia sube con la carga? marcados en la hora anterior
m2 = m.dropna(subset=["t"]).sort_values("t").set_index("t")
carga = m2.moderation_flag.rolling("60min").sum()
ok = m2.moderation_latency_min.between(1, 1440)
rho_s = stats.spearmanr(carga[ok], m2.moderation_latency_min[ok]).correlation
say("Spearman latencia vs marcados en la hora previa", round(rho_s, 3))
por_h = m2[ok].groupby(m2[ok].index.hour).moderation_latency_min.median()
say("mediana de latencia por hora: min", por_h.min(), "max", por_h.max())

# ---------- relación impresiones ~ seguidores ----------
r = d.dropna(subset=["impressions"])
r = r[r.actor_follower_count > 0]
sl, ic, rv, *_ = stats.linregress(r.actor_follower_count, r.impressions)
b = (r.impressions * r.actor_follower_count).sum() / (r.actor_follower_count ** 2).sum()
ratio = (r.impressions / r.actor_follower_count)
say("impresiones = b·seguidores, b", round(b, 4), "R2 lineal", round(rv ** 2, 4),
    "cociente mediana", round(ratio.median(), 4), "p10", round(ratio.quantile(.1), 3), "p90",
    round(ratio.quantile(.9), 3))
say("cociente por tipo", r.assign(q=ratio).groupby("account_type_code").q.median().round(3).to_dict())
fig, ax = plt.subplots(figsize=(3.2, 2.2))
smp = r.sample(6000, random_state=1)
ax.loglog(smp.actor_follower_count, smp.impressions, ".", ms=1, color=AZUL, alpha=0.4)
xx = np.logspace(1, 7, 50)
q = ratio.median()
ax.loglog(xx, q * xx, color=ROJO, lw=1, label=f"impresiones = {q:.2f} × seguidores".replace(".", ","))
ax.set_xlabel("seguidores de quien reenvía")
ax.set_ylabel("impresiones del evento")
ax.legend(frameon=False, fontsize=7)
fig.savefig(FIG / "f5_impresiones.png")

# ---------- hijos: tipo de cuenta, generación, superficie ----------
dn = d[~d.cascade_id.isin(trunc)]
say("R total", round(dn.hijos.mean(), 3), "var/media", round(dn.hijos.var() / dn.hijos.mean(), 2))
say("R por tipo", dn.groupby("account_type_code").hijos.mean().round(3).to_dict())
say("mezcla de reenvíos", dn[dn.seed_flag == 0].account_type_code.value_counts(normalize=True).round(3).to_dict())
say("mezcla de semillas", dn[dn.seed_flag == 1].account_type_code.value_counts(normalize=True).round(3).to_dict())
say("R por superficie", dn.groupby("platform_surface_code").hijos.mean().round(2).to_dict())
say("R por generación", dn.groupby("cascade_depth").hijos.mean().round(3).head(12).to_dict())
# ¿el efecto de la generación sobrevive dentro de cada tipo?
say("R por generación, sólo STANDARD", dn[dn.account_type_code == "STANDARD"].groupby("cascade_depth").hijos.mean().round(3).head(8).to_dict())
say("R por generación, sólo BROADCASTER", dn[dn.account_type_code == "BROADCASTER"].groupby("cascade_depth").hijos.mean().round(3).head(6).to_dict())
say("R nocivo vs no", dn.groupby("nocivo").hijos.mean().round(3).to_dict())

# ---------- nocivo y marca ----------
say("fracción nociva de eventos", round(d.nocivo.mean(), 3), "de impresiones",
    round(d.loc[d.nocivo, "impressions"].sum() / d.impressions.sum(), 3))
marc = d[d.moderation_flag == 1]
say("marcados", len(marc), "de ellos legítimos", round((~marc.nocivo).mean(), 3))
say("marcados por día", round(len(marc) / dias, 1))
say("verificadas: % eventos", round(d.verified_flag.mean(), 3))

# ---------- ventana de la moderación ----------
# minutos desde la publicación de cada evento
t0 = d.groupby("cascade_id").t.transform("min")
d["desde_pub"] = (d.t - t0).dt.total_seconds() / 60
noc = d[d.nocivo & d.impressions.notna()]
for T in [0, 43, 90, 139, 240, 360]:
    say(f"impresiones nocivas después de {T} min desde publicar",
        round(noc.loc[noc.desde_pub > T, "impressions"].sum() / noc.impressions.sum(), 3))
grandes = noc.groupby("cascade_id").size()
big = grandes[grandes >= 29].index
nb = noc[noc.cascade_id.isin(big)]
for T in [90, 139]:
    say(f"  en cascadas nocivas ≥ p90 (29 eventos), después de {T} min",
        round(nb.loc[nb.desde_pub > T, "impressions"].sum() / nb.impressions.sum(), 3))

# ---------- C2 ----------
c2s = d.groupby("cascade_id").c2.first()
say("cascadas C2", int(c2s.sum()), "tamaño medio C2", round(size[c2s].mean(), 1), "resto",
    round(size[~c2s].mean(), 1))
say("R C2 sin truncadas", round(dn[dn.c2].hijos.mean(), 3), "R resto", round(dn[~dn.c2].hijos.mean(), 3))
say("C2 % de impresiones nocivas", round(noc.loc[noc.c2, "impressions"].sum() / noc.impressions.sum(), 3),
    "C2 nocivas?", round(d[d.c2].nocivo.mean(), 3))

# ---------- a priori: la fila ----------
mu = 3.0  # ítems por minuto: 20 s por ítem (0,12 USD ÷ 22 USD/h)
objetivo = w.median()  # espera mediana a reproducir, sobre el piso de 90


def mediana_mm1(rho):
    # P(Wq > t) = rho · exp(-(mu - lam) t); la mediana existe si rho > 0,5
    lam = rho * mu
    return log(2 * rho) / (mu - lam)


lo, hi = 0.51, 0.999999
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if mediana_mm1(mid) < objetivo else (lo, mid)
rho_cal = lo
lam_cal = rho_cal * mu  # ítems marcados por minuto
say(f"calibración M/M/1: rho {rho_cal:.4f}, λ {lam_cal * 1440:.0f} ítems/día, factor sobre la muestra "
    f"{lam_cal * 1440 / (len(marc) / dias):.0f}, media Wq {rho_cal / (mu - lam_cal):.0f} min, "
    f"p90 Wq {log(10 * rho_cal) / (mu - lam_cal):.0f} min")


def erlang_c(c, lam, mu):
    a = lam / mu
    rho = a / c
    s = sum(a ** n / factorial(n) for n in range(c))
    top = a ** c / (factorial(c) * (1 - rho))
    pw = top / (s + top)
    return pw, pw / (c * mu - lam)


for c in [1, 2, 3, 4]:
    pw, wq = erlang_c(c, lam_cal, mu)
    say(f"c={c}: ocupación {lam_cal / (c * mu):.3f}, P(esperar) {pw:.3f}, Wq media {wq:.2f} min, "
        f"latencia media {90 + wq + 1 / mu:.1f} min")
for f in [0.9, 0.95, 1.0, 1.05, 1.4]:
    lam = lam_cal * f
    rho = lam / mu
    txt = f"Wq media {rho / (mu - lam):.0f} min" if rho < 1 else "inestable"
    say(f"  c=1 con {f:.2f}× el volumen calibrado: ρ {rho:.3f}, {txt}")

# ---------- a priori: ramificación y palancas ----------
R, Rc2 = 0.916, 1 - 1 / 42.8
say("R C2 por tamaño", round(Rc2, 3))
for r_ in [0, 0.1, 0.3, 0.5]:
    say(f"fricción {r_}: R C2 efectivo {Rc2 * (1 - r_):.3f}, tamaño {1 / (1 - Rc2 * (1 - r_)):.1f}; "
        f"todas {1 / (1 - R * (1 - r_)):.1f}")

# ---------- detección de coordinadas ----------
d["nueva"] = d.account_age_days < 30
prim = d[d.desde_pub <= 120].groupby("cascade_id").nueva.sum()
for u in [1, 3]:
    det = prim >= u
    tp = (det & c2s.reindex(det.index)).sum()
    say(f"regla ≥{u} cuentas nuevas en 2 h: precisión {tp / det.sum():.2f}, recall {tp / c2s.sum():.2f}, "
        f"cascadas señaladas {det.sum()}")

out.close()


# ---------- paneles para el informe ----------
def panel(nombres, salida):
    from PIL import Image, ImageDraw, ImageFont
    ims = [Image.open(FIG / f"{n}.png").convert("RGB") for n in nombres]
    h = max(i.height for i in ims)
    ims = [i.resize((int(i.width * h / i.height), h)) for i in ims]
    W = sum(i.width for i in ims) + 40 * (len(ims) - 1)
    c = Image.new("RGB", (W, h + 10), "white")
    x = 0
    dr = ImageDraw.Draw(c)
    try:
        f = ImageFont.truetype("DejaVuSans-Bold.ttf", 38)
    except OSError:
        f = ImageFont.load_default()
    for letra, i in zip("abcd", ims):
        c.paste(i, (x, 10))
        dr.text((x + 5, 0), f"({letra})", fill="black", font=f)
        x += i.width + 40
    c.save(FIG / salida)


panel(["f1_tamanos", "f2_llegadas"], "p1_tamanos_llegadas.png")
panel(["f3_generaciones", "f4_latencia"], "p2_generaciones_latencia.png")
