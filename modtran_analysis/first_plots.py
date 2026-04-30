import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from modtran_analysis.tools import utils

# Loading in the data file to read
from importlib import resources

LOCAL_DATA_PATH = resources.files("modtran_analysis") / "data"
DATA_FILE_PATH = LOCAL_DATA_PATH / "FV3_Modtran6_IO_v0_scene_1(1).nc"

ds_v0 = xr.open_dataset(DATA_FILE_PATH)

# Extracting the specific data we want to plot

wavelength_v0 = ds_v0['wavelength']
RAA_v0 = ds_v0['RAA']
SZA_v0 = ds_v0['SZA']
VZA_v0 = ds_v0['VZA']

spectral_radiance_toa_v0 = ds_v0['MODTRAN6_SPECTRAL_RADIANCE_TOA']

# Plotting Viewing geometries V0
from visualization import plotting

plt.figure(figsize=(20,6))
plt.subplot(1,3,1)
plotting.plot_viewing_geometry(RAA_v0, 'RAA', 'Unfiltering', data_version='V0')

plt.subplot(1,3,2)
plotting.plot_viewing_geometry(SZA_v0, 'SZA', 'Unfiltering', data_version='V0')

plt.subplot(1,3,3)
plotting.plot_viewing_geometry(VZA_v0, 'VZA', 'Unfiltering', data_version='V0')
plt.savefig("/Users/kese6848/Desktop/Figures/Viewing-Geometry-v0.jpeg")
plt.close()


# Plotting sample spectra V0
plt.figure(figsize=(10,6))
plotting.plot_single_spectrum(wavelength_v0, spectrum_data=utils.unit_conversion(spectral_radiance_toa_v0[0][0][0][:]),
                              title='MODTRAN6 calculated Spectrally-Resolved TOA Radiance \n(at 5 nm 300-5000 nm)',
                              RAA=f'{RAA_v0.values[0]}', SZA=f'{SZA_v0.values[0]}', VZA=f'{VZA_v0.values[0]}', data_version='V0')
plt.xscale('log')
plt.savefig("/Users/kese6848/Desktop/Figures/Spectral-v0.jpeg")
plt.close()

# -------------------------------------------------------------------------------------------------------------------------

#Plotting for v1
LOCAL_DATA_PATH = resources.files("modtran_analysis") / "data"
DATA_FILE_PATH = LOCAL_DATA_PATH / "FV3_Modtran6_IO_v1_scene_1(1).nc"

ds_v1 = xr.open_dataset(DATA_FILE_PATH)
wavelength_v1 = ds_v1['wavelength']
RAA_v1 = ds_v1['RAA']
SZA_v1 = ds_v1['SZA']
VZA_v1 = ds_v1['VZA']
spectral_radiance_toa_v1 = ds_v1['MODTRAN6_SPECTRAL_RADIANCE_TOA']
IGBP_Land_Type_v1 = ds_v1['IGBP_Type']

plt.figure(figsize=(20,6))
plt.subplot(1,3,1)
plotting.plot_viewing_geometry(RAA_v1, 'RAA', 'Unfiltering', data_version='V1')

plt.subplot(1,3,2)
plotting.plot_viewing_geometry(SZA_v1, 'SZA', 'Unfiltering', data_version='V1')

plt.subplot(1,3,3)
plotting.plot_viewing_geometry(VZA_v1, 'VZA', 'Unfiltering', data_version='V1')
plt.savefig("/Users/kese6848/Desktop/Figures/Viewing-Geometry-v1.jpeg")
plt.close()

plt.figure(figsize=(10,6))
plotting.plot_single_spectrum(wavelength_v1, spectrum_data=utils.unit_conversion(spectral_radiance_toa_v1[0][0][0][:]),
                              title='MODTRAN6 calculated Spectrally-Resolved TOA Radiance \n(at 5 nm 300-5000 nm)',
                              RAA=f'{RAA_v1.values[0]}', SZA=f'{SZA_v1.values[0]}', VZA=f'{VZA_v1.values[0]}',
                              scene=f'{IGBP_Land_Type_v1.values}', data_version='V1')
