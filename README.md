# LHS 1140 b y c: masa, radio y zona habitable

Trabajo final de Ciencias Planetarias (Universidad de Antioquia, 2026).

- **Problema 1:** masa y radio de LHS 1140 b y c a partir de velocidades radiales de HARPS (método line-by-line, LBL) y fotometría de TESS (PyTransit + emcee), comparados con la literatura.
- **Problema 2:** zona habitable de estrellas de 0.1 a 1.2 M☉ con los modelos de Baraffe et al. (2015) y las ecuaciones de Kopparapu et al. (2013).

El informe está en `paper/` (`articulo_LHS1140.tex` y `articulo_LHS1140.pdf`). Se compila con **XeLaTeX** (dos veces); las figuras se leen de `figs/`.

## Notebooks

Se ejecutan en orden. Los tres primeros usan Google Colab (`from google...`).

| Notebook | Contenido |
|---|---|
| `notebooks/1_HARPS_LHS1140_descarga.ipynb` | Consulta TAP al archivo de ESO y descarga de los espectros HARPS (e2ds) |
| `notebooks/2_LBL_HARPS_LHS1140.ipynb` | Velocidades radiales con LBL |
| `notebooks/3_Analisis_RV_LHS1140.ipynb` | Periodograma, ajuste de b y c, residuos, señal de 134 d, cromaticidad |
| `notebooks/4_LHS1140_transitos_MCMC.ipynb` | Curvas de luz de TESS, ajuste de tránsitos con MCMC, masas y radios |
| `notebooks/Problema2_zona_habitable.ipynb` | Zona habitable en función de la masa y la edad estelar |

El notebook del Problema 2 solo necesita NumPy y Matplotlib (la tabla del modelo estelar está incluida). Está guardado sin salidas: usa "Run all".

## Datos

Los espectros de HARPS vienen del archivo de ESO y las curvas de luz del archivo MAST (TESS, sectores 3, 30 y 107). No se incluyen en el repositorio por tamaño; los notebooks los descargan.

## Créditos

Las secciones 0 a 8 del notebook 1 (descarga de datos) vienen del trabajo de Juan David. Se usó Claude (Anthropic) como asistente para escribir y depurar el código y revisar el texto.

## Licencia

MIT, ver `LICENSE`.
