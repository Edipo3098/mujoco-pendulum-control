# Guía de desarrollo

El objetivo es aprender implementando y explicar las decisiones con tus propias palabras. Cada etapa debe dejar una implementación pequeña, una comprobación y una nota sobre lo aprendido.

## 1. Primera simulación e infraestructura

- [x] **Preparar el entorno:** MuJoCo / Studio 4.0.1 en Windows x64, entorno virtual de Python y bindings `mujoco` comprobados. Ver [entorno de desarrollo](ENVIRONMENT.md).
- [x] **Crear el modelo MJCF ideal:** plantilla [`models/cart-pole.xml`](../models/cart-pole.xml), con carro, articulaciones `slider` y `hinge`, péndulo de masa puntual aproximada y actuador de fuerza horizontal.
- [x] **Fijar los parámetros nominales y la convención:** [`config/cartpole-parameters.yaml`](../config/cartpole-parameters.yaml) define masas, longitud y gravedad; \(\theta=0\) abajo, \(\theta=\pi\) arriba y \(s=[x,\theta,\dot x,\dot\theta]^T\). El MJCF introduce una inercia rotacional residual \(10^{-8}\ \mathrm{kg\,m^2}\); esta aproximación deberá cuantificarse en la etapa 2.
- [x] **Generar el XML desde YAML:** [`CartPoleModelBuilder`](../scripts/model/build_model.py) transfiere masa del carro, masa del péndulo, longitud (centro de masas y geometrías visuales) y gravedad. Guarda `models/cartpole_generated.xml` y devuelve su ruta.
- [x] **Implementar el simulador reutilizable en Python:** [`CartPoleSimulator`](../scripts/mujoco/simulation.py) carga el MJCF, permite reiniciar el tiempo y las condiciones iniciales, consultar el estado, aplicar fuerza con `step(force)`, visualizar y cerrar.
- [x] **Comprobar la estructura y reinicio:** prueba comunicada por el autor con 2 grados de libertad, 1 actuador, tiempo inicial cero y lectura del estado \((0.2,\pi,0.1,0)\).
- [x] **Ejecutar y visualizar movimiento pasivo:** ensayo comunicado desde \(\theta=\pi+1^\circ\), sin control, con paso físico de 1 ms, cámara configurable y reproducción ralentizada.
- [x] **Separar el punto de entrada:** [`scripts/mujoco/simulation_example.py`](../scripts/mujoco/simulation_example.py) importa el generador y el simulador. Permite ejecutar desde la raíz: `python -m scripts.mujoco.simulation_example`.
- [x] **Comprobar la generación del XML con distintos parámetros YAML:** el autor confirma que el XML generado carga y refleja correctamente masas, gravedad, centros de masas y geometrías. Esta verificación funcional se da por completada; no se presupone que exista una suite automatizada de regresión.
- [ ] **Completar la reproducibilidad del entorno:** fijar y documentar dependencias Python, instrucciones de instalación y ejecución independientes de VS Code; decidir y versionar una configuración de ejecución portable. Actualmente `.gitignore` excluye `.vscode/`.
- [ ] **Preparar CMake y el ejecutable C++ de MuJoCo:** compilar, enlazar, cargar el modelo y ejecutar pasos de física. Esta será la base de los controladores C++.
- [ ] **Probar también el movimiento pasivo desde una perturbación pequeña del equilibrio inferior** \(\theta=0\), además de los ensayos del superior.
- [ ] **Registrar trazas reproducibles** con tiempo, posición del carro, ángulo, velocidades y fuerza (por ejemplo CSV), y representarlas con Python.

**Estado de la etapa:** existen y están versionados el MJCF, el generador YAML→XML, el módulo Python del simulador y su ejemplo de uso. El autor confirma las pruebas funcionales de generación del XML con distintos parámetros, así como las pruebas del visor y del reinicio. **No constan pruebas automatizadas de regresión ni una validación cuantitativa frente al modelo analítico.** Las tareas restantes de infraestructura pueden completarse de forma incremental; el siguiente estudio teórico será la **controlabilidad**, seguido de la **realimentación de estado con asignación de polos** (etapa 3).

**Criterio de avance:** modelo parametrizable y ejecutable, estados registrables, ejecución reproducible y primera integración C++ con MuJoCo. La validación de la dinámica física corresponde a la etapa 2.

## 2. Modelo dinámico

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

## 3. Primer controlador: realimentación de estado y asignación de polos (C++)

**Objetivo:** recuperar de forma gradual el diseño de control por realimentación del estado completo, antes de estudiar LQR. Queremos estabilizar \(s_e=[0,\pi,0,0]^T\), incluyendo la posición y velocidad del carro.