plt.xscale('log')
plt.savefig("/Users/kese6848/Desktop/Figures/Spectral-v1.jpeg")
plt.close()


# -------------------------------------------------------------------------------------------------------------------------

# Plotting for V3
LOCAL_DATA_PATH = resources.files("modtran_analysis") / "data"
DATA_FILE_PATH = LOCAL_DATA_PATH / "FV3_Modtran6_IO_v3_scene_1.nc"
ds_v3 = xr.open_dataset(DATA_FILE_PATH)
wavelength_v3_sw = ds_v3['wavelength_sw']
wavelength_v3_lw = ds_v3['wavelength_lw']
ERBE_RAA_v3 = ds_v3['ERBE_RAA']
ERBE_SZA_v3 = ds_v3['ERBE_SZA']
ERBE_VZA_v3 = ds_v3['ERBE_VZA']
CERES_TRMM_RAA_v3 = ds_v3['CERES_TRMM_RAA']
CERES_TRMM_SZA_v3 = ds_v3['CERES_TRMM_SZA']
CERES_TRMM_VZA_v3 = ds_v3['CERES_TRMM_VZA']
spectral_radiance_toa_sw_ERBE_v3 = ds_v3['MODTRAN6_SPECTRAL_RADIANCE_TOA_SW_WVL_ERBE']
spectral_radiance_toa_lw_ERBE_v3 = ds_v3['MODTRAN6_SPECTRAL_RADIANCE_TOA_LW_WVL_ERBE']
spectral_radiance_toa_sw_CERES_TRMM_v3 = ds_v3['MODTRAN6_SPECTRAL_RADIANCE_TOA_SW_WVL_CERES_TRMM']
spectral_radiance_toa_lw_CERES_TRMM_v3 = ds_v3['MODTRAN6_SPECTRAL_RADIANCE_TOA_LW_WVL_CERES_TRMM']
IGBP_Land_Type_v3 = ds_v3['IGBP_Type']

plt.figure(figsize=(20,6))
plt.subplot(1,3,1)
plotting.plot_viewing_geometry(ERBE_RAA_v3, 'RAA', 'ERBE', data_version='v3')

plt.subplot(1,3,2)
plotting.plot_viewing_geometry(ERBE_SZA_v3, 'SZA', 'ERBE', data_version='v3')

plt.subplot(1,3,3)
plotting.plot_viewing_geometry(ERBE_VZA_v3, 'VZA', 'ERBE', data_version='v3')
plt.savefig("/Users/kese6848/Desktop/Figures/Viewing-Geometry-ERBE-v3.jpeg")
plt.close()

plt.figure(figsize=(10,6))
plotting.plot_single_spectrum(wavelength_v3_sw, spectrum_data=utils.unit_conversion(spectral_radiance_toa_sw_ERBE_v3[0][0][0][:]),
                              title=f'{spectral_radiance_toa_sw_ERBE_v3.long_name}\n(at 2.5 nm 250-5000 nm)',
                              RAA=f'{ERBE_RAA_v3.values[0]}', SZA=f'{ERBE_SZA_v3.values[0]}', VZA=f'{ERBE_VZA_v3.values[0]}',
                              scene=f'{IGBP_Land_Type_v3.values}', data_version='v3')
plt.xscale('log')
plt.savefig("/Users/kese6848/Desktop/Figures/Spectral-ERBE-SW-v3.jpeg")
plt.close()

plt.figure(figsize=(10,6))
plotting.plot_single_spectrum(wavelength_v3_lw, spectrum_data=utils.unit_conversion(spectral_radiance_toa_lw_ERBE_v3[0][0][0][:]),
                              title=f'{spectral_radiance_toa_lw_ERBE_v3.long_name}\n(at 2.5 nm 250-5000 nm)',
                              RAA=f'{ERBE_RAA_v3.values[0]}', SZA=f'{ERBE_SZA_v3.values[0]}', VZA=f'{ERBE_VZA_v3.values[0]}',
                              scene=f'{IGBP_Land_Type_v3.values}', data_version='v3')
