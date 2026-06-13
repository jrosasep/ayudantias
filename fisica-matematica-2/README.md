# Física Matemática 2

Carpeta destinada a reunir material de ayudantías de **Física Matemática 2**.
## Contenido actual

### `convolucion/`

Carpeta dedicada a ejemplos sobre **transformada de Fourier** y **teorema de convolución**.

Contiene el notebook:

- `convolucion.ipynb`

Este notebook desarrolla un ejemplo del uso del **teorema de convolución** para calcular la transformada de Fourier de una función racional del tipo

$$
f(t)=\frac{1}{(t^2+1)(t^2+4)}.
$$

### `laplace_2d_cuarto_circulo/`

Carpeta dedicada al problema de la **ecuación de Laplace en un cuarto de círculo**, resuelto mediante el **método de separación de variables** en coordenadas polares.

El problema consiste en resolver

$$
\nabla^2\Psi=0
$$

en una región de la forma

$$
0<\varphi<\frac{\pi}{2}, \qquad a<r<b,
$$

con condiciones de borde homogéneas en los bordes angulares y en $r=a$, y una condición no homogénea en $r=b$.

La carpeta contiene el desarrollo en `.tex`, el PDF compilado, el script de visualización y figuras en formato `.svg`.

### `potencial_esfera_dirichlet/`

Carpeta dedicada a un problema de **Dirichlet para la ecuación de Laplace dentro de una esfera**.

Se determina el potencial $\phi(r,\theta,\varphi)$, finito en el origen, que satisface una condición de borde impuesta sobre la superficie esférica $r=R$.

El desarrollo usa la expansión en polinomios de Legendre y permite visualizar cómo la condición de borde sobre la esfera determina los coeficientes de la solución interior.

La carpeta contiene el desarrollo en `.tex`, el PDF compilado, el script de visualización y figuras en formato `.svg`.

### `potencial_dos_hemisferios_laplace/`

Carpeta dedicada al potencial electrostático de una **esfera conductora formada por dos hemisferios** separados por un anillo aislante.

El hemisferio superior se mantiene a potencial $+V_0$ y el hemisferio inferior a potencial $-V_0$. El problema se resuelve mediante la ecuación de Laplace con simetría axial y una expansión en polinomios de Legendre.

La carpeta contiene el desarrollo en `.tex`, el PDF compilado, el script de visualización y figuras en formato `.svg`.

### `armonicos_esfericos_integral/`

Carpeta dedicada a identidades de **armónicos esféricos** y al cálculo de una integral angular.

El material desarrolla la relación entre algunos armónicos esféricos y las coordenadas cartesianas $x$, $y$, $z$, para luego calcular una integral del tipo

$$
I=\int_0^\pi\int_0^{2\pi} (x+y+2z)Y_\ell^m(\theta,\varphi)\sin\theta\,d\varphi\,d\theta.
$$

Las visualizaciones muestran mapas angulares sobre la esfera para interpretar qué modos contribuyen a la integral.

La carpeta contiene el desarrollo en `.tex`, el PDF compilado, el script de visualización y figuras en formato `.svg`.

### `potencial_esfera_armonicos/`

Carpeta dedicada al potencial electrostático producido por un **cascarón esférico con densidad superficial de carga** $\sigma(\theta,\varphi)$.

El desarrollo usa armónicos esféricos para escribir el potencial dentro y fuera del cascarón, imponiendo continuidad del potencial y la discontinuidad correspondiente de la derivada radial asociada a la carga superficial.

La carpeta contiene el desarrollo en `.tex`, el PDF compilado, el script de visualización y figuras en formato `.svg`.

### `onda_2d_tambor_bessel/`

Carpeta dedicada al problema de la **ecuación de onda bidimensional en un disco**, usualmente interpretado como el problema del tambor circular con borde fijo.

El desarrollo usa separación de variables en coordenadas polares. La parte radial conduce a funciones de Bessel y la condición de borde fija selecciona los ceros de estas funciones. La solución general queda escrita como una superposición de modos normales.

La carpeta contiene el desarrollo en `.tex`, el PDF compilado y el notebook:

- `onda_disco_funcion_rara.ipynb`

En el notebook se puede visualizar una animación de la solución para una condición inicial arbitraria.

## Agradecimientos

Agradezco al profesor Guillermo Rubilar por los desarrollos de algunos problemas y por compartir el notebook asociado al problema del tambor.
