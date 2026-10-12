# TP3 · Investigación de Operaciones II · RedBaires

Simulador de eventos discretos para el TP3 de IO II (ITBA, 2º cuatrimestre 2026). El caso es
RedBaires, una red social que factura por impresión y quiere saber qué palanca le conviene
contra la difusión de rumores: más moderadores, un límite a los reenvíos o degradar el alcance
de las cuentas coordinadas.

| Entrega | Qué se produce | Vence | Dónde está |
|---|---|---|---|
| **TP3A** | modelo conceptual y modelo de datos, máximo 12 páginas | viernes 2/10, 12:00 · ✅ entregada | [`parte-a/`](parte-a/README.md) |
| **TP3B** | el simulador, máximo 10 páginas | **viernes 16/10, 12:00** | [`parte-b/`](parte-b/README.md) · versión preliminar del 12/10 |
| TP3C | experimentación, máximo 10 páginas | viernes 13/11, 12:00 | — |

## Cómo usar el repo

- **Datos:** no están en el repo porque son material de la cátedra. Van en [`datos/`](datos/README.md),
  y los usan las dos partes.
- **Herramienta:** Python. El simulador usa SimPy; las librerías están en
  [`parte-b/requirements.txt`](parte-b/requirements.txt).
- **Decisiones:** las de la parte A tienen número (D1 a D20) y están en
  [`parte-a/README.md`](parte-a/README.md). Con decir «D8: DISARM» en el grupo alcanza.
