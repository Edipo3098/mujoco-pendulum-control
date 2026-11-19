# 02 — Linearization and Lyapunov's Indirect Method

Este documento continúa [01 — Dynamic Models](01-dynamic-models.md). Linealizamos el **modelo ideal no lineal** del Cart-Pole alrededor del equilibrio superior, obtenemos los jacobianos, estudiamos sus valores propios y aplicamos el **método indirecto de Lyapunov**.

**Alcance:** resultados analíticos de un carro y un péndulo modelado como masa puntual en el extremo de una barra rígida sin masa. No son resultados de simulación ni de un controlador implementado. Los parámetros numéricos son nominales y provisionales.

## 1. Modelo de partida y convención

Definimos el estado, la fuerza horizontal y las funciones dinámicas como:

**Ecuación [31].**

$$
s=\begin{bmatrix}x\cr\theta\cr\dot{x}\cr\dot{\theta}\end{bmatrix},
\qquad
\dot{s}=F(s,u)=
\begin{bmatrix}f_1\cr f_2\cr f_3\cr f_4\end{bmatrix}.
$$

Con $\theta=0$ hacia abajo y $\theta=\pi$ hacia arriba, las ecuaciones [29]–[30] de [01 — Dynamic Models](01-dynamic-models.md) dan:

$$
\begin{gathered}
f_1=\dot{x},\qquad f_2=\dot{\theta},\cr
f_3=\dfrac{u+m_pl\dot{\theta}^2\sin\theta+m_pg\sin\theta\cos\theta}{m_c+m_p\sin^2\theta},\cr
f_4=-\dfrac{u\cos\theta+m_pl\dot{\theta}^2\sin\theta\cos\theta+g(m_c+m_p)\sin\theta}{l(m_c+m_p\sin^2\theta)}.
\end{gathered}
$$

Se supone $m_c>0$, $m_p>0$, $l>0$ y $g>0$.

## 2. Determinación de los equilibrios

Un par $(s_e,u_e)$ es un equilibrio estacionario si $F(s_e,u_e)=0$. Por tanto, $\dot{x}_e=\dot{\theta}_e=\ddot{x}_e=\ddot{\theta}_e=0$.

Al sustituir estas condiciones en las ecuaciones de Euler–Lagrange [13] y [17] obtenemos:

$$
u_e=0,\qquad m_pgl\sin\theta_e=0.
$$

Como $m_pgl>0$, se deduce $\theta_e=k\pi$ ($k\in\mathbb{Z}$). Módulo $2\pi$ hay dos orientaciones:

**Ecuación [32].**

$$
s_{\mathrm{down}}=\begin{bmatrix}x_e\cr0\cr0\cr0\end{bmatrix},
\qquad
s_{\mathrm{up}}=\begin{bmatrix}x_e\cr\pi\cr0\cr0\end{bmatrix},
\qquad
u_e=0.
$$

La posición horizontal $x_e$ puede ser cualquier constante porque el modelo ideal no depende explícitamente de $x$. Seleccionamos el equilibrio superior $s_{\mathrm{up}}$ para la linealización.

## 3. Perturbaciones y Taylor de primer orden

Las perturbaciones son diferencias exactas respecto al equilibrio:

**Ecuación [33].**

$$
\delta s=s-s_{\mathrm{up}}
=\begin{bmatrix}x-x_e\cr\theta-\pi\cr\dot{x}\cr\dot{\theta}\end{bmatrix},
\qquad
\delta u=u-u_e=u.
$$

Como el equilibrio es constante, $\delta\dot{s}=\dot{s}$. La expansión multivariable alrededor de $(s_{\mathrm{up}},u_e)$ es:

**Ecuación [34].**

$$
\begin{gathered}
F(s_{\mathrm{up}}+\delta s,u_e+\delta u)
=F(s_{\mathrm{up}},u_e)+A\delta s+B\delta u+R(\delta s,\delta u),\cr
A=\left.\dfrac{\partial F}{\partial s}\right|_{s_{\mathrm{up}},u_e},
\qquad
B=\left.\dfrac{\partial F}{\partial u}\right|_{s_{\mathrm{up}},u_e}.
\end{gathered}
$$

El término constante es cero por la condición de equilibrio. En este modelo suave el resto $R$ es de orden al menos cuadrático cerca del equilibrio. Al despreciarlo se obtiene el **modelo local lineal**:

