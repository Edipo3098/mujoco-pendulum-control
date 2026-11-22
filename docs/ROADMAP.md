# Guía de desarrollo

El objetivo es aprender implementando y explicar las decisiones con tus propias palabras. Cada etapa debe dejar una implementación pequeña, una comprobación y una nota sobre lo aprendido.

## 1. Primera simulación

- [x] Elegir una versión de MuJoCo y documentar el entorno: MuJoCo / Studio 4.0.1 para Windows x64; ver [entorno de desarrollo](ENVIRONMENT.md).
- [ ] Crear el modelo del carro y el péndulo en `models/`.
- [ ] Definir masas, inercias, longitud, gravedad y unidades. Notación de masas y longitud, masa puntual del péndulo y dirección del vector de gravedad documentadas en [model.md](theory/model.md); faltan valores, unidades y restantes hipótesis.
- [x] Comprobar los ejes y el significado de los ángulos en el modelo matemático. Convención matemática definida en [model.md](theory/model.md): x hacia la derecha, y hacia arriba y θ = 0 abajo, positivo antihorario; figura corregida y coherente con la convención; falta contrastar con MuJoCo.
- [ ] Preparar CMake y un ejecutable C++ que cargue el modelo.
- [ ] Ejecutar movimiento pasivo desde una pequeña desviación de la posición inferior.
- [ ] Guardar tiempo, posiciones y velocidades para representarlos después.

**Avance en el entorno local (pendiente de incorporar y validar en el repositorio):** se ha probado un XML del Cart-Pole ideal y un módulo Python `CartPoleSimulator` con `reset`, lectura de estado, `step`, visor y cierre; también se ha ensayado la generación del XML desde parámetros YAML. Estos avances no sustituyen la validación física del MJCF ni la integración futura del control en C++.

**Criterio de avance:** puedes ejecutar la simulación desde cero y explicar cada coordenada. Todavía no necesitas un controlador.

Preguntas para trabajar: ¿qué grados de libertad tiene el sistema?, ¿cuántos actuadores tiene?, ¿qué hace estable al equilibrio inferior?, ¿cómo afecta el paso de integración?

## 2. Modelo dinámico

- [ ] Derivar las ecuaciones y declarar las hipótesis: masa puntual o barra, rozamiento y ausencia/presencia de límites físicos. Avance: velocidades, energías cinética y potencial y lagrangiano desarrollados en [model.md](theory/model.md), con bloques numerados [1]–[9]. Pendientes: revisar el factor de longitud en la velocidad horizontal del bloque [4], la errata `\dot{x1}` en [6] y los cuadrados de velocidad de `Tp` y `Tc` en [7]; completar las hipótesis y obtener las ecuaciones de movimiento.
- [x] Identificar las configuraciones de equilibrio y elegir una convención única para el estado. Orden del estado definido como [x, θ, x_dot, θ_dot]; posiciones inferior θ = 0 y superior θ = π documentadas, pendientes de verificar con las ecuaciones.
- [ ] Comparar aceleraciones calculadas con las del simulador en varios estados.
- [ ] Revisar conservación/disipación de energía con fuerza de entrada nula.

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

## 3. Estabilización local por realimentación de estado completo (C++)

**Objetivo:** mantener el péndulo cerca de \(\theta=\pi\) y llevar también \(x\), \(\dot x\) y \(\dot\theta\) hacia cero, usando únicamente la fuerza horizontal del carro.

- [x] Obtener los puntos de equilibrio y linealizar el equilibrio superior mediante jacobianos, incluyendo las matrices \(A\) y \(B\): [derivación](theory/02-linearization-and-stability.md).
- [x] Calcular los valores propios y demostrar la inestabilidad en lazo abierto mediante el método indirecto de Lyapunov.
- [ ] Comprobar la **controlabilidad** del par \((A,B)\), antes de diseñar las ganancias.
- [ ] Definir el error \(e=[x,\ \theta-\pi,\ \dot x,\ \dot\theta]^T\) y estudiar la realimentación de estado \(u=-Ke\).
- [ ] Diseñar \(K\) mediante **asignación de polos** y justificar los polos deseados, el esfuerzo de control y el desplazamiento del carro. **No empezar por LQR**.
- [ ] Analizar la estabilidad del sistema lineal en lazo cerrado; usar, cuando proceda, una función cuadrática de Lyapunov \(V=e^TPe\).
- [ ] Elegir el período de control, discretizar o justificar la implementación discreta y estudiar saturación de fuerza y sensibilidad a las condiciones iniciales.
- [ ] Implementar el controlador en **C++**, independiente del simulador; validar primero sobre el modelo matemático y después frente a MuJoCo.
- [ ] Registrar \(x(t)\), \(\theta(t)-\pi\), velocidades, fuerza, tiempo de establecimiento y condiciones iniciales para distintos ensayos.
- [ ] Como comparación **opcional y posterior**, estudiar LQR; no es un requisito para comenzar.

