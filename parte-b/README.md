# Parte B · el simulador (entrega del viernes 16/10, 12:00)

Todo lo de la segunda entrega va en esta carpeta. Lo de la parte A (decisiones D1 a D20, modelo
conceptual y de datos) sigue en el [README de la raíz](../README.md) y no se toca.

**Estado: versión preliminar, lunes 12/10.** El simulador corre de punta a punta y está en
[`simulador.ipynb`](simulador.ipynb), con los resultados ya calculados para leerlo sin correrlo.
Falta revisarlo entre los tres, y el informe (máximo 10 páginas) todavía no está empezado.

## Cómo correrlo

1. Los dos CSV del campus van en [`../datos/`](../datos/README.md).
2. `pip install -r requirements.txt` (o `uv pip install -r requirements.txt`).
3. Abrir `simulador.ipynb` y correr todo. Tarda unos 10 minutos, casi todo en el paso 7
   (el piloto de N).

## Qué pide la grilla B y dónde está

| Grilla B | Dónde está en el notebook | Estado |
|---|---|---|
| Entidades: atributos y llegadas | pasos 2 (publicación) y 4 (llegadas por hora) | ✅ |
| Actividades y flujo: lógicas de filas, aleatoriedad | pasos 2 y 3 | ✅ |
| Recursos: lógica de asignación | paso 3 (moderadores, FIFO) | ✅; la prioridad por toxicidad queda como escenario |
| Variables de referencia | pasos 6 y 7 | ✅ las dos de la parte A |
| Variables de estado, calculadas en los eventos y graficadas | pasos 3 y 4 | ✅ cola, ocupados, publicaciones vivas |
| Stress test variando VD | paso 8 | ✅ c, volumen, fricción, degradación, clasificador |
| Debugging documentado | pasos 5, 7 y 9 | ✅ hay que contarlo en el informe |
| 2 funcionalidades no vistas en clase | ver abajo | a elegir |
| Informe: lógicas y bloques | — | ⬜ |
| Informe: dificultades y cambios respecto de la parte A | último paso del notebook | ⬜ pasarlo al informe |
| Informe: N y resultado en condiciones iniciales, con IC | pasos 6 y 7 | ⬜ pasarlo al informe |

## Los bloques de AnyLogic y lo que usamos en Python

El tutor aceptó Python, pidiendo que mostremos la analogía con los bloques de clase.

| AnyLogic | En el notebook | Para qué |
|---|---|---|
| *Agent type* con parámetros | un diccionario `pub` con los atributos | la publicación y el ítem de moderación |
| `Source` | el proceso `llegadas`: espera un tiempo exponencial con la tasa de la hora y crea una publicación | evento exógeno publicar |
| `Delay` | `env.timeout(t)` | demora entre generaciones; piso de 90 minutos |
| `SelectOutput` | un sorteo y un `if` | si Centinela marca, nace un ítem de moderación |
| `Queue` + `Service` + `ResourcePool` | `simpy.Resource(capacity=c)` y `with moderadores.request()` | la cola de moderación con *c* moderadores |
| `Sink` | el fin de la función del proceso | la publicación muere cuando el frente queda vacío |
| Variables y su gráfico | `anotar(ve, valor)` en cada evento, y un gráfico en escalones | variables de estado, sin muestreo cíclico |
| *Statistics* / *Dataset* | el diccionario `VR` y las listas de latencias y tamaños | variables de referencia |
| Parámetros del experimento | el diccionario de VD (`c`, `umbral`, `reduccion`, `degradar`, `clasificador`, `volumen`) | escenarios |

## Candidatas a «funcionalidades no vistas en clase»

1. **Números aleatorios comunes.** Cada publicación, cada generación y cada ítem tienen su propio
   generador sembrado con su número, y los sorteos se hacen por la inversa de la acumulada. Así
   dos escenarios ven las mismas publicaciones y la diferencia es de la palanca. Sin esto, N
   sería impracticable (paso 7).
2. **Variables de estado anotadas por evento** y promediadas en el tiempo, con las que
   comprobamos la ley de Little y la ocupación del balanceo (paso 9).
3. Pendiente, si queremos una tercera: la cola con prioridad por toxicidad
   (`simpy.PriorityResource`), que la parte A dejó como escenario.

## Lo que corregimos de la parte A con la teoría

- **El error admitido de N estaba en porcentaje** («por debajo del 5 % de su media»). La cátedra lo
  pide en valor absoluto (clase 02): «¿es razonable dar un % de un valor que aún no se conoce?».
  Ahora es ±7.920 USD por mes, la mitad de lo que cuesta un moderador, que es la decisión más chica
  que hay que poder distinguir.
- **No habíamos dicho nada del transitorio.** La cola arranca vacía y con un moderador al 99 % tarda
  en llegar al régimen: descartamos dos días de calentamiento en cada corrida (clase 08).
- **La escala era 50**, calculada con una M/M/1. Con el tiempo de revisión Erlang y calibrando sobre
  un mes queda en 53.
- **El plan de cuadros:** los cuadros 3 y 4 (barras apiladas del costo y daño evitado por peso) no
  decían que llevan intervalo de confianza. Ningún punto sin IC: hay que agregarlo en la parte C.

## Para revisar entre los tres

Lo que salió de correr el simulador y conviene decidir juntos:

| Hallazgo | Dónde | Qué hay que decidir |
|---|---|---|
| **N da unos 240 meses por escenario** con ±7.920 USD de error, aun con números aleatorios comunes (sin ellos serían unos 1.600) | paso 7 | aceptar unas dos horas de cómputo por escenario, relajar el error a un moderador entero (N baja a la cuarta parte) o pasar la réplica a una semana |
| **El p99 del tamaño de las cascadas da la mitad del observado** (69 contra 151). El tamaño medio y el p90 dan bien | paso 5 | recalibrar los R para las cascadas grandes, como preveía la parte A |
| **La cola de un moderador se arma de tarde y se vacía de noche**, y en los datos la latencia no sube en el pico | pasos 4 y 8 | es la limitación que ya declaramos en la A; contarla en el informe con el gráfico |
| **Con 5 % más de volumen la cola no crece sin límite**, como decía la evaluación a priori, porque la tasa baja de noche | paso 8 | corregir esa frase en lo que se diga de la A |
| **El clasificador nuevo con un solo moderador da más impresiones nocivas que hoy**: marca el doble, la cola llega a 9.000 ítems y las remociones llegan tarde | paso 8 | es un resultado para la parte C: el clasificador sólo sirve junto con más moderadores |
| **La escala es 53, no 50**, y con 54 la cola de un mes no se estabiliza | paso 5 | nada; anotarlo en los cambios respecto de la A |

El modelo pasa los controles del paso 9: ninguna latencia baja del piso de 90 minutos, la ley de
Little en la cola da 0,35 contra 0,34, y la ocupación medida da 0,443 contra 0,448 del balanceo.

## Para preguntarle al profe el martes 13/10

1. ¿Nos corrigen la parte A antes del viernes? Si no, ¿los cambios por la corrección pueden ir en
   la parte C?
2. La grilla dice «calcular N – cantidad de días a simular». Nosotros tomamos como réplica un mes,
   que es el horizonte de la parte A. ¿Está bien, o esperan N en días?
3. ¿Qué cuenta como «funcionalidad no vista en clase» si no usamos AnyLogic?