plt.xscale('log')
plt.savefig("/Users/kese6848/Desktop/Figures/Spectral-ERBE-LW-v3.jpeg")
plt.close()

from modtran_analysis.tools.utils import sw_lw_wavelength, sw_lw_spectra

wavelength_v3 = sw_lw_wavelength(wavelength_v3_sw, wavelength_v3_lw)
spectral_radiance_toa_ERBE_v3 = sw_lw_spectra(spectral_radiance_toa_sw_ERBE_v3, spectral_radiance_toa_lw_ERBE_v3, RAA_bin=0, SZA_bin=0, VZA_bin=0)


plt.figure(figsize=(10,6))
plotting.plot_single_spectrum(wavelength_v3, spectrum_data=utils.unit_conversion(spectral_radiance_toa_ERBE_v3[:]),
                              title=f'MODTRAN6 Spectrally-Resolved Top-of-Atmosphere Radiance in wavelength units at ERBE ADM angles\n(at 2.5 nm 250-5000 nm)',
                              RAA=f'{ERBE_RAA_v3.values[0]}', SZA=f'{ERBE_SZA_v3.values[0]}', VZA=f'{ERBE_VZA_v3.values[0]}',
                              scene=f'{IGBP_Land_Type_v3.values}', data_version='v3')
plt.xscale('log')
plt.savefig("/Users/kese6848/Desktop/Figures/Spectral-ERBE-v3.jpeg")
plt.close()


plt.figure(figsize=(20,6))
plt.subplot(1,3,1)
plotting.plot_viewing_geometry(CERES_TRMM_RAA_v3, 'RAA', 'TRMM', data_version='v3')

plt.subplot(1,3,2)
plotting.plot_viewing_geometry(CERES_TRMM_SZA_v3, 'SZA', 'TRMM', data_version='v3')

plt.subplot(1,3,3)
plotting.plot_viewing_geometry(CERES_TRMM_VZA_v3, 'VZA', 'TRMM', data_version='v3')
plt.savefig("/Users/kese6848/Desktop/Figures/Viewing-Geometry-TRMM-v3.jpeg")
plt.close()

plt.figure(figsize=(10,6))
plotting.plot_single_spectrum(wavelength_v3_sw, spectrum_data=utils.unit_conversion(spectral_radiance_toa_sw_CERES_TRMM_v3[0][0][0][:]),
                              title=f'{spectral_radiance_toa_sw_CERES_TRMM_v3.long_name}\n(at 2.5 nm 250-5000 nm)',
                              RAA=f'{CERES_TRMM_RAA_v3.values[0]}', SZA=f'{CERES_TRMM_SZA_v3.values[0]}', VZA=f'{CERES_TRMM_VZA_v3.values[0]}',
                              scene=f'{IGBP_Land_Type_v3.values}', data_version='v3')
plt.xscale('log')
plt.savefig("/Users/kese6848/Desktop/Figures/Spectral-TRMM-SW-v3.jpeg")
plt.close()

plt.figure(figsize=(10,6))
plotting.plot_single_spectrum(wavelength_v3_lw, spectrum_data=utils.unit_conversion(spectral_radiance_toa_lw_CERES_TRMM_v3[0][0][0][:]),
                              title=f'{spectral_radiance_toa_lw_CERES_TRMM_v3.long_name}\n(at 2.5 nm 250-5000 nm)',
                              RAA=f'{CERES_TRMM_RAA_v3.values[0]}', SZA=f'{CERES_TRMM_SZA_v3.values[0]}', VZA=f'{CERES_TRMM_VZA_v3.values[0]}',
                              scene=f'{IGBP_Land_Type_v3.values}', data_version='v3')
plt.xscale('log')
plt.savefig("/Users/kese6848/Desktop/Figures/Spectral-TRMM-LW-v3.jpeg")
plt.close()

spectral_radiance_toa_CERES_TRMM_v3 = sw_lw_spectra(spectral_radiance_toa_sw_CERES_TRMM_v3, spectral_radiance_toa_lw_CERES_TRMM_v3, RAA_bin=0, SZA_bin=0, VZA_bin=0)