- [x] Obtener los equilibrios y los jacobianos \(A\) y \(B\) del equilibrio superior: [derivación](theory/02-linearization-and-stability.md).
- [x] Calcular los valores propios de lazo abierto y demostrar la inestabilidad del equilibrio superior por el método indirecto de Lyapunov.
- [ ] **Reproducir la prueba de controlabilidad:** formar \(\mathcal C=[B,\ AB,\ A^2B,\ A^3B]\), calcular su rango y explicar por qué \(\operatorname{rank}(\mathcal C)=4\) permite asignar polos. Para los parámetros nominales, \(\det(\mathcal C)\approx -1539.7776\ne0\); la comprobación analítica/numerica debe formar parte del experimento documentado.
- [ ] Definir el estado de error \(e=[x,\theta-\pi,\dot x,\dot\theta]^T\) y derivar la dinámica en lazo cerrado con \(u=-Ke\).
- [ ] Elegir polos cerrados deseados, calcular \(K\) mediante **asignación de polos** y estudiar los valores propios de \(A-BK\).
- [ ] Explicar por qué este controlador estabiliza **localmente el estado completo** y por qué un PID aplicado solo al ángulo no garantiza \(x\to0\).
- [ ] Definir período de control, límites de fuerza y saturación, y observar su efecto sobre el desempeño.
- [ ] Implementar el controlador de realimentación en **C++**, separado de MuJoCo, y conectarlo con el simulador C++.
- [ ] Probar perturbaciones pequeñas del equilibrio superior con el modelo no lineal y MuJoCo, registrando estados, fuerza, tiempo de establecimiento y errores.

**Criterio de avance:** poder deducir \(u=-Ke\), explicar y reproducir el cálculo de \(K\), y verificar estabilización **local** de las cuatro variables para perturbaciones documentadas. La asignación de polos es una técnica de realimentación de estado completo y sí es viable para el Cart-Pole ideal linealizado controlable.

## 4. LQR: elección óptima de las ganancias de estado (C++)

**Objetivo:** partir de la misma arquitectura \(u=-Ke\) que ya funciona y estudiar una forma sistemática de calcular \(K\) mediante un criterio cuadrático.

- [ ] Comprender la función de coste \(J=\int_0^\infty(e^TQe+u^TRu)\,dt\), los pesos \(Q,R\), la ecuación algebraica de Riccati y el cálculo de la ganancia \(K\).
- [ ] Comprobar que \(A-BK\) es Hurwitz, justificar la estabilidad del modelo lineal y estudiar la relación con Lyapunov.
- [ ] Evaluar el compromiso entre error angular, posición del carro, velocidad, esfuerzo de control y saturación.
- [ ] Elegir período de muestreo y distinguir correctamente LQR continuo de LQR discreto cuando corresponda.
- [ ] Implementar LQR en **C++** y probarlo en los mismos escenarios no lineales y de MuJoCo utilizados para la asignación de polos.
- [ ] Comparar cuantitativamente ambos métodos sobre condiciones iniciales, restricciones y métricas idénticas.

**Criterio de avance:** implementar un segundo estabilizador local basado en **la misma realimentación de estado**, explicando de dónde sale \(K\) y las diferencias reales frente a asignación de polos.

## 5. Linealización por realimentación (*feedback linearization*)

**Objetivo:** estudiar si una transformación no lineal de la entrada puede simplificar la dinámica y qué se pierde al hacerlo en un sistema **subactuado** (dos coordenadas y una sola fuerza).

- [ ] Revisar las ecuaciones no lineales y expresar el sistema en la forma afín \(\dot s=f(s)+g(s)u\).
- [ ] Elegir y justificar una salida (por ejemplo, \(x\) o \(\theta\)); calcular derivadas temporales, grado relativo y ley de linealización entrada–salida cuando sea válida.
- [ ] Calcular la **dinámica interna o dinámica cero** y estudiar su estabilidad alrededor del equilibrio superior; identificar singularidades y dominio de validez.
- [ ] Determinar si el controlador obtenido estabiliza realmente **las cuatro variables** o solo la salida elegida. No suponer que linealizar una salida equivale a estabilizar todo el sistema.
- [ ] **Punto de decisión:** si la dinámica interna no permite la estabilización requerida, documentar la limitación y **no invertir tiempo en implementar esa ley como controlador completo**. Conservar el estudio teórico.
- [ ] Solo si se justifica, implementar una alternativa útil en C++ y compararla con LQR bajo condiciones idénticas.

**Criterio de avance:** explicar con ecuaciones qué dinámica se linealiza, cuál permanece interna y por qué el método es o no adecuado para nuestro objetivo.

