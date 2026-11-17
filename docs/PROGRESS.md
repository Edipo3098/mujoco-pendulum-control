# Registro de progreso

## 17 de noviembre de 2026 — Desarrollo del modelo matemático

### Trabajo realizado

- Incorporada la derivación inicial de velocidades, energía cinética, energía potencial y lagrangiano en [model.md](theory/model.md).
- Documentadas las coordenadas generalizadas, el orden del estado, los ejes y la convención angular: ángulo nulo con el péndulo abajo y sentido positivo antihorario.
- Mejorada la redacción en español, organizada la presentación en secciones y numerados los nueve bloques de ecuaciones como [1]–[9]. Los ejemplos de sintaxis se conservan en un apéndice.
- Revisada la consistencia del desarrollo escrito; las observaciones matemáticas siguientes permanecen abiertas. Esta actualización de estilo conserva las expresiones del autor y no añade ecuaciones.

### Observaciones pendientes de resolver

| Bloque | Observación |
| --- | --- |
| [4] | La componente horizontal de la velocidad del péndulo omite el factor de longitud que sí aparece en los desarrollos posteriores. |
| [6] | Aparece `\dot{x1}` donde el resto del documento utiliza `\dot{x}`; revisar la errata. |
| [7] | Los términos de traslación de las energías individuales `Tp` y `Tc` no tienen el cuadrado de la velocidad, aunque sí aparece en la energía total. |

Conviene distinguir tipográficamente el vector de gravedad de su magnitud escalar y unificar los subíndices de masas, velocidades y energías.

### Estado de las etapas

La preparación del entorno está documentada en [ENVIRONMENT.md](ENVIRONMENT.md). El desarrollo matemático ha avanzado hasta una expresión del lagrangiano, pero aún no está validado. No se da por terminada la etapa de modelo dinámico.

Siguen pendientes las hipótesis completas, los parámetros físicos y sus unidades, las ecuaciones de movimiento, el modelo MJCF, la configuración de compilación y la comparación con MuJoCo. No se han ejecutado pruebas de simulación ni comprobaciones de conservación de energía.

El [roadmap](ROADMAP.md) conserva sus puntos originales. Los avances parciales se describen sin marcar como terminadas tareas que todavía incluyen trabajo pendiente.
