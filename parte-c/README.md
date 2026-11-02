# Parte C · experimentación (entrega del viernes 13/11, 12:00)

Todo lo de la tercera entrega va en esta carpeta. El simulador del que parte es el de
[`../parte-b/simulador.ipynb`](../parte-b/simulador.ipynb). Las decisiones D1 a D20 están en
[`../parte-a/README.md`](../parte-a/README.md).

| | |
|---|---|
| Vence | viernes 13/11/2026, 12:00, por el campus. La mora es de −0,1 punto por día |
| Largo | máximo 10 páginas |
| Qué se sube | informe PDF y el notebook o código de la experimentación |
| Pesa | 1 punto de los 11 de la cursada, y sin el TP3 completo no se aprueba la cursada |

## Lo que pide la consigna, textual

Del memorándum de RedBaires (`TP3-consigna.pdf`, sección 7):

> Las preguntas que la Dirección quiere ver respondidas, con números y no con opiniones, son:
> ¿conviene adoptar cada una de estas medidas? ¿En qué intensidad? ¿Cuál es el costo-beneficio de
> cada una y cuál rinde más por cada peso invertido? La recomendación final debe indicar, de manera
> inequívoca, qué haría el equipo en nuestro lugar y por qué. Nos importa especialmente entender bajo
> qué condiciones una medida que hoy parece cara se vuelve imprescindible (y viceversa).

Las tres palancas son ampliar la moderación (más moderadores, mejor clasificador o ambos), poner
fricción a los reenvíos y degradar el alcance de las cuentas grandes o coordinadas.

De la sección 8:

> El modelo debe ser reproducible y permitir cambiar los supuestos con facilidad. La Dirección no
> quiere un único número: quiere ver un rango de resultados (al menos un escenario conservador, uno
> intermedio y uno pesimista) y entender qué tan sensible es la conclusión a los supuestos.

> La recomendación se defenderá ante el comité. Esperen preguntas sobre por qué el modelo se comporta
> como lo hace, pedidos de justificar cada supuesto y de recalcular en vivo cambiando alguno.

## La grilla C de la cátedra

Transcripta de `IO2-22C1-TP 3-Contenidos C.PNG`. Cada sección vale el 50 %.

**Proceso de experimentación (50 %)**

| Elemento | Qué miran |
|---|---|
| Procedimiento de experimentación | plantear un plan previo, la heurística y los pasos de cálculo |
| VD: justificación de rangos y lógica de variación | rango, *step* y valores descartados |
| Condiciones del experimento | duración y *warm up* |
| Medición de VR y output de los experimentos | exportar los resultados |
| Parameter Variation (PV) | que esté bien programada |
| Automatización | correr el total de experimentos, calcular las VR y exportar los datos con un click |

**Análisis y conclusiones (50 %)**

| Elemento | Qué miran |
|---|---|
| Dificultades, errores y debugging de la experimentación | |
| Cambios contra el modelo conceptual y el simulador de la parte B | los ajustes, explicados |
| Resultados con IC y comparación entre escenarios | cálculo de IC, tests adecuados y distintos métodos para comparar alternativas |
| Conclusión y recomendación final | claridad |

Para el informe miran el orden del código, los comentarios, el formato de los gráficos, el índice,
las referencias y la ortografía.

## Lo que dijeron en clase el 27/10 (Experimentación 1 y 2)

Sale de las notas de Gonzalo, que mandó por mail el 28/10:

- [ ] Evaluar cada propuesta con las VR que salen del simulador.
- [ ] Si hay un inventario o un nivel que cambia en el tiempo, se usa el promedio ponderado por
      tiempo y no el promedio simple.
- [ ] Decidir y justificar si las corridas son con terminación o *long run*. Si son *long run*, hace
      falta *warm-up*, que se busca mirando las VE, y hay que cuidar la autocorrelación.
- [ ] Si el simulador cambió desde el TP3B, recalcular el N de corridas con el nuevo y quedarse con
      el más alto.
- [ ] Chequear la homocedasticidad, después aplicar Tukey entre las alternativas y dar los resultados
      como IC.
- [ ] Elegir qué se compara contra qué, porque comparar todos contra todos gasta cómputo.
- [ ] Preparar la explicación de cada estadístico que vaya a la presentación.

## Para arrancar

1. Definir las alternativas: qué valores de cada palanca y qué combinaciones se prueban, con el rango,
   el *step* y lo que se descarta. Es lo primero que pide la grilla.
2. Definir los tres escenarios de supuestos (conservador, intermedio y pesimista) con los rangos de
   `parametros_y_costos.csv`.
3. Automatizar la corrida de todo el diseño en el notebook, con un solo click, y exportar a CSV.
4. Calcular los IC y las comparaciones, y escribir la recomendación.
