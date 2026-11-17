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

El eje vertical es positivo hacia arriba. Denotamos por \(g>0\) la magnitud de la aceleración gravitatoria; su vector es:

**Ecuación [3].**

$$
\mathbf{g}=\begin{bmatrix}0\\-g\end{bmatrix}.
$$

## Análisis dinámico

### Hipótesis del modelo

Se considera un carro que se traslada horizontalmente, una barra **rígida sin masa** y una masa puntual \(m_p\) en su extremo, a distancia \(l\) del pivote. El pivote no está actuado. En esta derivación ideal no se incluyen rozamientos, límites de recorrido ni saturación del actuador; la única fuerza de control es \(u=F_x\). Se supone \(m_c>0\), \(m_p>0\), \(l>0\).

### Posición y velocidad

La posición del carro (representado a la altura del pivote) y la masa del péndulo son:

**Ecuación [4].**

$$
\mathbf r_c=\begin{bmatrix}x\\0\end{bmatrix},\qquad
\mathbf r_p=\begin{bmatrix}x+l\sin\theta\\-l\cos\theta\end{bmatrix}.
$$

Derivando respecto al tiempo y aplicando la regla de la cadena:

**Ecuación [5].**

$$
\mathbf v_c=\begin{bmatrix}\dot{x}\\0\end{bmatrix},\qquad
\mathbf v_p=\begin{bmatrix}
\dot{x}+l\dot{\theta}\cos\theta\\
l\dot{\theta}\sin\theta
\end{bmatrix}.
$$

La velocidad al cuadrado de la masa puntual es:

**Ecuación [6].**

$$
\begin{aligned}
\|\mathbf v_p\|^2
&=(\dot{x}+l\dot{\theta}\cos\theta)^2+
(l\dot{\theta}\sin\theta)^2\\
&=\dot{x}^2+2l\dot{x}\dot{\theta}\cos\theta
+l^2\dot{\theta}^2(\cos^2\theta+\sin^2\theta)\\
&=\dot{x}^2+2l\dot{x}\dot{\theta}\cos\theta+l^2\dot{\theta}^2.
\end{aligned}
$$

### Energía cinética

Para cada masa puntual utilizamos \(T=\frac12 m\|\mathbf v\|^2\). La energía cinética del carro, del péndulo y del sistema total queda:

**Ecuación [7].**

$$
\begin{aligned}
T_c&=\frac12m_c\dot{x}^2,\\
T_p&=\frac12m_p\dot{x}^2
+m_pl\dot{x}\dot{\theta}\cos\theta
+\frac12m_pl^2\dot{\theta}^2,\\
T&=T_c+T_p\\
&=\frac12(m_c+m_p)\dot{x}^2
+m_pl\dot{x}\dot{\theta}\cos\theta
+\frac12m_pl^2\dot{\theta}^2.
\end{aligned}
$$

El término cruzado no conserva un factor \(\frac12\): al desarrollar el binomio aparece \(2\dot{x}l\dot{\theta}\cos\theta\), que cancela ese factor. El término cruzado representa el acoplamiento entre traslación y rotación.

### Energía potencial

Tomando como referencia de altura el pivote, la energía potencial del carro es constante y se elige igual a cero. La de la masa puntual es \(U_p=m_pgy_p\):

**Ecuación [8].**

$$
U_c=0,\qquad U_p=-m_pgl\cos\theta,\qquad
U=-m_pgl\cos\theta.
$$

### Lagrangiano

El lagrangiano es la diferencia entre energías cinética y potencial:

**Ecuación [9].**

$$
\boxed{
\mathcal L=T-U=
\frac12(m_c+m_p)\dot{x}^2
+m_pl\dot{x}\dot{\theta}\cos\theta
+\frac12m_pl^2\dot{\theta}^2
+m_pgl\cos\theta
}
$$

## Ecuaciones de movimiento mediante Euler–Lagrange

Para cada coordenada generalizada \(q_i\), con fuerza generalizada \(Q_i\):

**Ecuación [10].**