plt.figure(figsize=(10,6))
plotting.plot_single_spectrum(wavelength_v3, spectrum_data=utils.unit_conversion(spectral_radiance_toa_CERES_TRMM_v3[:]),
                              title=f'MODTRAN6 Spectrally-Resolved Top-of-Atmosphere Radiance in wavelength units at CERES-TRMM ADM angles\n(at 2.5 nm 250-5000 nm)',
                              RAA=f'{ERBE_RAA_v3.values[0]}', SZA=f'{ERBE_SZA_v3.values[0]}', VZA=f'{ERBE_VZA_v3.values[0]}',
                              scene=f'{IGBP_Land_Type_v3.values}', data_version='v3')
plt.xscale('log')
plt.savefig("/Users/kese6848/Desktop/Figures/Spectral-TRMM-v3.jpeg")
plt.close()

# -------------------------------------------------------------------------------------------------------------------------
# Plotting midrange spectra for v0
# ---- Compute absolute max radiance across all VZAs ----
global_max_radiance = max(
    utils.unit_conversion(spectral_radiance_toa_v0[i][2][4]).max().item()
    for i in range(len(VZA_v0))
)
plt.figure(figsize=(15, 12))

for i in range(len(VZA_v0)):
    vza_legend = VZA_v0.values[i]

    plotting.plot_single_spectrum(
        wavelength_data=wavelength_v0,
        spectrum_data=spectral_radiance_toa_v0[i][2][4],
        SZA=f'{SZA_v0.values[2]}',
        RAA=f'{RAA_v0.values[4]}',
        data_version='V0',
        label=f'VZA = {vza_legend}°',
        print_max_radiance=False
    )
plt.text(
    0.5, 0.95,
    f"Max Radiance (All VZA) = {global_max_radiance:.2f}\n"
    r"[$Watts/seradians/m^2/nm$]",
    transform=plt.gca().transAxes,
    ha='center',
    va='top',
    fontsize=10,
    bbox=dict(facecolor='white', alpha=0.6)
)
plt.legend(title="Viewing Zenith Angle")
plt.suptitle(f'All the VZA angles for RAA = {RAA_v0.values[4]} $\degree$ and SZA = {SZA_v0.values[2]} $\degree$\n Data Version V0', fontsize=14)
plt.tight_layout()
plt.xscale('log')
plt.savefig("/Users/kese6848/Desktop/Figures/Midrange-Viewing-v0.jpeg")
plt.close()
# -------------------------------------------------------------------------------------------------------------------------

# Plotting midrange for v1

# ---- Compute absolute max radiance across all VZAs ----
global_max_radiance = max(
    utils.unit_conversion(spectral_radiance_toa_v1[i][7][9]).max().item()
    for i in range(len(VZA_v1))
)
plt.figure(figsize=(15, 12))

for i in range(len(VZA_v1)):
    vza_legend = VZA_v1.values[i]

    plotting.plot_single_spectrum(
        wavelength_data=wavelength_v1,
        spectrum_data=spectral_radiance_toa_v1[i][7][9],
        SZA=f'{SZA_v1.values[7]}',
        RAA=f'{RAA_v1.values[9]}',
        scene=f'{IGBP_Land_Type_v1.values}',
        data_version='V1',
        label=f'VZA = {vza_legend}°',
        print_max_radiance=False
    )
plt.text(
    0.5, 0.95,
    f"Max Radiance (All VZA) = {global_max_radiance:.2f}\n"
    r"[$Watts/seradians/m^2/nm$]",
    transform=plt.gca().transAxes,
    ha='center',
    va='top',
    fontsize=10,
    bbox=dict(facecolor='white', alpha=0.6)
)
plt.legend(title="Viewing Zenith Angle")
plt.tight_layout()
plt.suptitle(f'All the VZA angles for RAA = {RAA_v1.values[9]} $\degree$ and SZA = {SZA_v1.values[7]} $\degree$ \n Data Version V1', fontsize=14)
plt.xscale('log')
plt.savefig("/Users/kese6848/Desktop/Figures/Midrange-Viewing-v1.jpeg")
plt.close()

# -------------------------------------------------------------------------------------------------------------------------

