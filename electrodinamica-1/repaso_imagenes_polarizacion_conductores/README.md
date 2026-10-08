# Práctica de repaso de Electrodinámica I

La guía reúne dos problemas: una carga frente a un plano conductor conectado
a tierra y un cilindro conductor neutro sometido a un campo uniforme.
Incluye los enunciados, desarrollos basados en las notas manuscritas,
esquemas TikZ y una sección final de visualización numérica. La notación
usa `V` para el potencial, `s` para la coordenada cilíndrica radial, `phi`
para el ángulo azimutal y flechas para los vectores.

En el problema del plano se distinguen los puntos fuente y de observación,
se desarrolla la dirección de la fuerza y el producto escalar del trabajo,
y se hacen explícitos los nuevos límites al cambiar de variable en la
carga inducida. Los dos cortes TikZ en el plano `xz` explican la
equivalencia exacta del sistema carga-plano y del sistema carga-imagen:
ambos usan las mismas líneas y flechas de campo en `z>0`. En el plano
las líneas terminan en el conductor; en el dipolo continúan hacia la
carga imagen. Los caminos están incorporados en el propio TikZ y se
trazaron a partir del campo exacto. Las distancias en el desarrollo se
escriben como magnitudes de diferencias vectoriales. Las ecuaciones
reutilizadas están numeradas.

El apartado multipolar sigue la definición del apunte de Electrodinámica
de Guillermo Rubilar: el potencial se descompone en contribuciones de
orden `n`, y desarrolla los momentos monopolar y dipolar. Se muestra
por qué se trunca en el dipolo dominante a grandes distancias. Las
referencias a los paneles numéricos conectan el cálculo con las figuras.
Los momentos se calculan como sumas sobre las dos cargas puntuales del
sistema auxiliar. La carga inducida es la carga física distribuida sobre
todo el plano conductor infinito; se usa su valor total `-q` al calcular
la carga total del sistema.

En el cilindro se utiliza directamente la forma factorizada de las notas,
estudiada en la ayudantía 5. Los coeficientes se determinan en ese orden:
selección de `m=1`, producto `A_1 C_1`, anulación de los términos restantes
y cálculo de `B_1` en la superficie. Se conserva el cálculo del campo y de
la densidad inducida.
El esquema TikZ del cilindro muestra el campo externo, las líneas del
campo total y la cancelación de las dos contribuciones dentro del metal.
La carga superficial se representa como una banda continua con signos;
la etiqueta interior conserva un fondo transparente.

## Compilar en Overleaf

Sube el contenido de esta carpeta conservando la subcarpeta `figuras/` y
selecciona `repaso_imagenes_polarizacion_conductores.tex` como archivo
principal. Usa pdfLaTeX.
Los dos SVG ya están generados; no necesitas ejecutar Python en Overleaf.

El documento usa `svg` con `inkscapelatex=false`, de modo que las etiquetas
de los gráficos permanecen dentro de la imagen. El archivo `latexmkrc`
habilita la conversión automática de SVG por Inkscape durante la compilación.
Overleaf explica este procedimiento en su documentación sobre
[inserción de imágenes SVG](https://www.overleaf.com/learn/latex/Inserting_Images#SVG_images).
Las figuras en TikZ se compilan directamente desde el `.tex`.

## Regenerar los gráficos

Instala las dependencias y ejecuta el script:

```sh
python -m pip install -r requirements.txt
python repaso_imagenes_polarizacion_conductores_visualizacion.py
```

Los archivos de salida son:

- `figuras/carga_plano_visualizacion.svg`
- `figuras/cilindro_uniforme_visualizacion.svg`

Los gráficos evalúan las fórmulas analíticas en unidades adimensionales.
Los SVG son vectoriales y conservan su nitidez al ampliarlos. La malla
de evaluación y el número de niveles de color se han aumentado para
suavizar los mapas y la superficie 3D; las etiquetas son más grandes.
Los mapas incluyen escalas de color del potencial, de la magnitud del campo
y de la densidad superficial. Las líneas de campo se obtienen a partir de
los valores del campo exacto. En el caso del plano se compara además el
potencial exacto con su aproximación dipolar para diferentes distancias.
La vista tridimensional del cilindro representa un tramo sin tapas de un
sistema infinito, con una densidad independiente de la coordenada axial.

En el semiespacio físico del problema del plano se excluye una vecindad de
la carga puntual para evitar su singularidad. La carga imagen solo aparece
en el esquema TikZ como una fuente matemática auxiliar.

El PDF incluido es la guía completa compilada. Las figuras externas se
conservan en SVG, junto con el script que permite reproducirlas.
