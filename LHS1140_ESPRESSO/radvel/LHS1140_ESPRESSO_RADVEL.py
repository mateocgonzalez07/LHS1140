# RadVel configuration file — LHS 1140 (TOI-256)
# Solo ESPRESSO (LBL, 44 espectros después de junio 2019)
# Basado en el ejemplo de Camilo (TOI233_MX_BR_ESP_1GP_ecross_RADVEL_EXAMPLE.py)
#
# SIN proceso gaussiano (Camilo: con GP se demora horas) y con órbitas circulares.
# P y T0 vienen de NUESTRO ajuste de tránsitos con TESS (informe de Mateo, Tabla III).

import numpy as np
import pandas as pd
import radvel

# ── Opciones ──────────────────────────────────────────────────────────────────
EXCENTRICA = False         # False = órbitas circulares (e = 0)

# ── Archivos (CAMBIAR por sus rutas) ─────────────────────────────────────────
archivo_espresso = '/home/juan/COSMIA_LHS1140/LBL_LHS1140/lblrdb/lbl_LHS1140_tc_LHS1140_tc.rdb'

# ── Efemérides de NUESTRO ajuste de TESS (Tabla III del informe) ─────────────
# T0 está en BTJD = BJD - 2457000. Lo pasamos a RJD = BJD - 2400000.
P1,  sP1  = 24.737246, 0.000016          # planeta b
T01, sT01 = 2142.0469 + 57000, 0.0008    # RJD
P2,  sP2  = 3.777936, 0.000001           # planeta c
T02, sT02 = 2133.5481 + 57000, 0.0004    # RJD

# ── Datos ─────────────────────────────────────────────────────────────────────
def leer_rdb(archivo):
    # Los .rdb de LBL: primera fila = nombres, segunda fila = guiones
    df = pd.read_csv(archivo, sep='\t', skiprows=[1])
    t = df['rjd'].astype(float).values
    v = df['vrad'].astype(float).values
    ev = df['svrad'].astype(float).values
    v = v - np.median(v)          # velocidad relativa (como pidió Camilo)
    return t, v, ev

t_esp, v_esp, ev_esp = leer_rdb(archivo_espresso)
instnames = ['espresso']

# ── Sistema ───────────────────────────────────────────────────────────────────
time_base = round((t_esp.min() + t_esp.max()) / 2, 3)   # mitad de los datos (RJD)

# Llevamos cada T0 al tránsito más cercano a time_base (como hizo Camilo)
n1 = round((time_base - T01) / P1)
n2 = round((time_base - T02) / P2)
tc1 = T01 + n1 * P1
tc2 = T02 + n2 * P2
s_tc1 = np.sqrt(sT01**2 + (n1 * sP1)**2)    # incertidumbre propagada
s_tc2 = np.sqrt(sT02**2 + (n2 * sP2)**2)

starname       = 'LHS1140'
nplanets       = 2
ntels          = len(instnames)
fitting_basis  = 'per tc secosw sesinw logk'
bjd0           = 2400000 + time_base
planet_letters = {1: 'b', 2: 'c'}

data = pd.DataFrame({
    'time'  : t_esp - time_base,
    'mnvel' : v_esp,
    'errvel': ev_esp,
    'tel'   : ['espresso'] * len(t_esp),
})

# ── Parámetros iniciales ──────────────────────────────────────────────────────
params = radvel.Parameters(nplanets, basis=fitting_basis, planet_letters=planet_letters)

# Planeta b
params['per1']    = radvel.Parameter(value=P1)
params['tc1']     = radvel.Parameter(value=tc1 - time_base)
params['secosw1'] = radvel.Parameter(value=0.0)
params['sesinw1'] = radvel.Parameter(value=0.0)
params['logk1']   = radvel.Parameter(value=np.log(4.0))   # valor inicial

# Planeta c
params['per2']    = radvel.Parameter(value=P2)
params['tc2']     = radvel.Parameter(value=tc2 - time_base)
params['secosw2'] = radvel.Parameter(value=0.0)
params['sesinw2'] = radvel.Parameter(value=0.0)
params['logk2']   = radvel.Parameter(value=np.log(2.5))   # valor inicial

# Sin tendencia lineal ni curvatura
params['dvdt'] = radvel.Parameter(value=0.0)
params['curv'] = radvel.Parameter(value=0.0)
params['dvdt'].vary = False
params['curv'].vary = False

# Un gamma y un jitter por instrumento
for tel in instnames:
    params['gamma_' + tel] = radvel.Parameter(value=0.0)
    params['jit_' + tel]   = radvel.Parameter(value=2.0)

# Órbitas circulares: excentricidad fija en 0
for i in [1, 2]:
    params['secosw%d' % i].vary = EXCENTRICA
    params['sesinw%d' % i].vary = EXCENTRICA

# ── Priors ────────────────────────────────────────────────────────────────────
priors = [
    # Planeta b: P y tc de TESS
    radvel.prior.Gaussian('per1', P1, sP1),
    radvel.prior.Gaussian('tc1', tc1 - time_base, s_tc1),
    radvel.prior.HardBounds('logk1', np.log(0.5), np.log(20)),

    # Planeta c: P y tc de TESS
    radvel.prior.Gaussian('per2', P2, sP2),
    radvel.prior.Gaussian('tc2', tc2 - time_base, s_tc2),
    radvel.prior.HardBounds('logk2', np.log(0.5), np.log(10)),
]

for tel in instnames:
    priors.append(radvel.prior.HardBounds('jit_' + tel, 0.0, 20.0))
    priors.append(radvel.prior.HardBounds('gamma_' + tel, -50.0, 50.0))

if EXCENTRICA:
    for i in [1, 2]:
        priors.append(radvel.prior.HardBounds('secosw%d' % i, -1, 1))
        priors.append(radvel.prior.HardBounds('sesinw%d' % i, -1, 1))

# ── Masa estelar (literatura: Cadieux et al. 2024) ────────────────────────────
stellar = dict(mstar=0.1844, mstar_err=0.0045)