## 6. Control no lineal y diseño basado en Lyapunov (Slotine)

**Objetivo:** diseñar o analizar una ley para el Cart-Pole no lineal utilizando el método directo de Lyapunov, con atención a la subactuación. Referencia: Slotine y Li, *Applied Nonlinear Control*.

- [ ] Estudiar estabilidad, estabilidad asintótica, invariancia, región de atracción y diferencias entre garantías locales y globales.
- [ ] Proponer una función candidata \(V(e)\) apropiada para el **estado completo** y justificar cuándo es definida positiva.
- [ ] Calcular \(\dot V\) usando la dinámica no lineal; investigar cómo puede influir la fuerza \(u\) en su signo sin asumir un actuador en la bisagra.
- [ ] Estudiar las posibilidades de diseño (por ejemplo funciones de Lyapunov de control, enfoques basados en energía o pasividad), sus hipótesis y posibles restricciones.
- [ ] **Punto de decisión:** si no se obtiene una ley con garantías útiles para nuestro objetivo, documentarlo sin convertirla forzosamente en un controlador de simulación.
- [ ] Implementar en **C++** el diseño que resulte justificable y contrastarlo con LQR, incluyendo saturación, perturbaciones y región de funcionamiento.

**Criterio de avance:** presentar \(V\), \(\dot V\), ley de control, hipótesis y conclusión matemática; distinguir inequívocamente lo demostrado de lo observado en MuJoCo.

## 7. MPC lineal

**Objetivo:** estabilizar el estado superior incorporando explícitamente restricciones de fuerza y desplazamiento, usando un modelo discreto.

- [ ] Obtener \((A_d,B_d)\), definir período de muestreo, horizonte, referencias y restricciones de \(x\) y \(u\).
- [ ] Establecer el coste, estudiar factibilidad y elegir un solver adecuado para la integración en C++.
- [ ] Implementar el optimizador y aplicar únicamente la primera entrada en cada iteración.
- [ ] Medir tiempo de cálculo, comportamiento ante soluciones no factibles y cumplimiento de restricciones.
- [ ] Comparar con LQR sobre los mismos estados iniciales, modelo no lineal y límites de actuador.

**Criterio de avance:** comportamiento reproducible con restricciones documentadas, solver estable y coste computacional compatible con el período de control.

## 8. MPC no lineal (NMPC)

**Objetivo:** estudiar si la predicción con el modelo no lineal mejora el rango operativo o el cumplimiento de los objetivos frente al MPC lineal.

- [ ] Definir la dinámica discreta no lineal, coste, restricciones y método de integración.
- [ ] Estudiar optimización no convexa, inicialización del solver, convergencia y tratamiento de fallos.
- [ ] Implementar un prototipo y, si los resultados justifican el coste, integrarlo con el controlador C++.
- [ ] Comparar NMPC, MPC lineal y LQR con condiciones iniciales, perturbaciones, restricciones y criterios idénticos.
- [ ] Medir tiempo de optimización, calidad de solución y fallos, sin atribuir garantías globales a una validación numérica local.

**Criterio de avance:** justificar con datos cuándo NMPC aporta valor y cuándo su complejidad no compensa. Esta etapa se abordará **después** del MPC lineal.

## 9. Swing-up e integración (última etapa)

**Objetivo:** partir del equilibrio inferior, llevar el péndulo hasta la región de captura del estabilizador superior y mantener **el estado completo** cerca del objetivo.

- [ ] Definir energía objetivo y diseñar una ley de *swing-up* compatible con una sola fuerza horizontal.
- [ ] Resolver el arranque desde reposo en el equilibrio inferior y evaluar saturación de fuerza y recorrido del carro.
- [ ] Establecer una región de captura basada en las limitaciones observadas de los estabilizadores ya probados.
- [ ] Diseñar la conmutación con condiciones de entrada/salida e histéresis para evitar cambios repetidos.
- [ ] Validar ensayos reproducibles desde abajo hasta arriba, incluyendo fallos de captura, perturbaciones y métricas.
- [ ] Publicar gráficas y una demostración de la integración completa.

**Criterio de avance:** ejecución reproducible desde \(\theta=0\) hasta \(\theta\approx\pi\), con convergencia del carro y el péndulo al equilibrio objetivo dentro de los límites declarados.

## Cómo pedir y usar la guía

Para cada paso, trae tu código, una duda o un resultado. La revisión puede centrarse en el planteamiento, las ecuaciones, el código o el diseño del experimento. Avanza con cambios pequeños y explicables; las soluciones completas se desarrollan como parte de tu trabajo.
