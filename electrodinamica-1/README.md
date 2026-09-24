# Electrodinámica I

Esta carpeta reúne los desarrollos de los problemas de Electrodinámica I en
`.tex`, sus versiones compiladas en PDF y los scripts en Python usados para
las visualizaciones. Agradecemos a Pablo Solano por facilitarnos los problemas
que dieron origen a este material.

---

## `cilindro_hueco_infinito/`

Problema de electrostática para un **cilindro hueco infinito con densidad volumétrica no uniforme**.

La distribución de carga está dada por

```math
\rho(r)=
\begin{cases}
0, & 0\leq r \lt a,\\
\dfrac{\rho_0}{r}, & a \lt r \lt b,\\
0, & r \gt b.
\end{cases}
```

El campo eléctrico se calcula mediante integración directa y mediante la Ley de Gauss. Luego se obtiene el potencial en las tres regiones, usando la condición de referencia

```math
\phi(b)=0.
```

---

## `anillo_carga_no_uniforme/`

Problema de electrostática para un **anillo con densidad lineal de carga no uniforme**.

El anillo se encuentra en el plano $xy$ y su densidad depende de la coordenada angular según

```math
\lambda(\varphi')=\lambda_0\cos\varphi'.
```

Se discute por qué la Ley de Gauss no permite calcular directamente el campo eléctrico de esta distribución. Después se obtienen el campo y el potencial sobre el eje geométrico del anillo mediante integración directa, y se verifica la relación

```math
E_z=-\frac{d\phi}{dz}.
```

---

## `densidad_superficial_desde_potencial/`

Problema de **densidad superficial de carga obtenida a partir del potencial eléctrico** sobre un plano infinito.

El plano $z=0$ divide el vacío en dos regiones, con potencial

```math
\phi(x,y,z)=
\begin{cases}
\dfrac{V_0z}{(x^2+y^2+z^2)^{3/2}}, & z \gt 0,\\
\dfrac{V_0z}{2(x^2+y^2+z^2)^{3/2}}, & z \lt 0.
\end{cases}
```

El desarrollo calcula el campo eléctrico a ambos lados del plano y estudia sus componentes normal y tangencial. La continuidad tangencial se obtiene mediante un contorno rectangular y el teorema de Stokes, mientras que la densidad superficial se determina usando una pastilla gaussiana y la condición de salto

```math
\hat n\cdot
\left(
\vec E^+-\vec E^-
\right)
=
\frac{\sigma}{\varepsilon_0}.
```

Las figuras muestran la geometría de la interfaz y las superficies utilizadas en las condiciones de frontera.

---

## `separacion_variables_cilindro/`

Problema de la **ecuación de Laplace en un cilindro infinito**, con el
potencial impuesto sobre una superficie de radio $R$:

```math
V(R,\phi,z)=V_0\sin(2\phi).
```

El enunciado pide separar las variables, hallar los potenciales interior y
exterior y, a partir de ellos, calcular el campo eléctrico y la carga
superficial.

---

## `cuna_conductora_60_grados/`

Problema del **método de imágenes para una cuña conductora de $60^\circ$**.
Dos semiplanos conectados a tierra se encuentran en $\phi=0$ y
$\phi=\pi/3$; una carga puntual está sobre la bisectriz. Se busca el
potencial dentro de la cuña,

```math
V(s,\phi,z)=\frac{1}{4\pi\varepsilon_0}
\sum_{j=0}^{5}\frac{q_j}{R_j},
```

junto con la densidad de carga inducida en ambas caras. El desarrollo sigue
los tres apartados del enunciado: construcción de las imágenes, potencial y
densidad superficial.

---

