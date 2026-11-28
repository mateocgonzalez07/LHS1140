# RadVel configuration file — TOI-233 MAROON-X Blue + Red (LBL, self-template)
# Blue channel: lbl_TOI233_MAROONX_B_GEMINI_2025_tc_TOI233_MAROONX_B_GEMINI_2025_tc.fits
# Red channel: lbl_TOI233_MAROONX_R_GEMINI_2025_tc_TOI233_MAROONX_R_GEMINI_2025_tc.fits
# 25 observations × 2 channels = 50 independent measurements
# Deriva del etalon MAROON-X: ~2-3 cm/s/día (Basant+2025) → dvdt libre con prior gaussiano
# Parámetros orbitales iniciales: Exoplanet Archive (TOI-233.01 y TOI-233.02)


# NO UTILIZAR GAUSSIAN PROCESS FOR THE INITIAL TEST

# This file uses Gaussian Process for all of them

import os
import numpy as np
import pandas as pd
from astropy.io import fits
import radvel

# ── Sistema ───────────────────────────────────────────────────────────────────
# tc propagados desde Exoplanet Archive al baseline 2025 (RJD):
#   tc1_archive = 2458365.26145 BJD → 58365.26145 RJD
#   tc1 propagado con P1 × 222 épocas → 60956.008 RJD
#   tc2_archive = 2458359.47144 BJD → 58359.47144 RJD
#   tc2 propagado con P2 × 360 épocas → 60951.881 RJD
time_base = 58754.0  # punto medio del baseline (~RJD 60870–61038)
tc1_rjd = 59142.0469
tc2_rjd = 59133.5481
P1 = 24.737246
P2 = 3.777936
n1 = round((time_base - tc1_rjd)/P1)
n2 = round((time_base - tc2_rjd)/P2)
tc1_2025 = tc1_rjd + n1 * P1
tc2_2025 = tc2_rjd + n2 * P2
starname      = 'LHS1140'
nplanets      = 2
instnames     = ['espresso']        # ['harps', 'espresso']   # Maroon X as two different instruments
ntels         = len(instnames)
fitting_basis = 'per tc secosw sesinw logk'
bjd0          =  2400000 + time_base       # RJD ya tiene 2400000 (dejenlo así...)
planet_letters = {1: 'b', 2: 'c'} # TOI256 a, TOI256 b

# ── Blue Channel ───────────────────────────────────────────────────
#_fits_b = '/home/camilo/Desktop/MITACS_Project/lbl/DEMOS/TOI233_MAROONX_B_GEMINI_2/lblrdb/lbl_TOI233_MAROONX_B_GEMINI_2025_tc_TOI233_MAROONX_B_GEMINI_2025_tc.fits'

#with fits.open(_fits_b) as f:
    #_rdb_b  = f['RDB'].data   # Datis principales
    #_time_b = _rdb_b['rjd'].astype(float) - time_base   # tiempo
    #_vrad_b = _rdb_b['vrad'].astype(float)              # velocidades radiales
    #_svrad_b = _rdb_b['svrad'].astype(float)            # standard deviation VR
    #_vrad_b -= 0.0217* (_rdb_b['rjd'].astype(float) - time_base)  # corrección de la deriva de elaton
    #_vrad_b  -= np.median(_vrad_b)


# ── Red Channel ───────────────────────────────────────────────────
#fits_r = '/home/camilo/Desktop/MITACS_Project/lbl/DEMOS/TOI233_MAROONX_R_GEMINI_2/lblrdb/lbl_TOI233_MAROONX_R_GEMINI_2025_tc_TOI233_MAROONX_R_GEMINI_2025_tc.fits'

#with fits.open(_fits_r) as f:
#    _rdb_r  = f['RDB'].data
 #   _time_r = _rdb_r['rjd'].astype(float) - time_base
  #  _vrad_r = _rdb_r['vrad'].astype(float)
   # _svrad_r = _rdb_r['svrad'].astype(float)
    #_vrad_r -= 0.0225* (_rdb_r['rjd'].astype(float) - time_base)
#vrad_r  -= np.median(_vrad_r)
    
# ── ESPRESSO ─────────────────────────────────────────────────────
_espresso_ = '/home/juan/COSMIA_LHS1140/LBL_LHS1140/lblrdb/lbl_LHS1140_tc_LHS1140_tc.rdb'  # Remplazar por su carpeta de origen

espresso_df = pd.read_csv(_espresso_, sep='\t', skiprows=[1])
_time_ex = espresso_df['rjd'] - time_base
_vrad_ex = espresso_df['vrad']
_svrad_ex = espresso_df['svrad']
_vrad_ex -= np.median(_vrad_ex)   # Acá se extrae la mediana para calcular las RV relativas


