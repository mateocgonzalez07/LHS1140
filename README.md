# LHS 1140 b y c: velocidades radiales de HARPS con LBL y tránsitos de TESS

Proyecto final de Ciencias Planetarias (2026-2), Universidad de Antioquia. Autor: Mateo C. Gonzalez. Caracteriza los planetas LHS 1140 b y c con datos públicos:

- **293 espectros de HARPS** del archivo de ESO, de los que se extraen velocidades radiales (RV) con el método *line-by-line* (**LBL**, Artigau et al. 2022).
- **Fotometría de TESS** (sectores 3, 30 y 107), ajustada con un modelo de tránsito y MCMC.
- **Zona habitable** de estrellas de 0.1 a 1.2 M☉ (Baraffe et al. 2015 y Kopparapu et al. 2013), aplicada a LHS 1140.

El artículo está en `articulo_LHS1140.tex` (revtex4-2) y las figuras en `figs/`.

## Resultados principales

| | LHS 1140 b | LHS 1140 c |
|---|---|---|
| K (m/s) | 4.78 ± 0.45 | 2.47 ± 0.47 |
| Radio (R⊕) | 1.78 (+0.10/−0.07) | 1.25 (+0.06/−0.04) |
| Masa (M⊕) | 7.0 ± 0.7 | 1.95 ± 0.37 |
| Flujo recibido (S⊕) | 0.43 (zona habitable) | 5.3 (fuera) |

- La masa de c coincide con la literatura. La de b queda ~2σ por encima de la medida de ESPRESSO (Cadieux et al. 2024) y coincide con las de HARPS.
- Los residuos muestran una señal a 134 d, cerca de la rotación estelar (131 d). Las pruebas de coherencia, cromaticidad e indicadores de actividad apuntan a actividad y no a un tercer planeta.
- Las masas se calculan con órbitas circulares y la inclinación obtenida de los tránsitos.

## Contenido

| Archivo | Qué hace |
|---|---|
| `1_HARPS_LHS1140_descarga.ipynb` | Busca y descarga los espectros `e2ds_A` de HARPS por TAP, arma el manifiesto, prepara el blaze y audita su calidad. |
| `2_LBL_HARPS_LHS1140.ipynb` | Instala LBL y extrae las velocidades radiales de los 293 espectros. |
| `3_Analisis_RV_LHS1140.ipynb` | Promedio por noche, periodograma GLS, ajuste de b y c, residuos, actividad, cromaticidad y comparación con la literatura. |
| `4_LHS1140_transitos_MCMC.ipynb` | Ajuste de tránsitos (PyTransit + emcee), excentricidad, masas, radios, semiejes y diagrama masa-radio con mr-plotter. |
| `5_Problema2_zona_habitable.ipynb` | Zona habitable general en función de la masa y la edad estelar. |
| `articulo_LHS1140.tex` | Artículo. |
| `figs/` | Figuras del artículo. |

Pruebas opcionales (no entran en los resultados del artículo): `Prueba_GP_LHS1140.ipynb` (ajuste con proceso gaussiano para la actividad y robustez de K) y `Prueba_blaze_por_noche.ipynb` (consulta si el archivo de ESO tiene el blaze de cada noche; no lo tiene).

## Cómo reproducirlo

Los notebooks se escribieron y corrieron en **Google Colab** y guardan sus resultados en Google Drive, en la carpeta `MyDrive/LHS1140_HARPS/`. Se corren en orden:

1. **Descarga (notebook 1).** Baja ~2 GB entre `.tar` y `e2ds`.
2. **LBL (notebook 2).** Es la parte más lenta. Genera `resultados_LBL/completa/RV_LHS1140.csv`.
3. **RV (notebook 3).** Lee ese CSV y guarda sus figuras en `resultados_LBL/completa/analisis/`.
4. **Tránsitos y masas (notebook 4).** Usa los K del notebook 3. Con 25 000 pasos para b y 45 000 para c, el MCMC tarda unos minutos.
5. **Zona habitable (notebook 5).** No depende de los otros.

Todos los notebooks comparten el mismo bloque de constantes de LHS 1140 (Cadieux et al. 2024).

### Dependencias

Colab ya trae NumPy, SciPy, pandas, Matplotlib y Astropy. Cada notebook instala lo que falta:

`pyvo`, `lightkurve`, `PyTransit`, `emcee`, `corner`, `LBL`, `VPLanet`.

El diagrama masa-radio usa [mr-plotter](https://github.com/castro-gzlz/mr-plotter), que se clona dentro del notebook 4 (no se instalan sus `requirements.txt` en Colab, solo `pyvo`).

### El blaze de HARPS

Los espectros `e2ds` no incluyen el blaze, y el de cada noche no está disponible en el archivo de ESO. Se usó un solo blaze (`HARPS_BLAZE_A_72.fits`) reducido por Camilo A. Ospinal Achicanoy con el pipeline de HARPS, al que se le añadió un orden sintético (orden 0) para llegar a 72 órdenes. **Ese archivo no está en este repositorio.** Pídelo a su autor o colócalo en `MyDrive/LHS1140_HARPS/` antes de correr el notebook 1. Los detalles y la auditoría están en la sección *Datos* del artículo y en el notebook 1.

## Datos

- **HARPS** (ESO, La Silla): espectros públicos del archivo de ESO, consultados por TAP en `archive.eso.org/tap_obs`.
- **TESS**: curvas de luz SPOC (PDCSAP, 120 s) del archivo MAST, descargadas con `lightkurve`.
- **Catálogo de planetas**: NASA Exoplanet Archive (Akeson et al. 2013; Christiansen et al. 2025).

## Limitaciones conocidas

- Se usó un solo blaze para todas las épocas de HARPS.
- Cada planeta se ajustó por separado, con oscurecimiento al limbo fijo y órbita circular.
- La señal de 134 d no se modela en el valor principal de K; se probó con una tercera sinusoide y con un proceso gaussiano, sin cambios mayores a 1σ.
- Con HARPS solo, la incertidumbre de K_b (~10 %) es cuatro veces mayor que la de ESPRESSO. Un análisis conjunto con ESPRESSO sería la mejora más directa.

## Cómo citar

Si usas este trabajo, cita el artículo:

> Gonzalez, M. C. 2026, *Caracterización de LHS 1140 b y c con velocidades radiales line-by-line de HARPS y fotometría de TESS, y zona habitable de estrellas de baja masa*, Universidad de Antioquia.

Y, si usas el diagrama masa-radio, a [mr-plotter](https://github.com/castro-gzlz/mr-plotter).

## Agradecimientos

A Camilo A. Ospinal Achicanoy y al semillero COSMIA-UdeA por el blaze de HARPS y el taller de LBL; a Alejandra Arciniegas por el notebook base de fotometría de tránsitos; a Juan David Sanclemente Salazar por las secciones de descarga de datos; y al profesor Pablo Cuartas-Restrepo por el curso en el que se desarrolló este trabajo. Se usó Claude (Anthropic) como asistente para escribir y depurar el código y revisar el texto.

## Licencia

MIT, © 2026 Mateo C. Gonzalez. Ver el archivo [`LICENSE`](LICENSE).

Repositorio: https://github.com/mateocgonzalez07/LHS1140