$$
\boxed{\delta\dot{s}=A\delta s+B\delta u.}
$$

La transformación de coordenadas es exacta; **la aproximación** está en descartar los términos de orden superior de Taylor.

## 4. Cálculo de los jacobianos

Las funciones $f_1=\dot{x}$ y $f_2=\dot{\theta}$ proporcionan las dos primeras filas:

$$
\begin{bmatrix}
\dfrac{\partial f_1}{\partial s}\cr
\dfrac{\partial f_2}{\partial s}
\end{bmatrix}
=
\begin{bmatrix}0&0&1&0\cr0&0&0&1\end{bmatrix}.
$$

Las aceleraciones $f_3$ y $f_4$ no dependen explícitamente de $x$ ni de $\dot{x}$, por lo que las derivadas respecto a esas variables son cero.

### 4.1. Aceleración horizontal

Definimos el numerador y denominador de $f_3=N_3/D_3$:

$$
\begin{gathered}
N_3=u+m_pl\dot{\theta}^2\sin\theta+m_pg\sin\theta\cos\theta,\cr
D_3=m_c+m_p\sin^2\theta.
\end{gathered}
$$

Aplicando las reglas del producto y del cociente:

**Ecuación [35].**

$$
\begin{gathered}
N_3'=m_pl\dot{\theta}^2\cos\theta+m_pg(\cos^2\theta-\sin^2\theta),\cr
D_3'=2m_p\sin\theta\cos\theta,\cr
\dfrac{\partial f_3}{\partial\theta}=\dfrac{N_3'D_3-N_3D_3'}{D_3^2},\cr
\dfrac{\partial f_3}{\partial\dot{\theta}}=\dfrac{2m_pl\dot{\theta}\sin\theta}{D_3},\qquad
\dfrac{\partial f_3}{\partial u}=\dfrac{1}{D_3}.
\end{gathered}
$$

Evaluando **después de derivar** en $\theta_e=\pi$, $\dot{\theta}_e=0$ y $u_e=0$:

$$
N_3=0,\quad N_3'=m_pg,\quad D_3=m_c,\quad D_3'=0.
$$

Por consiguiente:

$$
\left.\dfrac{\partial f_3}{\partial\theta}\right|_e=\dfrac{m_pg}{m_c},
\qquad
\left.\dfrac{\partial f_3}{\partial\dot{\theta}}\right|_e=0,
\qquad
\left.\dfrac{\partial f_3}{\partial u}\right|_e=\dfrac{1}{m_c}.
$$

### 4.2. Aceleración angular

En $f_4=-N_4/D_4$ hay un **signo negativo exterior** que debe conservarse:

$$
\begin{gathered}
N_4=u\cos\theta+m_pl\dot{\theta}^2\sin\theta\cos\theta+g(m_c+m_p)\sin\theta,\cr
D_4=l(m_c+m_p\sin^2\theta).
\end{gathered}
$$

Las derivadas necesarias son:

**Ecuación [36].**

$$
\begin{gathered}
N_4'=-u\sin\theta+m_pl\dot{\theta}^2(\cos^2\theta-\sin^2\theta)+g(m_c+m_p)\cos\theta,\cr
D_4'=2lm_p\sin\theta\cos\theta,\cr
\dfrac{\partial f_4}{\partial\theta}=-\dfrac{N_4'D_4-N_4D_4'}{D_4^2},\cr
\dfrac{\partial f_4}{\partial\dot{\theta}}=-\dfrac{2m_pl\dot{\theta}\sin\theta\cos\theta}{D_4},\qquad
\dfrac{\partial f_4}{\partial u}=-\dfrac{\cos\theta}{D_4}.
\end{gathered}
$$

En el equilibrio superior:

$$
N_4=0,\quad N_4'=-g(m_c+m_p),\quad D_4=lm_c,\quad D_4'=0.
$$

Por tanto:

$$
\left.\dfrac{\partial f_4}{\partial\theta}\right|_e=\dfrac{g(m_c+m_p)}{lm_c},
\qquad
\left.\dfrac{\partial f_4}{\partial\dot{\theta}}\right|_e=0,
\qquad
\left.\dfrac{\partial f_4}{\partial u}\right|_e=\dfrac{1}{lm_c}.
$$

## 5. Matrices linealizadas

Agrupando los jacobianos evaluados en el equilibrio superior:

**Ecuación [37].**