# ── Dataframe ─────────────────────────────────────────────
data = pd.DataFrame({
    'time'  : np.concatenate([_time_ex]),  # Los de HARPS irian primero 
    'mnvel' : np.concatenate([_vrad_ex]),
    'errvel': np.concatenate([_svrad_ex]),
    'tel'   : ['espresso'] * len(_time_ex), # Lo mismo pero con HARPS
})

# Se lo pueden saltar!!! Pueden comentarlo...
# ── Gaussian parameters ──────────────────────────────────────────────────────
#gp_per_mean = 43.5 # From RVs and Halpha periodograms
#gp_per_unc = 1     # Just in case

#gp_explength_mean = gp_per_mean*np.sqrt(2.) # sqrt(2)*Prot (recommended by Ryan [1,10] x T)
#gp_explength_unc = 1.0*np.sqrt(2.)
#gp_perlength_mean = np.sqrt(1./(2*3.32)) # It should be around 0.5
#gp_perlength_unc = 0.1 # Wide just in case

# Defensive checks for GP parameters to prevent infs/NaNs
#assert gp_explength_mean > 0 and not np.isnan(gp_explength_mean) and not np.isinf(gp_explength_mean), "Invalid gp_explength_mean"
#assert gp_explength_unc > 0 and not np.isnan(gp_explength_unc) and not np.isinf(gp_explength_unc), "Invalid gp_explength_unc"
#assert gp_perlength_mean > 0 and not np.isnan(gp_perlength_mean) and not np.isinf(gp_perlength_mean), "Invalid gp_perlength_mean"
#assert gp_perlength_unc > 0 and not np.isnan(gp_perlength_unc) and not np.isinf(gp_perlength_unc), "Invalid gp_perlength_unc"
#assert gp_per_mean > 0 and not np.isnan(gp_per_mean) and not np.isinf(gp_per_mean), "Invalid gp_per_mean"
#assert gp_per_unc > 0 and not np.isnan(gp_per_unc) and not np.isinf(gp_per_unc), "Invalid gp_per_unc"

# ── Inicial parameters ──────────────────────────────────────────────────────

anybasis_params = radvel.Parameters(nplanets,
                                    basis=fitting_basis,
                                    planet_letters=planet_letters)

# Planet b — TOI-233.01 (P ~ 11.67 d)
anybasis_params['per1'] = radvel.Parameter(value=P1)  # Periodo 
anybasis_params['tc1']  = radvel.Parameter(value=tc1_2025 - time_base) # Tiempo de trancito
anybasis_params['sesinw1'] = radvel.Parameter(value=0.00)  # Una buena aproximación para la excentricidad es 0
anybasis_params['secosw1'] = radvel.Parameter(value=0.00)
anybasis_params['logk1']   = radvel.Parameter(value=np.log(3.0))    # Semi amplitud! m/s — initial guess

# Planet c — TOI-233.02 (P ~ 7.20 d)
anybasis_params['per2'] = radvel.Parameter(value=P2)
anybasis_params['tc2']  = radvel.Parameter(value=tc2_2025 - time_base)
anybasis_params['sesinw2'] = radvel.Parameter(value=0.00)
anybasis_params['secosw2'] = radvel.Parameter(value=0.00)
anybasis_params['logk2'] = radvel.Parameter(value=np.log(2.0))    # m/s — initial guess

# Etanol MAROON-X (Basant+2025: ~2-3 cm/s/day = 0.02-0.03 m/s/day)?? ESTA DESCRIPCIÓN SOLO APLICA PARA MAROON X 

anybasis_params['dvdt'] = radvel.Parameter(value=0.0) # Suponer que la velocidad oscila respecto a 0 o un valor de referencia
anybasis_params['curv'] = radvel.Parameter(value=0.0)    # curvatura fija en 0

# Zero-points per instruments
#anybasis_params['gamma_maroonx_b'] = radvel.Parameter(value=0.0)   # m/s
#anybasis_params['gamma_maroonx_r'] = radvel.Parameter(value=0.0)   # m/s
anybasis_params['gamma_espresso'] = radvel.Parameter(value=0.0)

# Jitter per instrument
#anybasis_params['jit_maroonx_b'] = radvel.Parameter(value=2.0)     # m/s
#anybasis_params['jit_maroonx_r'] = radvel.Parameter(value=2.0)     # m/s
anybasis_params['jit_espresso'] = radvel.Parameter(value=2.0)

# Convertir a la base de fitting
params = anybasis_params.basis.to_any_basis(anybasis_params, fitting_basis)

