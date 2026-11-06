# Guía de desarrollo

El objetivo es aprender implementando y explicar las decisiones con tus propias palabras. Cada etapa debe dejar una implementación pequeña, una comprobación y una nota sobre lo aprendido.

## 1. Primera simulación

- [ ] Elegir una versión de MuJoCo y documentar el entorno.
- [ ] Crear el modelo del carro y el péndulo en `models/`.
- [ ] Definir masas, inercias, longitud, gravedad y unidades.
- [ ] Comprobar los ejes y el significado de los ángulos.
- [ ] Preparar CMake y un ejecutable C++ que cargue el modelo.
- [ ] Ejecutar movimiento pasivo desde una pequeña desviación de la posición inferior.
- [ ] Guardar tiempo, posiciones y velocidades para representarlos después.

**Criterio de avance:** puedes ejecutar la simulación desde cero y explicar cada coordenada. Todavía no necesitas un controlador.

Preguntas para trabajar: ¿qué grados de libertad tiene el sistema?, ¿cuántos actuadores tiene?, ¿qué hace estable al equilibrio inferior?, ¿cómo afecta el paso de integración?

## 2. Modelo dinámico

- [ ] Derivar las ecuaciones y declarar las hipótesis: masa puntual o barra, rozamiento y ausencia/presencia de límites físicos.
- [ ] Identificar los equilibrios y elegir una convención única para el estado.
- [ ] Comparar aceleraciones calculadas con las del simulador en varios estados.
- [ ] Revisar conservación/disipación de energía con fuerza de entrada nula.

**Criterio de avance:** las diferencias entre el modelo matemático y MuJoCo están medidas y explicadas.

## 3. Estabilización local

- [ ] Linealizar alrededor del equilibrio superior y comprobar la controlabilidad.
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