$$
\frac{d}{dt}\left(\frac{\partial\mathcal L}{\partial\dot q_i}\right)
-\frac{\partial\mathcal L}{\partial q_i}=Q_i,
\qquad
q=\begin{bmatrix}x\\\theta\end{bmatrix},
\quad
\begin{bmatrix}Q_x\\Q_\theta\end{bmatrix}
=\begin{bmatrix}u\\0\end{bmatrix}.
$$

No se aplica un par directamente al péndulo, por lo que \(Q_\theta=0\).

### Movimiento horizontal del carro: coordenada \(x\)

El lagrangiano no depende explícitamente de la posición \(x\), pero sí de su velocidad:

**Ecuación [11].**

$$
\frac{\partial\mathcal L}{\partial x}=0,\qquad
\frac{\partial\mathcal L}{\partial\dot{x}}
=(m_c+m_p)\dot{x}+m_pl\dot{\theta}\cos\theta.
$$

La derivada temporal requiere la regla del producto y la regla de la cadena:

**Ecuación [12].**

$$
\begin{aligned}
\frac{d}{dt}\left(\frac{\partial\mathcal L}{\partial\dot{x}}\right)
&=(m_c+m_p)\ddot{x}
+m_pl\frac{d}{dt}(\dot{\theta}\cos\theta)\\
&=(m_c+m_p)\ddot{x}
+m_pl\ddot{\theta}\cos\theta
-m_pl\dot{\theta}^2\sin\theta.
\end{aligned}
$$

Sustituyendo en Euler–Lagrange se obtiene la **primera ecuación de movimiento**:

**Ecuación [13].**

$$
\boxed{
(m_c+m_p)\ddot{x}
+m_pl\cos\theta\,\ddot{\theta}
-m_pl\sin\theta\,\dot{\theta}^2=u
}
$$

### Movimiento del péndulo: coordenada \(\theta\)

Al calcular \(\partial\mathcal L/\partial\theta\), las velocidades se mantienen constantes:

**Ecuación [14].**

$$
\begin{aligned}
\frac{\partial\mathcal L}{\partial\theta}
&=-m_pl\dot{x}\dot{\theta}\sin\theta-m_pgl\sin\theta,\\
\frac{\partial\mathcal L}{\partial\dot{\theta}}
&=m_pl\dot{x}\cos\theta+m_pl^2\dot{\theta}.
\end{aligned}
$$

La derivada temporal de la segunda expresión es:

**Ecuación [15].**

$$
\frac{d}{dt}\left(\frac{\partial\mathcal L}{\partial\dot{\theta}}\right)
=m_pl\ddot{x}\cos\theta
-m_pl\dot{x}\dot{\theta}\sin\theta
+m_pl^2\ddot{\theta}.
$$

Al sustituir ambas derivadas en Euler–Lagrange, los términos \(-m_pl\dot{x}\dot{\theta}\sin\theta\) se cancelan:

**Ecuación [16].**

$$
\begin{aligned}
0={}&m_pl\ddot{x}\cos\theta
-m_pl\dot{x}\dot{\theta}\sin\theta
+m_pl^2\ddot{\theta}\\
&-\left(-m_pl\dot{x}\dot{\theta}\sin\theta-m_pgl\sin\theta\right).
\end{aligned}
$$

La **segunda ecuación de movimiento** queda:

**Ecuación [17].**

$$
\boxed{
m_pl\cos\theta\,\ddot{x}
+m_pl^2\ddot{\theta}
+m_pgl\sin\theta=0
}
$$

Dividiendo entre \(m_pl\), también puede escribirse como:

$$
\boxed{\ddot{x}\cos\theta+l\ddot{\theta}+g\sin\theta=0.}
$$

## Forma matricial del manipulador

Agrupamos los términos con aceleraciones, los dependientes de las velocidades, la gravedad y la entrada:

**Ecuación [18].**

$$
\boxed{
M(q)\ddot q+C(q,\dot q)\dot q=\tau_g(q)+Bu
}
$$

En esta notación, \(M(q)\) es la matriz de inercia; \(C(q,\dot q)\dot q\) agrupa los términos inerciales dependientes de las velocidades; \(\tau_g(q)\) es el vector de fuerzas generalizadas debidas a la gravedad **ubicado en el lado derecho**; y \(B\) distribuye la entrada \(u\). Los argumentos entre paréntesis indican de qué variables depende cada función o matriz.

