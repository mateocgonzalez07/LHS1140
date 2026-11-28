# LHS 1140 · parte de ESPRESSO

Semillero **COSMIA UdeA**. Esta carpeta tiene la parte del trabajo *"Masas, radios y composición de LHS 1140 b y c"* hecha por Juan David Sanclemente Salazar. La parte de HARPS, el ajuste MCMC de los tránsitos y la zona habitable las hizo Mateo Chavarría González y están en su repositorio.

La idea general: bajar los espectros públicos de ESPRESSO, sacarles las velocidades radiales con **LBL** (*line-by-line*), ajustarlas con **RadVel** y juntarlas con los tránsitos de **TESS** para sacar las masas, los radios y las densidades de los dos planetas.

## Orden

| Paso | Archivo | Qué hace |
|---|---|---|
| 1 | `notebooks/01_extraccion_datos_ESO.ipynb` | Explica paso a paso cómo consultar el archivo de ESO (TAP/ADQL), qué trae cada producto y el corte de ESPRESSO de junio de 2019. |
| 2 | `notebooks/02_descarga_espectros_ESPRESSO.ipynb` | Baja solo el espectro 2D y el blaze de cada producto de ESPRESSO, con la estructura de carpetas que pide LBL. |
| 3 | `lbl/wrap_LHS1140.py` | Configuración con la que se corrió LBL (Teff = 3100 K). La salida está en `datos/`. |
| 4 | RadVel | Ajuste kepleriano de dos planetas a las VR de ESPRESSO. Los resultados están en `resultados_radvel/`. |
| 5 | `notebooks/03_transitos_masas_densidades.ipynb` | BLS y `batman` sobre TESS, y luego masas (con RadVel), densidades y un diagrama masa-radio rápido. |

## Datos y resultados

- `datos/lbl_LHS1140_tc_LHS1140_tc.rdb`: velocidades radiales de LBL para los **44 espectros** de ESPRESSO (julio–diciembre de 2019), con los indicadores FWHM, CRX, dW, etc.
- `datos/lbl2_LHS1140_tc_LHS1140_tc.rdb`: la segunda tabla que genera el paso de compilación de LBL (42 filas).
- `datos/LHS1140_mr-plotter.ini`: configuración usada con [mr-plotter](https://github.com/castro-gzlz/mr-plotter) para el diagrama masa-radio del informe.
- `resultados_radvel/circular/`: ajuste final con **órbitas circulares**, el que se usa en el informe. Ahí están el resumen de posteriores, los cuantiles de las masas, las gráficas y la comparación de modelos.
- `resultados_radvel/excentrico/`: prueba con **excentricidad libre**. Las excentricidades salieron compatibles con cero, por eso el ajuste final es circular.

Los archivos de RadVel se llaman `TOI233_..._RADVEL_EXAMPLE` porque el archivo de configuración se armó a partir de un ejemplo de otro sistema. **Todos son de LHS 1140.**

Resultados principales con ESPRESSO: K_b = 3.05 m/s y K_c = 1.74 m/s, lo que da **M_b = 4.5 ± 1.1 M⊕** y **M_c = 1.37 ± 0.44 M⊕**. El modelo de dos planetas es el preferido por el AICc.

## Qué no está aquí

- **Los espectros FITS** (varios GB). Son públicos en el archivo de ESO y se vuelven a bajar con el notebook 02.
- *Pendiente:* el archivo `.py` de configuración de RadVel.

## Requisitos

Python 3 con `pyvo`, `astropy`, `numpy`, `pandas`, `matplotlib`, `lightkurve`, `batman-package`, `scipy`, `radvel` y [`lbl`](https://github.com/njcuk9999/lbl). Los notebooks 01 y 02 están pensados para Google Colab.

> **Ojo:** el notebook 03 lee los resultados de RadVel desde una ruta del computador de JuanDa (`/home/juan/Downloads/...`). Para correrlo, hay que cambiar esa ruta a `../resultados_radvel/circular/`.