**Decisión:** un PID aplicado únicamente al ángulo no constituye por sí solo un controlador del **estado completo**: puede corregir la inclinación sin garantizar que el carro vuelva a \(x=0\). No será la primera estrategia de este proyecto.

**Criterio de avance:** para pequeñas perturbaciones documentadas, el estado completo converge localmente al equilibrio superior con fuerza y recorrido del carro medidos. Distinguir estabilidad del modelo lineal de la validación sobre el sistema no lineal.

## 4. Diseño de control basado en Lyapunov y estudio de Slotine

**Objetivo:** aprender a **diseñar y justificar** una ley de control, no solo a comprobar su comportamiento mediante simulaciones. Referencia de estudio: Slotine y Li, *Applied Nonlinear Control*, especialmente el método directo de Lyapunov y las técnicas de control no lineal aplicables.

- [ ] Repasar estabilidad de Lyapunov, estabilidad asintótica, dominios de atracción y diferencias entre condiciones suficientes y observaciones numéricas.
- [ ] Analizar la dinámica no lineal y la **subactuación** del Cart-Pole: dos coordenadas generalizadas y una sola entrada \(u\).
- [ ] Elegir una función candidata \(V(e)\), justificar positividad y calcular \(\dot V\) a partir de las ecuaciones del modelo.
- [ ] Estudiar si puede obtenerse una ley \(u(e)\) que garantice la condición requerida sobre \(\dot V\) **para el equilibrio completo**, sin suponer actuadores inexistentes.
- [ ] Investigar las limitaciones de *feedback linearization*: salida elegida, grado relativo y dinámica interna, antes de adoptarla.
- [ ] Implementar en **C++** solo un controlador cuya hipótesis y dominio de aplicación se hayan explicado.
- [ ] Comparar el diseño no lineal con el estabilizador por realimentación de estado en escenarios idénticos de MuJoCo.

**Criterio de avance:** presentar una ley de control junto con sus hipótesis, derivación, condiciones de estabilidad y región de validez; distinguir expresamente lo demostrado de lo observado en simulación.

## 5. MPC lineal

- [ ] Definir horizonte, coste, restricciones y estrategia ante problemas no factibles.
- [ ] Elegir un solver y documentar sus dependencias.
- [ ] Implementar el problema de optimización y la aplicación de la primera acción.
- [ ] Medir tiempo de cálculo y compararlo con el período de control.
- [ ] Evaluar fuerza y recorrido del carro, sin confundir límites solicitados con garantías fuera del modelo.

**Criterio de avance:** el controlador resuelve los escenarios acordados, registra restricciones y gestiona fallos del solver.

## 6. Extensión opcional: MPC no lineal

Incorporar predicción no lineal cuando exista una referencia lineal comprobada. Comparar coste computacional, convergencia y desempeño antes de decidir si aporta una mejora útil.

## 7. Swing-up e integración (última etapa)

**Objetivo:** llevar el péndulo desde el equilibrio inferior hasta la región de atracción de un estabilizador ya probado y mantenerlo arriba.

- [ ] Definir la energía objetivo y estudiar una ley de *swing-up*.
- [ ] Resolver el arranque desde reposo en el equilibrio inferior.
- [ ] Estudiar el desplazamiento del carro y los límites de fuerza durante la maniobra.
- [ ] Diseñar el cambio al estabilizador local con condiciones de entrada/salida e histéresis.
- [ ] Registrar fallos de captura y ajustar con criterios explícitos.
- [ ] Comparar escenarios reproducibles desde abajo hasta arriba, con registros y visualización.

**Criterio de avance:** una ejecución reproducible va desde abajo hasta el equilibrio superior y lo mantiene. Publicar una gráfica y una demostración.

## Cómo pedir y usar la guía

Para cada paso, trae tu código, una duda o un resultado. La revisión puede centrarse en el planteamiento, las ecuaciones, el código o el diseño del experimento. Avanza con cambios pequeños y explicables; las soluciones completas se desarrollan como parte de tu trabajo.
