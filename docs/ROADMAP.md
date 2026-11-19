# Guía de desarrollo

El objetivo es aprender implementando y explicar las decisiones con tus propias palabras. Cada etapa debe dejar una implementación pequeña, una comprobación y una nota sobre lo aprendido.

El estado de cada etapa se mantiene en esta misma guía. La derivación matemática está documentada en [01 — Dynamic Models](theory/01-dynamic-models.md) y la preparación de herramientas en [ENVIRONMENT.md](ENVIRONMENT.md). Una casilla marcada indica solo la tarea descrita, no la validación completa de la etapa.

**Estado al 19 de noviembre de 2026:** se ha completado la derivación analítica del modelo ideal no lineal, su linealización alrededor del equilibrio superior y el análisis de inestabilidad en lazo abierto mediante el método indirecto de Lyapunov. Hay parámetros numéricos nominales aún **sin validación** con MuJoCo. Ver [02 — Linearization and Lyapunov's Indirect Method](theory/02-linearization-and-stability.md).

## 1. Primera simulación

- [x] Elegir una versión de MuJoCo y documentar el entorno: MuJoCo / Studio 4.0.1 para Windows x64; ver [entorno de desarrollo](ENVIRONMENT.md).
- [ ] Crear el modelo del carro y el péndulo en `models/`.
- [x] Proponer **valores nominales provisionales y unidades** de masas, longitud y gravedad: [config/cartpole-parameters.yaml](../config/cartpole-parameters.yaml).
- [ ] Contrastar la inercia, la geometría y los valores nominales con el futuro MJCF; aún no existe el modelo físico implementado.
- [x] Definir la **convención matemática**: eje x hacia la derecha, y hacia arriba; θ = 0 abajo y positivo antihorario; θ = π arriba. Véase [01 — Dynamic Models](theory/01-dynamic-models.md).
- [ ] Contrastar los ejes, el origen, el sentido del ángulo y la figura de coordenadas con el modelo MJCF real. La coherencia geométrica de la imagen requiere revisión independiente.
- [ ] Preparar CMake y un ejecutable C++ que cargue el modelo.
- [ ] Ejecutar movimiento pasivo desde una pequeña desviación de la posición inferior.
- [ ] Guardar tiempo, posiciones y velocidades para representarlos después.

**Criterio de avance:** puedes ejecutar la simulación desde cero y explicar cada coordenada. Todavía no necesitas un controlador.

Preguntas para trabajar: ¿qué grados de libertad tiene el sistema?, ¿cuántos actuadores tiene?, ¿qué hace estable al equilibrio inferior?, ¿cómo afecta el paso de integración?

## 2. Modelo dinámico

**Resultado hasta ahora:** derivación simbólica completada para el Cart-Pole ideal, sin rozamiento, con barra rígida sin masa y masa puntual en el extremo. Está descrita paso a paso en [01 — Dynamic Models](theory/01-dynamic-models.md) (ecuaciones [1]–[30]). **La etapa 2 aún no está validada numéricamente.**

- [x] Definir coordenadas generalizadas y orden del estado: `q = [x, θ]ᵀ`; `s = [x, θ, x_dot, theta_dot]ᵀ`, con entrada `u = F_x`.
- [x] Derivar la cinemática: posiciones `x_p = x + l sin(θ)`, `y_p = -l cos(θ)` y las velocidades del carro y la masa puntual.
- [x] Obtener y simplificar las energías cinética y potencial y el lagrangiano `L = T - U`.
- [x] Aplicar Euler–Lagrange por separado a la traslación `x` y a la rotación `θ`, identificando `Q_x = u` y `Q_θ = 0`.
- [x] Obtener las **dos ecuaciones de movimiento acopladas**, incluida la cancelación de los términos cruzados en la ecuación angular.
- [x] Reorganizar el sistema en forma matricial `M(q) q_ddot + C(q,q_dot) q_dot = τ_g(q) + B u`; identificar la matriz de masas, una elección válida de matriz de velocidad, el vector gravitatorio y la distribución de entrada.
- [x] Calcular el determinante, la adjunta y la inversa de `M(q)`; verificar algebraicamente su invertibilidad para `m_c, m_p, l > 0`.
- [x] Despejar ambas aceleraciones mediante la multiplicación matricial y la simplificación de sus numeradores `N₁` y `N₂`.
- [x] Expresar las **cuatro ecuaciones no lineales de primer orden** `s_dot = F(s,u)`.
- [x] Identificar analíticamente las configuraciones de equilibrio inferior `θ = 0` y superior `θ = π` con velocidades y fuerza nulas (para `x = 0` como posición de referencia).
- [ ] Verificar los valores físicos nominales y la correspondencia de masas, inercia, fuerzas, ejes, signos y longitudes con el MJCF. Un modelo MuJoCo con barra de masa/inercia no despreciable no tiene por qué reproducir exactamente las ecuaciones ideales.
- [ ] Comparar las aceleraciones analíticas con las calculadas por MuJoCo en varios estados y entradas, con tolerancias y resultados reproducibles.
- [ ] Comprobar conservación de energía cuando `u = 0` en el modelo ideal, y analizar pérdidas o diferencias numéricas cuando corresponda.
- [ ] Documentar errores, discrepancias físicas y limitaciones del modelo a partir de esas pruebas.

**Criterio de avance:** las aceleraciones y las propiedades energéticas calculadas con el modelo matemático se han contrastado con MuJoCo, y sus diferencias están medidas y explicadas. La derivación en papel **no equivale** a haber superado este criterio.

## 3. Estabilización local

- [x] Obtener los puntos de equilibrio y linealizar el equilibrio superior mediante jacobianos, incluyendo las matrices $A$ y $B$: [derivación](theory/02-linearization-and-stability.md).
- [x] Calcular los valores propios y demostrar la inestabilidad en lazo abierto mediante el método indirecto de Lyapunov.
- [ ] Comprobar la **controlabilidad** del par $(A,B)$.
- [ ] Elegir tiempo de muestreo y obtener el modelo discreto.
- [ ] Diseñar el LQR y justificar las ponderaciones.
- [ ] Verificar estabilidad del modelo lineal cerrado.
- [ ] Probar pequeñas desviaciones en el sistema no lineal con saturación.

**Criterio de avance:** el péndulo recupera el equilibrio en un conjunto de condiciones iniciales documentado. No confundir estabilidad local con estabilidad global.

## 4. Swing-up e integración

- [ ] Definir la energía objetivo y estudiar una ley de swing-up.
- [ ] Resolver el arranque desde reposo en el equilibrio inferior.
- [ ] Estudiar el desplazamiento del carro durante la maniobra.
- [ ] Diseñar el cambio al estabilizador con condiciones de entrada/salida e histéresis.
- [ ] Registrar fallos de captura y ajustar con criterios explícitos.

**Criterio de avance:** una ejecución reproducible va desde abajo hasta el equilibrio superior y lo mantiene. Publicar una gráfica y una demostración.

## 5. Control no lineal

- [ ] Elegir una técnica adecuada al sistema subactuado.
- [ ] Proponer una función candidata de Lyapunov y estudiar su derivada.
- [ ] Identificar hipótesis, singularidades y dominio de validez.
- [ ] Si se utiliza linealización por realimentación, justificar qué salida o dinámica se linealiza y analizar la dinámica interna.
- [ ] Comparar con swing-up + LQR usando los mismos escenarios.

**Criterio de avance:** explicar lo que el análisis garantiza y distinguirlo de lo observado en simulación.

## 6. MPC lineal

- [ ] Definir horizonte, coste, restricciones y estrategia ante problemas no factibles.
- [ ] Elegir un solver y documentar sus dependencias.
- [ ] Implementar el problema de optimización y la aplicación de la primera acción.
- [ ] Medir tiempo de cálculo y compararlo con el periodo de control.
- [ ] Evaluar fuerza y recorrido del carro, sin confundir límites solicitados con garantías fuera del modelo.

**Criterio de avance:** el controlador resuelve los escenarios acordados, registra restricciones y gestiona fallos del solver.

## 7. Extensión opcional: MPC no lineal

Incorporar predicción no lineal cuando exista una referencia lineal comprobada. Comparar coste computacional, convergencia y desempeño antes de decidir si aporta una mejora útil.

## Cómo pedir y usar la guía

Para cada paso, trae tu código, una duda o un resultado. La revisión puede centrarse en el planteamiento, las ecuaciones, el código o el diseño del experimento. Avanza con cambios pequeños y explicables; las soluciones completas se desarrollan como parte de tu trabajo.