$$
\boxed{
A=\begin{bmatrix}
0&0&1&0\cr
0&0&0&1\cr
0&\dfrac{m_pg}{m_c}&0&0\cr
0&\dfrac{g(m_c+m_p)}{lm_c}&0&0
\end{bmatrix},
\qquad
B=\begin{bmatrix}
0\cr
0\cr
\dfrac{1}{m_c}\cr
\dfrac{1}{lm_c}
\end{bmatrix}.
}
$$

Las dimensiones son $A\in\mathbb{R}^{4\times4}$ y $B\in\mathbb{R}^{4\times1}$. Aunque $u_e=0$, **no** se anula la perturbación de control $\delta u$: representa la fuerza con la que el futuro controlador modificará la dinámica.

## 6. Estabilidad local y método indirecto de Lyapunov

En **lazo abierto** fijamos $\delta u=0$, con lo cual $\delta\dot{s}=A\delta s$.

El método indirecto de Lyapunov para un sistema no lineal continuamente diferenciable alrededor de un equilibrio afirma:

- Si todos los valores propios del jacobiano tienen parte real estrictamente negativa, el equilibrio no lineal es localmente asintóticamente estable.
- Si alguno tiene parte real estrictamente positiva, el equilibrio no lineal es inestable.
- Si no hay partes reales positivas y al menos una es cero, el jacobiano por sí solo no determina la estabilidad del equilibrio no lineal.

La ecuación característica para [37] es:

**Ecuación [38].**

$$
\det(\lambda I-A)
=\lambda^2\left(\lambda^2-\dfrac{g(m_c+m_p)}{lm_c}\right)=0.
$$

De ella obtenemos:

**Ecuación [39].**

$$
\boxed{
\lambda_1=\lambda_2=0,\qquad
\lambda_3=+\sqrt{\dfrac{g(m_c+m_p)}{lm_c}},\qquad
\lambda_4=-\sqrt{\dfrac{g(m_c+m_p)}{lm_c}}.
}
$$

Las dos raíces cero están asociadas a la traslación libre del carro y su deriva sin fuerza restauradora. La raíz negativa representa un modo decreciente y la positiva un modo creciente. Como $m_c,m_p,l,g>0$, **$\lambda_3>0$**: queda demostrado que el equilibrio superior es **inestable para el modelo no lineal original en lazo abierto**. Las raíces cero no invalidan esta conclusión.

Este resultado **no** prueba controlabilidad, estabilización mediante realimentación ni estabilidad global.

## 7. Ejemplo numérico provisional

Usamos los parámetros nominales propuestos en [config/cartpole-parameters.yaml](../../config/cartpole-parameters.yaml), pendientes de implementar y validar en MuJoCo:

| Parámetro | Valor nominal | Unidad |
| --- | ---: | --- |
| $m_c$ | 1.0 | kg |
| $m_p$ | 0.1 | kg |
| $l$ | 0.5 | m |
| $g$ | 9.81 | m/s² |

Así, las matrices numéricas son:

**Ecuación [40].**

$$
A_{\mathrm{nom}}=
\begin{bmatrix}
0&0&1&0\cr
0&0&0&1\cr
0&0.981&0&0\cr
0&21.582&0&0
\end{bmatrix},
\qquad
B_{\mathrm{nom}}=
\begin{bmatrix}0\cr0\cr1\cr2\end{bmatrix}.
$$

$$
\lambda_{\mathrm{nom}}=
\{0,0,+\sqrt{21.582},-\sqrt{21.582}\}
\approx\{0,0,+4.6456,-4.6456\}\ \mathrm{s}^{-1}.
$$

**Estos números son de referencia**, no mediciones del sistema ni resultados obtenidos ejecutando MuJoCo. Las expresiones simbólicas y la conclusión de inestabilidad no dependen de estos valores concretos.

## 8. Límites y siguientes pasos

Las coordenadas de perturbación describen exactamente las desviaciones, pero las matrices linealizadas solo aproximan localmente las aceleraciones del modelo no lineal. No se ha establecido un dominio angular de precisión ni una validación con MuJoCo.

Quedan pendientes: contrastar el MJCF y los parámetros físicos con el modelo ideal, comparar aceleraciones no lineales y linealizadas para diferentes perturbaciones, estudiar la **controlabilidad** del par $(A,B)$ y diseñar el controlador LQR.

Referencia conceptual: Slotine y Li, *Applied Nonlinear Control*, capítulo 3, método indirecto de Lyapunov.
