# Física Matemática 2

El repositorio reúne desarrollos en `.tex`, versiones compiladas en PDF y scripts o notebooks en Python para visualizar mejor la estructura matemática y física de los problemas.

---

## `convolucion/`

Notebook sobre **transformada de Fourier** y **teorema de convolución**.

Archivo principal:

- `convolucion.ipynb`

El ejemplo central consiste en calcular la transformada de Fourier de

```math
f(t)=\frac{1}{(t^2+1)(t^2+4)}.
```

La idea es mostrar cómo una función racional puede tratarse usando convolución en el espacio de frecuencias.

---

## `laplace_2d_cuarto_circulo/`

Problema de la **ecuación de Laplace en un cuarto de círculo**, resuelto por separación de variables en coordenadas polares.

Se estudia

```math
\nabla^2\Psi = 0,
```

en la región

```math
0<\varphi<\frac{\pi}{2},
\qquad
a<r<b.
```

Las condiciones de borde son homogéneas en los bordes angulares y en $r=a$, mientras que en $r=b$ se impone una condición no homogénea. El desarrollo muestra cómo las condiciones de borde seleccionan los modos angulares y determinan los coeficientes de la expansión.

---

## `potencial_esfera_dirichlet/`

Problema de **Dirichlet para la ecuación de Laplace dentro de una esfera**.

Se busca un potencial

```math
\phi(r,\theta,\varphi)
```

finito en el origen y determinado por una condición de borde impuesta sobre la superficie

```math
r=R.
```

El desarrollo usa una expansión en polinomios de Legendre. Las figuras muestran cómo la condición de borde sobre la esfera fija la estructura angular del potencial.

---

## `potencial_dos_hemisferios_laplace/`

Problema electrostático para una **esfera conductora formada por dos hemisferios** separados por un anillo aislante.

La condición de borde es

```math
\phi(a,\theta)=
\begin{cases}
+V_0, & 0\leq \theta < \pi/2,\\
-V_0, & \pi/2<\theta\leq \pi.
\end{cases}
```

La solución se obtiene resolviendo la ecuación de Laplace con simetría axial,

```math
\nabla^2\phi=0.
```

El desarrollo usa una expansión en polinomios de Legendre y muestra cómo la discontinuidad en el ecuador determina qué modos contribuyen a la solución.

---

## `armonicos_esfericos_integral/`

Se relacionan algunos armónicos esféricos con las coordenadas cartesianas $x$, $y$, $z$, para estudiar integrales del tipo

```math
I=
\int_0^\pi
\int_0^{2\pi}
(x+y+2z)
Y_\ell^m(\theta,\varphi)
\sin\theta
\,d\varphi\,d\theta.
```

Las visualizaciones muestran mapas angulares sobre la esfera. La idea es identificar qué modos tienen la simetría correcta para contribuir a la integral y cuáles se anulan por ortogonalidad.

---

## `potencial_esfera_armonicos/`

Problema de potencial electrostático para un **cascarón esférico con densidad superficial de carga**

```math
\sigma(\theta,\varphi).
```

El potencial se escribe separadamente dentro y fuera del cascarón:

```math
\phi_i(r,\theta,\varphi),
\qquad
\phi_e(r,\theta,\varphi).
```

El desarrollo usa armónicos esféricos e impone la continuidad del potencial en $r=R$,

```math
\phi_i(R,\theta,\varphi)
=
\phi_e(R,\theta,\varphi),
```

junto con la discontinuidad radial asociada a la carga superficial:

```math
-\varepsilon_0
\left[
\frac{\partial \phi_e}{\partial r}
-
\frac{\partial \phi_i}{\partial r}
\right]_{r=R}
=
\sigma(\theta,\varphi).
```

Las figuras muestran la topología angular de la densidad superficial y de los modos que aparecen en la solución.

---

## `onda_2d_tambor_bessel/`

Problema de la **ecuación de onda bidimensional en un disco**, interpretado como un tambor circular con borde fijo.

La ecuación estudiada es

```math
\frac{\partial^2 \psi}{\partial t^2}
=
v^2\nabla^2\psi,
```

con condición de borde

```math
\psi(a,\varphi,t)=0.
```

Usando separación de variables en coordenadas polares, la parte radial conduce a funciones de Bessel. La condición de borde selecciona los ceros de estas funciones, de modo que la solución general queda escrita como una superposición de modos normales.

Notebook para visualizar la solución de la ecuación de onda 2D para una condición inicial arbitraria, hecho por Guillermo Rubilar. Es una excelente forma de ver la física del sistema más allá de las ecuaciones.

- `onda_disco_funcion_rara.ipynb`

---

## `calor_2d_rectangulo/`

Problema de la **ecuación de difusión del calor bidimensional en un rectángulo**, resuelto por separación de variables en coordenadas cartesianas.

Se estudia

```math
\nabla^2\psi-\frac{1}{\alpha}\frac{\partial \psi}{\partial t}=0,
```

en el dominio

```math
0<x<a,
\qquad
0<y<b,
\qquad
t\geq 0,
```

con condiciones de borde homogéneas de Dirichlet sobre los cuatro lados del rectángulo.

El desarrollo muestra cómo las condiciones de borde seleccionan una base doble de senos y cómo la condición inicial determina los coeficientes de Fourier. La carpeta incluye un notebook de apoyo visual asociado a la difusión del calor 2D, compartido por Guillermo Rubilar.

---

## `helmholtz_esfericas_msv/`

Desarrollo del **método de separación de variables para la ecuación de Helmholtz en coordenadas esféricas**.

Se estudia

```math
\nabla^2\Psi+\alpha\Psi=0,
```

usando el ansatz separable

```math
\Psi_{\mathrm{sep}}(r,\theta,\phi)=R(r)\Theta(\theta)\Phi(\phi).
```

El desarrollo muestra cómo aparecen las ecuaciones diferenciales ordinarias radial, polar y azimutal, junto con las constantes de separación asociadas a la periodicidad angular y a la estructura esférica del problema.

---

## Agradecimientos

Agradezco al profesor **Guillermo Rubilar** por facilitar desarrollos de algunos problemas y por compartir notebooks utilizados como apoyo visual en Física Matemática 2, en particular los asociados al tambor circular y a la difusión del calor 2D. Agradezco también al profesor **Félix Borotto** por facilitar algunas soluciones que sirvieron como referencia para la elaboración, revisión y adaptación de parte del material.
