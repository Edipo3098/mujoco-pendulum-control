# Modelado matemático del carro-péndulo

Este documento presenta las convenciones del sistema y el desarrollo de su modelo matemático.

## Coordenadas y parámetros del modelo

![Esquema del carro-péndulo y sus variables](../media/cart-pendulum-coordinates.png?v=fc411248)

La figura resume los ejes y las variables utilizados. **Convención angular: $\theta=0$ corresponde al péndulo hacia abajo.** Se adopta el sentido positivo antihorario indicado en el texto de la figura, visto en el plano del dibujo.

| Símbolo | Definición |
| --- | --- |
| $x$ | Posición horizontal del carro, positiva hacia la derecha |
| $y$ | Eje vertical, positivo hacia arriba |
| $\theta$ | Ángulo desde la vertical inferior, positivo antihorario |
| $l$ | Longitud desde el pivote hasta la masa puntual del péndulo |
| $m_c$ | Masa del carro |
| $m_p$ | Masa del péndulo, concentrada en el extremo |
| $u$ | Fuerza horizontal aplicada al carro, positiva hacia la derecha |

Tomando el pivote como referencia vertical ($y=0$), la posición de la masa puntual es:

**Ecuación [1].**

$$
x_p=x+l\sin\theta,\qquad y_p=-l\cos\theta.
$$

Así, $\theta=\pi/2$ sitúa el péndulo horizontal hacia la derecha.

Coordenadas generalizadas y orden del estado:

**Ecuación [2].**

$$
q=\begin{bmatrix}x\\\theta\end{bmatrix},
\qquad
s=\begin{bmatrix}x\\\theta\\\dot{x}\\\dot{\theta}\end{bmatrix}.
$$

El sistema tiene dos coordenadas generalizadas y una entrada de fuerza sobre el carro. La articulación del péndulo no está actuada.

Con esta convención, las posiciones verticales corresponden a $\theta=0$ (inferior) y $\theta=\pi$ (superior), módulo $2\pi$. En reposo, $\dot{x}=\dot{\theta}=0$; la comprobación de equilibrio deberá hacerse con las ecuaciones y el modelo MuJoCo.

La masa puntual del péndulo está definida en la figura. Quedan pendientes los valores de masas y longitud, la gravedad, las unidades, el tratamiento de la masa/inercia de la barra, el rozamiento y los límites físicos. También falta contrastar ejes y signos con el modelo MJCF.

## Aceleración de la gravedad

El vector de aceleración gravitatoria se expresa en los ejes definidos anteriormente:

**Ecuación [3].**

$$
g=\begin{bmatrix}0\\-g
\end{bmatrix},
$$

La notación $\dot{x}$ y $\dot{\theta}$ representa las derivadas temporales de las coordenadas generalizadas.

## Análisis dinámico

### Energía cinética

En primer lugar, se expresan las velocidades del carro y de la masa del péndulo:

**Ecuación [4].**

$$
\begin{gathered}
Vcar = \begin{bmatrix} \dot{x} \\ 0 \end{bmatrix} \\
Vpole = \begin{bmatrix} \dot{x} + \dot{\theta}\cos{\theta} \\ l\dot{\theta}\sin{\theta}\end{bmatrix}
\end{gathered}
$$

La energía cinética se calcula a partir de la masa y del módulo de la velocidad:

**Ecuación [5].**

$$
T =  \frac{1}{2}m||V||^2,
$$

**Ecuación [6].**

$$
\begin{gathered}
Vp^2 =  \dot{x}^2  + (\dot{\theta}l\cos{\theta})^2 +  2\dot{x1}(\dot{\theta}l\cos{\theta})  + (\dot{\theta}l\sin{\theta})^2,\\
Vp^2 =  \dot{x}^2  +  2\dot{x}(\dot{\theta}l\cos{\theta})  + (\dot{\theta}^2l^2),
\end{gathered}
$$

**Ecuación [7].**

$$
\begin{gathered}
Tp = \frac{1}{2}mp\dot{x} +  mp\dot{x}(\dot{\theta}l\cos{\theta})  + \frac{1}{2}mp(\dot{\theta}^2l^2), \\
Tc =  \frac{1}{2}mc\dot{x} \\
T = \frac{1}{2}(mc+mp)\dot{x}^2 +  mp\dot{x}\dot{\theta}l\cos{\theta}  + \frac{1}{2}mp(\dot{\theta}^2l^2),
\end{gathered}
$$

### Energía potencial

Tomando el nivel del pivote como referencia de altura, se expresan las contribuciones de energía potencial del carro y del péndulo:

**Ecuación [8].**

$$
\begin{gathered}
U = mgh,\\
Uc = 0, \\
Up = mpg(-l\cos{\theta})
\end{gathered}
$$

### Lagrangiano

El lagrangiano se obtiene como la diferencia entre la energía cinética y la energía potencial:

**Ecuación [9].**

$$
\begin{gathered}
\mathcal{L} = T -U,\\
\mathcal{L} = \frac{1}{2}(mc+mp)\dot{x}^2 +  mp\dot{x}\dot{\theta}l\cos{\theta}  + \frac{1}{2}mp(\dot{\theta}^2l^2) +mpg(l\cos{\theta})
\end{gathered}
$$

## Apéndice: ejemplos de escritura matemática

Este ejemplo solo muestra la sintaxis; no representa la dinámica del carro-péndulo.

Escribe lo siguiente para obtener una ecuación centrada:

```latex
$$
f(\theta) = a\cos^2(\theta) + b\sin(\theta)
$$
```

Resultado:

$$
f(\theta) = a\cos^2(\theta) + b\sin(\theta)
$$

Para una matriz multiplicada por un vector:

```latex
$$
A(\theta)\,q =
\begin{bmatrix}
1 & \cos(\theta) \\
\cos(\theta) & 1 + \cos^2(\theta)
\end{bmatrix}
\begin{bmatrix}
x \\
\theta
\end{bmatrix}
$$
```

Resultado:

$$
A(\theta)\,q =
\begin{bmatrix}
1 & \cos(\theta) \\
\cos(\theta) & 1 + \cos^2(\theta)
\end{bmatrix}
\begin{bmatrix}
x \\
\theta
\end{bmatrix}
$$

Referencias rápidas:

- `\cos^2(\theta)`: coseno al cuadrado.
- `\theta`: letra griega theta.
- `\dot{x}` y `\ddot{x}`: primera y segunda derivadas temporales.
- `\frac{a}{b}`: fracción.
- `m_{11}`: subíndice.
- Dentro de una matriz, `&` separa columnas y `\\` separa filas.
- Usa `$x(t)$` para una expresión dentro de una frase y `$$ ... $$` para una ecuación centrada.