# Variacion de la excentricidad (también puedes variar los otros parámetros)
params['secosw1'].vary = False
params['sesinw1'].vary = False
params['secosw2'].vary = False
params['sesinw2'].vary = False

params['curv'].vary = False
params['dvdt'].vary = False


#------------------------------- GP  --------------------
# Define GP hyperparameters as Parameter objects.
#params['gp_amp_maroonx_b'] = radvel.Parameter(value=26.0)  # Just because we don't know the exact value of this parameter
#params['gp_amp_maroonx_r'] = radvel.Parameter(value=26.0)
#params['gp_amp_espresso'] = radvel.Parameter(value=26.0)
#params['gp_amp'] = radvel.Parameter(value=26.0)
#params['gp_explength'] = radvel.Parameter(value=gp_explength_mean)
#params['gp_per'] = radvel.Parameter(value=gp_per_mean)
#params['gp_perlength'] = radvel.Parameter(value=gp_perlength_mean)

# gaussian process
#hnames = {
#    'maroonx_b': ['gp_amp', 'gp_explength', 'gp_per', 'gp_perlength'],
#    'maroonx_r': ['gp_amp', 'gp_explength', 'gp_per', 'gp_perlength'],
#    'espresso':  ['gp_amp', 'gp_explength', 'gp_per', 'gp_perlength'],
#}

#kernel_name = {tel: 'QuasiPer' for tel in instnames}
#hnames = {
#  'maroonx_b': ['gp_amp_maroonx_b', # GP variability amplitude
#              'gp_per', # GP variability period
#              'gp_explength', # GP non-periodic characteristic length
#              'gp_perlength'], # GP periodic characteristic length
#  'maroonx_r': ['gp_amp_maroonx_r',
#          'gp_per',
#          'gp_explength',
#          'gp_perlength'],}
#  'espresso': ['gp_amp_espresso',
#          'gp_per',
#          'gp_explength',
#          'gp_perlength'],
#}

# ── Priors ────────────────────────────────────────────────────────────────────
priors = [
    # Planeta b
    radvel.prior.Gaussian('per1', P1, 0.000016),
    radvel.prior.Gaussian('tc1',  tc1_2025 - time_base,  0.001),
    radvel.prior.HardBounds('secosw1', -1, 1),
    radvel.prior.HardBounds('sesinw1', -1, 1),
    radvel.prior.HardBounds('logk1', np.log(0.5), np.log(20)),

    # Planeta c
    radvel.prior.Gaussian('per2', P2, 0.000001),
    radvel.prior.Gaussian('tc2',  tc2_2025 - time_base,  0.001), # los valores númericos corresponden a los definidos anteriormente
    radvel.prior.HardBounds('secosw2', -1, 1),
    radvel.prior.HardBounds('sesinw2', -1, 1),
    radvel.prior.HardBounds('logk2', np.log(1), np.log(10)),

    # Excentricidad
    radvel.prior.EccentricityPrior(nplanets, 0.556),   # una excentricidad de 0.3 es muy alta. La excentricidad fue definida utilizando la ecuación de la excentricidad de cruce (cross eccentricity)

    # Jitter
    #radvel.prior.HardBounds('jit_maroonx_b', 0.0, 10.0),
    #radvel.prior.HardBounds('jit_maroonx_r', 0.0, 10.0),
    radvel.prior.HardBounds('jit_espresso', 0.0, 10.0),

    # Gamma — sin prior fuerte, el fit encuentra el offset relativo entre canales
    #radvel.prior.HardBounds('gamma_maroonx_b', -50.0, 50.0),
    #radvel.prior.HardBounds('gamma_maroonx_r', -50.0, 50.0),
    radvel.prior.HardBounds('gamma_espresso', -50.0, 50.0),
    
    # Gaussian process
    #radvel.prior.Jeffreys('gp_amp_maroonx_b', 0.01, 100.),
    #radvel.prior.Jeffreys('gp_amp_maroonx_r', 0.01, 100.),
    #radvel.prior.Jeffreys('gp_amp_espresso', 0.01, 100.),
    #radvel.prior.Jeffreys('gp_amp', 0.01, 100.),
    #radvel.prior.HardBounds('gp_explength', 0.1, 100.),
    #radvel.prior.HardBounds('gp_per', 0.1, 100.),
    #radvel.prior.HardBounds('gp_perlength', 0.01, 10.0)
]

# ── Masa estelar ──────────────────────────────────────────────────────────────
stellar = dict(mstar=0.1844, mstar_err=0.0045)   # TOI-233: M enana ~0.37 Msun