### Matriz de inercia

Identificamos los coeficientes de \(\ddot{x}\) y \(\ddot{\theta}\) en las ecuaciones [13] y [17]:

**Ecuación [19].**

$$
\boxed{
M(q)=
\begin{bmatrix}
m_c+m_p & m_pl\cos\theta\\
m_pl\cos\theta & m_pl^2
\end{bmatrix}
}
$$

Es simétrica. Los términos fuera de la diagonal describen el acoplamiento dinámico entre carro y péndulo.

### Términos centrífugos/de Coriolis

El término dependiente de la velocidad en la ecuación horizontal es \(-m_pl\dot{\theta}^2\sin\theta\); la ecuación angular no tiene un término independiente de las aceleraciones de ese tipo:

**Ecuación [20].**

$$
\boxed{
C(q,\dot q)=
\begin{bmatrix}
0 & -m_pl\dot{\theta}\sin\theta\\
0 & 0
\end{bmatrix},
\qquad
C(q,\dot q)\dot q=
\begin{bmatrix}
-m_pl\dot{\theta}^2\sin\theta\\
0
\end{bmatrix}
}
$$

Esta elección de \(C\) reproduce los términos del modelo; la representación matricial de \(C\) no es única. No debe confundirse este término inercial con un rozamiento viscoso.

### Gravedad y distribución del control

La gravedad se traslada al lado derecho de [18], por lo que su signo es negativo:

**Ecuación [21].**

$$
\boxed{
\tau_g(q)=
\begin{bmatrix}
0\\-m_pgl\sin\theta
\end{bmatrix}
}
$$

La entrada es una fuerza horizontal aplicada al carro; el pivote no recibe un par de control:

**Ecuación [22].**

$$
\boxed{
B=\begin{bmatrix}1\\0\end{bmatrix},
\qquad u=F_x.
}
$$

El modelo completo puede comprobarse multiplicando sus matrices:

**Ecuación [23].**

$$
\begin{bmatrix}
m_c+m_p & m_pl\cos\theta\\
m_pl\cos\theta & m_pl^2
\end{bmatrix}
\begin{bmatrix}\ddot{x}\\\ddot{\theta}\end{bmatrix}
+
\begin{bmatrix}-m_pl\dot{\theta}^2\sin\theta\\0\end{bmatrix}
=
\begin{bmatrix}u\\-m_pgl\sin\theta\end{bmatrix}.
$$

## Despeje de las aceleraciones

Para simular la dinámica necesitamos despejar ambas aceleraciones:

$$
\ddot q=M(q)^{-1}
\left[\tau_g(q)+Bu-C(q,\dot q)\dot q\right].
$$

### Determinante, adjunta e inversa de \(M(q)\)

Aplicando \(ad-bc\) a la matriz de inercia y usando \(1-\cos^2\theta=\sin^2\theta\):

**Ecuación [24].**

$$
\begin{aligned}
\det M(q)
&=(m_c+m_p)m_pl^2-(m_pl\cos\theta)^2\\
&=m_pl^2\left[m_c+m_p(1-\cos^2\theta)\right]\\
&=\boxed{m_pl^2(m_c+m_p\sin^2\theta)}.
\end{aligned}
$$

La matriz adjunta se obtiene intercambiando los términos diagonales y negando los no diagonales:

**Ecuación [25].**

$$
\operatorname{adj}(M)=
\begin{bmatrix}
m_pl^2 & -m_pl\cos\theta\\
-m_pl\cos\theta & m_c+m_p
\end{bmatrix}.
$$

Por tanto:

**Ecuación [26].**

$$
\boxed{
M(q)^{-1}=
\frac{1}{m_pl^2(m_c+m_p\sin^2\theta)}
\begin{bmatrix}
m_pl^2 & -m_pl\cos\theta\\
-m_pl\cos\theta & m_c+m_p
\end{bmatrix}
}
$$

