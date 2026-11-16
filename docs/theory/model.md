# Modelado matemático del carro-péndulo

<!-- Añade aquí tu desarrollo matemático. Para ecuaciones centradas utiliza bloques $$ ... $$. -->

## Ejemplo de escritura matemática

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