# Plotting midrange for v3
# ERBE SW
# ---- Compute absolute max radiance across all VZAs ----
global_max_radiance = max(
    utils.unit_conversion(spectral_radiance_toa_sw_ERBE_v3[i][2][4], use_microwatts=False).max().item()
    for i in range(len(ERBE_VZA_v3))
)
plt.figure(figsize=(15, 13))

for i in range(len(ERBE_VZA_v3)):
    vza_legend = ERBE_VZA_v3.values[i]

    plotting.plot_single_spectrum(wavelength_data=wavelength_v3_sw,
                                  spectrum_data=spectral_radiance_toa_sw_ERBE_v3[i][2][4],
                                  RAA=f'{ERBE_RAA_v3.values[4]}',
                                  SZA=f'{ERBE_SZA_v3.values[2]}', data_version='v3',
                                  scene=f'{IGBP_Land_Type_v3.values}', label=f'VZA = {vza_legend}°', print_max_radiance=False)
plt.text(
    0.5, 0.95,
    f"Max Radiance (All VZA) = {global_max_radiance:.2f}\n"
    r"[$Watts/seradians/m^2/nm$]",
    transform=plt.gca().transAxes,
    ha='center',
    va='top',
    fontsize=10,
    bbox=dict(facecolor='white', alpha=0.6)
)
plt.legend(title="Viewing Zenith Angle")
plt.tight_layout()
plt.suptitle(f'All the VZA angles for RAA = {ERBE_RAA_v3.values[4]} $\degree$ and SZA = {ERBE_SZA_v3.values[2]} $\degree$ \n Data Version v3 ERBE SW', fontsize=14)
plt.xscale('log')
plt.savefig("/Users/kese6848/Desktop/Figures/Midrange-Viewing-v3-ERBE-SW.jpeg")
plt.close()

# ERBE tot
# ---- Compute absolute max radiance across all VZAs ----
global_max_radiance = max(utils.unit_conversion(sw_lw_spectra(spectral_radiance_toa_sw_ERBE_v3, spectral_radiance_toa_lw_ERBE_v3, RAA_bin=4, SZA_bin=2, VZA_bin=i), use_microwatts=False).max().item()
    for i in range(len(ERBE_VZA_v3)))

plt.figure(figsize=(15, 13))

for i in range(len(ERBE_VZA_v3)):
    vza_legend = ERBE_VZA_v3.values[i]

    plotting.plot_single_spectrum(wavelength_data=wavelength_v3,
                                  spectrum_data=utils.unit_conversion(sw_lw_spectra(spectral_radiance_toa_sw_ERBE_v3, spectral_radiance_toa_lw_ERBE_v3, RAA_bin=4, SZA_bin=2, VZA_bin=i), use_microwatts=False),
                                  RAA=f'{ERBE_RAA_v3.values[4]}', SZA=f'{ERBE_SZA_v3.values[2]}', data_version='v3',
                                  scene=f'{IGBP_Land_Type_v3.values}', label=f'VZA = {vza_legend}°', print_max_radiance=False)
plt.text(
    0.5, 0.95,
    f"Max Radiance (All VZA) = {global_max_radiance:.2f}\n"
    r"[$Watts/seradians/m^2/nm$]",
    transform=plt.gca().transAxes,
    ha='center',
    va='top',
    fontsize=10,
    bbox=dict(facecolor='white', alpha=0.6)
)
plt.legend(title="Viewing Zenith Angle")
plt.tight_layout()
plt.xscale('log')
plt.suptitle(f'All the VZA angles for RAA = {ERBE_RAA_v3.values[4]} $\degree$ and SZA = {ERBE_SZA_v3.values[2]} $\degree$ \n Data Version v3 ERBE TOT', fontsize=14)

plt.savefig("/Users/kese6848/Desktop/Figures/Midrange-Viewing-v3-ERBE-tot.jpeg")
plt.close()

# -------------------------------------------------------------------------------------------------------------------------

# CERES SW
# ---- Compute absolute max radiance across all VZAs ----
global_max_radiance = max(
    utils.unit_conversion(spectral_radiance_toa_sw_CERES_TRMM_v3[i][4][5], use_microwatts=False).max().item()
    for i in range(len(CERES_TRMM_VZA_v3))
)
plt.figure(figsize=(15, 13))