Como \(m_c,m_p,l>0\), el determinante es positivo para cualquier \(\theta\); la inversa existe en todas las configuraciones.

### Vector de fuerzas y multiplicación matricial

Primero calculamos el vector al que se aplica la inversa:

**Ecuación [27].**

$$
\begin{aligned}
\tau_g+Bu-C\dot q
&=\begin{bmatrix}0\\-m_pgl\sin\theta\end{bmatrix}
+\begin{bmatrix}u\\0\end{bmatrix}
-\begin{bmatrix}-m_pl\dot{\theta}^2\sin\theta\\0\end{bmatrix}\\
&=\boxed{\begin{bmatrix}
u+m_pl\dot{\theta}^2\sin\theta\\
-m_pgl\sin\theta
\end{bmatrix}}.
\end{aligned}
$$

La primera fila de la adjunta produce el numerador \(N_1\) y la segunda, \(N_2\):

**Ecuación [28].**

$$
\begin{aligned}
N_1
&=m_pl^2(u+m_pl\dot{\theta}^2\sin\theta)
+(-m_pl\cos\theta)(-m_pgl\sin\theta)\\
&=m_pl^2u+m_p^2l^3\dot{\theta}^2\sin\theta
+m_p^2gl^2\sin\theta\cos\theta,\\[5pt]
N_2
&=(-m_pl\cos\theta)(u+m_pl\dot{\theta}^2\sin\theta)
+(m_c+m_p)(-m_pgl\sin\theta)\\
&=-m_plu\cos\theta
-m_p^2l^2\dot{\theta}^2\sin\theta\cos\theta
-m_pgl(m_c+m_p)\sin\theta.
\end{aligned}
$$

Dividiendo cada numerador entre \(\det M\) y cancelando factores comunes, obtenemos el **modelo dinámico no lineal explícito**:

**Ecuación [29].**

$$
\boxed{
\ddot{x}=
\frac{
u+m_pl\dot{\theta}^2\sin\theta+
m_pg\sin\theta\cos\theta
}{
m_c+m_p\sin^2\theta
}
}
$$

$$
\boxed{
\ddot{\theta}=
-\frac{
u\cos\theta+
m_pl\dot{\theta}^2\sin\theta\cos\theta+
g(m_c+m_p)\sin\theta
}{
l(m_c+m_p\sin^2\theta)
}
}
$$

## Espacio de estados no lineal

Con el orden ya definido en [2], \(s=[x,\theta,\dot{x},\dot{\theta}]^T\), podemos convertir las dos ecuaciones diferenciales de segundo orden en cuatro de primer orden. Definimos \(s_1=x\), \(s_2=\theta\), \(s_3=\dot{x}\), \(s_4=\dot{\theta}\):

**Ecuación [30].**

$$
\boxed{
\dot{s}=
\begin{bmatrix}
s_3\\[3pt]
s_4\\[6pt]
\dfrac{u+m_pls_4^2\sin s_2+m_pg\sin s_2\cos s_2}
{m_c+m_p\sin^2s_2}\\[12pt]
-\dfrac{u\cos s_2+m_pls_4^2\sin s_2\cos s_2+
g(m_c+m_p)\sin s_2}
{l(m_c+m_p\sin^2s_2)}
\end{bmatrix}
=F(s,u).
}
$$

Los dos equilibrios verticales con el carro en \(x=0\), velocidades nulas y entrada \(u=0\) son:

- **Inferior (estable en ángulo, sin controlar):** \(s_{\mathrm{down}}=[0,0,0,0]^T\).
- **Superior (inestable):** \(s_{\mathrm{up}}=[0,\pi,0,0]^T\).

Por invariancia traslacional, otros valores constantes de \(x\) también son posiciones de equilibrio. La estabilidad inferior indicada se refiere al ángulo del péndulo; sin rozamiento, no implica estabilidad asintótica del estado completo.

La **linealización alrededor de \(\theta=\pi\)** y el diseño del controlador LQR quedan para la siguiente etapa: no forman parte de la derivación realizada aquí. Antes de contrastar este modelo con MuJoCo habrá que confirmar los parámetros, las inercias físicas, los ejes y el sentido angular del MJCF.

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
