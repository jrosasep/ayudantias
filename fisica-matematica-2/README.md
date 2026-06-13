# Física Matemática 2

El material está organizado por problema o tema. En general, cada carpeta contiene el desarrollo en `.tex`, el PDF compilado y, cuando corresponde, scripts o notebooks para generar visualizaciones complementarias.

## Contenido actual

### `convolucion/`

Notebook sobre **transformada de Fourier** y **teorema de convolución**.

Archivo principal:

- `convolucion.ipynb`

El notebook desarrolla el cálculo de la transformada de Fourier de una función racional del tipo

$$
f(t)=\frac{1}{(t^2+1)(t^2+4)}.
$$

### `laplace_2d_cuarto_circulo/`

Problema de la **ecuación de Laplace en un cuarto de círculo**, resuelto mediante separación de variables en coordenadas polares.

Se estudia el problema

$$
\nabla^2\Psi=0,
$$

en la región

$$
0<\varphi<\frac{\pi}{2}, \qquad a<r<b,
$$

con condiciones de borde homogéneas en los bordes angulares y en $r=a$, y una condición no homogénea en $r=b$.

### `potencial_esfera_dirichlet/`

Problema de **Dirichlet para la ecuación de Laplace dentro de una esfera**.

Se determina el potencial $\phi(r,\theta,\varphi)$, finito en el origen, a partir de una condición de borde impuesta sobre la superficie $r=R$. El desarrollo usa expansión en polinomios de Legendre y visualizaciones de la condición de borde sobre la esfera.

### `potencial_dos_hemisferios_laplace/`

Potencial electrostático de una **esfera conductora formada por dos hemisferios** separados por un anillo aislante.

El hemisferio superior se mantiene a potencial $+V_0$ y el hemisferio inferior a potencial $-V_0$. La solución se obtiene desde la ecuación de Laplace con simetría axial, usando una expansión en polinomios de Legendre.

### `armonicos_esfericos_integral/`

Identidades de **armónicos esféricos** y cálculo de una integral angular.

Se relacionan algunos armónicos esféricos con las coordenadas cartesianas $x$, $y$, $z$, para luego calcular una integral del tipo

$$
I=\int_0^\pi\int_0^{2\pi} (x+y+2z)Y_\ell^m(\theta,\varphi)\sin\theta\,d\varphi\,d\theta.
$$

Incluye mapas angulares sobre la esfera para visualizar qué modos contribuyen a la integral.

### `potencial_esfera_armonicos/`

Potencial electrostático de un **cascarón esférico con densidad superficial de carga** $\sigma(\theta,\varphi)$.

El desarrollo usa armónicos esféricos para escribir el potencial dentro y fuera del cascarón, imponiendo continuidad del potencial y la discontinuidad de la derivada radial asociada a la carga superficial.

### `onda_2d_tambor_bessel/`

Problema de la **ecuación de onda bidimensional en un disco**, interpretado como un tambor circular con borde fijo.

El desarrollo usa separación de variables en coordenadas polares. La parte radial conduce a funciones de Bessel, y la condición de borde selecciona sus ceros. La solución general queda escrita como superposición de modos normales.

Archivo complementario:

- `onda_disco_funcion_rara.ipynb`

En el notebook se puede visualizar una animación de la solución para una condición inicial arbitraria.

## Estructura típica de las carpetas

Según el problema, las carpetas pueden incluir:

- `.tex`: fuente editable del desarrollo;
- `.pdf`: versión compilada para estudio;
- `.py`: scripts para generar figuras;
- `figures/`: figuras en formato `.svg`;
- `.ipynb`: notebooks de apoyo o visualización.

## Agradecimientos

Agradezco al profesor Guillermo Rubilar por los desarrollos de algunos problemas y por compartir el notebook asociado al problema del tambor.