for i in range(len(CERES_TRMM_VZA_v3)):
    vza_legend = CERES_TRMM_VZA_v3.values[i]

    plotting.plot_single_spectrum(wavelength_data=wavelength_v3_sw,
                                  spectrum_data=utils.unit_conversion(spectral_radiance_toa_sw_CERES_TRMM_v3[i][4][5], use_microwatts=False),
                                  RAA=f'{CERES_TRMM_RAA_v3.values[5]}',
                                  SZA=f'{CERES_TRMM_SZA_v3.values[4]}',
                                  data_version='V3',
                                  scene=f'{IGBP_Land_Type_v3.values}',
                                  label=f'VZA = {vza_legend}°',
                                  print_max_radiance=False)
plt.text(
    0.5, 0.95,
    f"Max Radiance (All VZA) = {global_max_radiance:.2f}\n"
    r"[$Watts/seradians/m^2/nm$]",
    transform=plt.gca().transAxes,
    ha='center',
    va='top',
    fontsize=10,
    bbox=dict(facecolor='white', alpha=0.6)
)
plt.legend(title="Viewing Zenith Angle")
plt.tight_layout()
plt.xscale('log')
plt.suptitle(f'All the VZA angles for RAA = {CERES_TRMM_RAA_v3.values[5]} $\degree$ and SZA = {CERES_TRMM_SZA_v3.values[4]} $\degree$ \n Data Version v3 CERES-TRMM SW', fontsize=14)
plt.savefig("/Users/kese6848/Desktop/Figures/Midrange-Viewing-v3-CERES-TRMM-SW.jpeg")
plt.close()

# CERES total
# ---- Compute absolute max radiance across all VZAs ----\
global_max_radiance = max(utils.unit_conversion(sw_lw_spectra(spectral_radiance_toa_sw_CERES_TRMM_v3, spectral_radiance_toa_lw_CERES_TRMM_v3, RAA_bin=5, SZA_bin=4, VZA_bin=i), use_microwatts=False).max().item()
    for i in range(len(CERES_TRMM_VZA_v3)))
plt.figure(figsize=(15, 13))

for i in range(len(CERES_TRMM_VZA_v3)):
    vza_legend = CERES_TRMM_VZA_v3.values[i]

    plotting.plot_single_spectrum(wavelength_data=wavelength_v3,
                                  spectrum_data=utils.unit_conversion(sw_lw_spectra(spectral_radiance_toa_sw_CERES_TRMM_v3,
                                                                                    spectral_radiance_toa_lw_CERES_TRMM_v3, RAA_bin=5, SZA_bin=4, VZA_bin=i),
                                                                      use_microwatts=False),
                                  RAA=f'{CERES_TRMM_RAA_v3.values[5]}', SZA=f'{CERES_TRMM_SZA_v3.values[4]}',
                                  VZA=f'{CERES_TRMM_VZA_v3.values[i]}', data_version='v3',
                                  scene=f'{IGBP_Land_Type_v3.values}', label=f'VZA = {vza_legend}°',
                                  print_max_radiance=False)
plt.text(
    0.5, 0.95,
    f"Max Radiance (All VZA) = {global_max_radiance:.2f}\n"
    r"[$Watts/seradians/m^2/nm$]",
    transform=plt.gca().transAxes,
    ha='center',
    va='top',
    fontsize=10,
    bbox=dict(facecolor='white', alpha=0.6)
)
plt.legend(title="Viewing Zenith Angle")
plt.xscale('log')
plt.tight_layout()
plt.suptitle(f'All the VZA angles for RAA = {CERES_TRMM_RAA_v3.values[5]} $\degree$ and SZA = {CERES_TRMM_SZA_v3.values[4]} $\degree$ \n Data Version v3 CERES-TRMM TOT', fontsize=14)

plt.savefig("/Users/kese6848/Desktop/Figures/Midrange-Viewing-v3-CERES-TRMM-total.jpeg")
plt.close()