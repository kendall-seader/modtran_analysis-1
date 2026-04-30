from modtran_analysis.tools import utils
from importlib import resources
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

LOCAL_DATA_PATH = resources.files("modtran_analysis") / "data"
#Here I just very quickly fixed things to try the v4 data, and renamed everything after this
DATA_FILE_PATH = LOCAL_DATA_PATH / "FV3_Modtran6_IO_v4_scene_106.nc"
ds_v4 = xr.open_dataset(DATA_FILE_PATH)

# todo i would like to find a way to make importing these things more "universal" and whatnot so that i can implement it over more things
''' thinking maybe a function where i say which ADM type, like if ERBE=True then import things with ERBE and if TRMM=True then swap them out '''

wavelength_v4_sw = ds_v4['wavelength_sw']
wavelength_v4_lw = ds_v4['wavelength_lw']
wavelength_v4_tot = utils.sw_lw_wavelength(wavelength_v4_sw, wavelength_v4_lw)

IGBP_Land_Type_v4 = ds_v4['IGBP_Type']
# above all of these consistent across all viewing geometries
############
### ERBE ###
############

ERBE_RAA_v4 = ds_v4['ERBE_RAA']
ERBE_SZA_v4 = ds_v4['ERBE_SZA']
ERBE_VZA_v4 = ds_v4['ERBE_VZA']
ERBE_SW_RAD = utils.unit_conversion(ds_v4['MODTRAN6_SW_RAD_TOA_ERBE'], use_microwatts=False)
ERBE_LW_RAD = utils.unit_conversion(ds_v4['MODTRAN6_LW_RAD_TOA_ERBE'], use_microwatts=False)
ERBE_NIR_RAD = utils.unit_conversion(ds_v4['MODTRAN6_NIR_RAD_TOA_ERBE'], use_microwatts=False)
ERBE_VIS_RAD = utils.unit_conversion(ds_v4['MODTRAN6_VIS_RAD_TOA_ERBE'], use_microwatts=False)
ERBE_TOT_RAD = utils.unit_conversion(ds_v4['MODTRAN6_TOT_RAD_TOA_ERBE'], use_microwatts=False)
ERBE_SW_FLUX = utils.unit_conversion(ds_v4['MODTRAN6_SW_FLX_UPDIF_ERBE'], use_microwatts=False)
ERBE_LW_FLUX = utils.unit_conversion(ds_v4['MODTRAN6_LW_FLX_UPDIF_ERBE'], use_microwatts=False)
ERBE_NIR_FLUX = utils.unit_conversion(ds_v4['MODTRAN6_NIR_FLX_UPDIF_ERBE'], use_microwatts=False)
ERBE_VIS_FLUX = utils.unit_conversion(ds_v4['MODTRAN6_VIS_FLX_UPDIF_ERBE'], use_microwatts=False)
ERBE_TOT_FLUX = utils.unit_conversion(ds_v4['MODTRAN6_TOT_FLX_UPDIF_ERBE'], use_microwatts=False)

#these are going to be integrated
spectral_radiance_toa_sw_ERBE_v4 = ds_v4['MODTRAN6_SPECTRAL_RADIANCE_TOA_SW_WVL_ERBE']
#this has a nan values in the first spot in every array, I THINK I SHOULD JUST CHOP IT??
# todo need to do some thinking and brainstoriming here because we have some values that are nan (specifically the first value of spectra which i am unsure why) and we need to make this consistent across all of the arrays
spectral_radiance_toa_lw_ERBE_v4 = ds_v4['MODTRAN6_SPECTRAL_RADIANCE_TOA_LW_WVL_ERBE']
#todo for here i am doing just a temp fix to have a table but i need to fix this indexing

# Starting here things need to be changed across all viewing geometries, these are ONLY for [0,0,0]
spectral_radiance_toa_tot_ERBE_v4 = utils.sw_lw_radiance(spectral_radiance_toa_sw_ERBE_v4, spectral_radiance_toa_lw_ERBE_v4, RAA_bin=0, VZA_bin=0, SZA_bin=0)

# Adding the integration
#this is with the chopping of the nans
# todo i would like to to find a better way to go about this because this is janky
integrated_sw_radiance = utils.integrate_spectrum(wavelength=wavelength_v4_sw[1:], spectrum_data=utils.unit_conversion(
    spectral_radiance_toa_sw_ERBE_v4[0][0][0][1:], use_microwatts=False))
# trimming\NIR (0.7 um - 5 um) (SW starts at 0.25 um)
print(spectral_radiance_toa_sw_ERBE_v4.shape)
# todo brainstorming here -- should i use an if statement or make a function?

spectral_radiance_toa_tot_ERBE_v4 = spectral_radiance_toa_tot_ERBE_v4.assign_coords(
    wavelength=("dim_0", wavelength_v4_tot.data)
)

min_NIR = 700
max_NIR = 5000
NIR_radiance = spectral_radiance_toa_tot_ERBE_v4.where(
    (spectral_radiance_toa_tot_ERBE_v4.wavelength >= min_NIR) &
    (spectral_radiance_toa_tot_ERBE_v4.wavelength <= max_NIR),
    drop=True
)
NIR_radiance = NIR_radiance.dropna(dim="dim_0")
wavelength_NIR_radiance = NIR_radiance.wavelength

integrated_NIR_radiance = utils.integrate_spectrum(wavelength=NIR_radiance.wavelength, spectrum_data=utils.unit_conversion(
    NIR_radiance, use_microwatts=False))
integrated_lw_radiance = utils.integrate_spectrum(wavelength=wavelength_v4_lw, spectrum_data=utils.unit_conversion(
    spectral_radiance_toa_lw_ERBE_v4, use_microwatts=False))
print(integrated_lw_radiance.shape)
integrated_tot_radiance = utils.integrate_spectrum(wavelength=wavelength_v4_tot[1:], spectrum_data=utils.unit_conversion(
    spectral_radiance_toa_tot_ERBE_v4[1:], use_microwatts=False))
integrated_VIS_radiance = integrated_sw_radiance - integrated_NIR_radiance

# todo add all of the flux integration
spectral_flux_updif_sw_ERBE_v4 = ds_v4['MODTRAN6_SPECTRAL_FLUX_UPDIF_SW_ERBE'] #these have nan's in them so i need to go through and figure that oart out
#the shape of this is (10,31,1901) where is this 31 coming from?! -- sza=10, levels=31, where are the other things?!
spectral_flux_updif_lw_ERBE_v4 = ds_v4['MODTRAN6_SPECTRAL_FLUX_UPDIF_LW_ERBE'] #in units of w/cm^2/nm
# todo check for 1e15 or nans??
spectral_flux_updif_tot_ERBE_v4 = utils.sw_lw_flux(spectral_flux_sw=spectral_flux_updif_sw_ERBE_v4, spectral_flux_lw=spectral_flux_updif_lw_ERBE_v4,SZA_bin=0, levels=0)
integrated_sw_flux = utils.integrate_spectrum(wavelength=wavelength_v4_sw[1:], spectrum_data=utils.unit_conversion(
    spectral_flux_updif_sw_ERBE_v4[0][0][1:], use_microwatts=False))
integrated_lw_flux = utils.integrate_spectrum(wavelength=wavelength_v4_lw[1:], spectrum_data=(
    utils.unit_conversion(spectral_flux_updif_lw_ERBE_v4[0][0][1:], use_microwatts=False)))

print(integrated_lw_flux)

min_NIR = 700 #nanometers
max_NIR = 5000 #nanometers
#todo try with total later
NIR_flux = spectral_flux_updif_sw_ERBE_v4.isel(erbe_solar_zenith_angle=0, Levels=0).where(
    (spectral_flux_updif_sw_ERBE_v4.wavelength_sw >= min_NIR) &
    (spectral_flux_updif_sw_ERBE_v4.wavelength_sw <= max_NIR),
    drop=True)
wavelength_NIR_flux = NIR_flux.wavelength_sw.values
integrated_NIR_flux = utils.integrate_spectrum(wavelength=wavelength_NIR_flux, spectrum_data=(
    utils.unit_conversion(xr.DataArray(NIR_flux), use_microwatts=False)))
integrated_VIS_flux = integrated_sw_flux - integrated_NIR_flux
integrated_tot_flux = utils.integrate_spectrum(wavelength=wavelength_v4_tot[1:], spectrum_data=(
    utils.unit_conversion(spectral_flux_updif_tot_ERBE_v4[1:], use_microwatts=False)))
print(utils.unit_conversion(spectral_flux_updif_tot_ERBE_v4[1:], use_microwatts=False))
print(spectral_flux_updif_lw_ERBE_v4)
#todo rewrite a spectral function for flux
'''
spectral_flux_updif_tot_ERBE_v4 = utils.sw_lw_radiance(spectral_flux_updif_sw_ERBE_v4, spectral_flux_updif_lw_ERBE_v4, RAA_bin=0, VZA_bin=0, SZA_bin=0)

# Adding the integration
#todo want to add bounds to the integration function
integrated_sw_flux = utils.integrate_spectrum(wavelength=wavelength_v4_sw, spectrum_data=spectral_flux_updif_sw_ERBE_v4)
# trimming NIR (0.7 um - 5 um) (SW starts at 0.25 um)

wavelength_NIR = []
spectral_flux_updif_NIR_ERBE_v4 = []
min_NIR = 700 #nanometers
max_NIR = 5000 #nanometers
for wavelength_NIR_filter, spectral_flux_updif_NIR_ERBE_v4_filter in zip(wavelength_v4_tot, spectral_flux_updif_tot_ERBE_v4):
    if min_NIR <= wavelength_NIR_filter <= max_NIR:
        wavelength_NIR.append(wavelength_NIR_filter)
        spectral_flux_updif_NIR_ERBE_v4.append(spectral_flux_updif_NIR_ERBE_v4_filter)

integrated_NIR_flux = utils.integrate_spectrum(wavelength=wavelength_NIR, spectrum_data=spectral_flux_updif_NIR_ERBE_v4)
integrated_lw_flux = utils.integrate_spectrum(wavelength=wavelength_v4_lw, spectrum_data=spectral_flux_updif_lw_ERBE_v4)
integrated_tot_flux = utils.integrate_spectrum(wavelength=wavelength_v4_tot, spectrum_data=spectral_flux_updif_tot_ERBE_v4)
# integrated_VIS_flux = integration.integrate_spectrum(wavelength= , spectrum_data= )
'''

##################
### CERES-TRMM ###
##################
CERES_TRMM_RAA_v4 = ds_v4['CERES_TRMM_RAA']
CERES_TRMM_SZA_v4 = ds_v4['CERES_TRMM_SZA']
CERES_TRMM_VZA_v4 = ds_v4['CERES_TRMM_VZA']

print(f'ceres sza = {CERES_TRMM_SZA_v4.values}')
print(f'ceres vza = {CERES_TRMM_VZA_v4.values}')
'''
CERES_TRMM_SW_RAD = ds_v4['MODTRAN6_SW_RAD_TOA_CERES-TRMM']
CERES_TRMM_LW_RAD = ds_v4['MODTRAN6_LW_RAD_TOA_CERES-TRMM']
CERES_TRMM_NIR_RAD = ds_v4['MODTRAN6_NIR_RAD_TOA_CERES_TRMM']
CERES_TRMM_VIS_RAD = ds_v4['MODTRAN6_VIS_RAD_TOA_CERES_TRMM']
CERES_TRMM_TOT_RAD = ds_v4['MODTRAN6_TOT_RAD_TOA_CERES_TRMM']
CERES_TRMM_SW_FLUX = ds_v4['MODTRAN6_SW_FLX_UPDIF_CERES_TRMM']
CERES_TRMM_LW_FLUX = ds_v4['MODTRAN6_LW_FLX_UPDIF_CERES-TRMM']
CERES_TRMM_NIR_FLUX = ds_v4['MODTRAN6_NIR_FLX_UPDIF_CERES_TRMM']
CERES_TRMM_VIS_FLUX = ds_v4['MODTRAN6_VIS_FLX_UPDIF_CERES_TRMM']
CERES_TRMM_TOT_FLUX = ds_v4['MODTRAN6_TOT_FLX_UPDIF_CERES_TRMM']
'''
spectral_radiance_toa_sw_CERES_TRMM_v4 = ds_v4['MODTRAN6_SPECTRAL_RADIANCE_TOA_SW_WVL_CERES_TRMM']
spectral_radiance_toa_lw_CERES_TRMM_v4 = ds_v4['MODTRAN6_SPECTRAL_RADIANCE_TOA_LW_WVL_CERES_TRMM']

radiance_vals = utils.integrate_spectrum(wavelength_v4_lw, spectral_radiance_toa_lw_ERBE_v4)
# TODO OK KEN YOU GOTTA WRITE SOME FUNCTIONS BECAUSE THIS IS JUST RANCID AND THINGS ARE GOING WRONG THAT I CANNOT TELL BECAUSE THERE ARE SO MANY PARTS
table_v4 = {
    'ADM-Type': ['ERBE'],
    'VZA': [ERBE_VZA_v4[0].values],
    'RAA': [ERBE_RAA_v4[0].values],
    'SZA': [ERBE_SZA_v4[0].values],
    'IGBP Scene': [IGBP_Land_Type_v4.values],
    'SW Radiance': [ERBE_SW_RAD[0][0][0].values],
    'INTEGRATED SW Radiance': [integrated_sw_radiance],
    'NIR Radiance': [ERBE_NIR_RAD[0][0][0].values],
    'INTEGRATED NIR Radiance': [integrated_NIR_radiance],
    'LW Radiance': [ERBE_LW_RAD[0][0][0].values],
    'INTEGRATED LW Radiance': [integrated_lw_radiance[0][0][0]],
    'VIS Radiance': [ERBE_VIS_RAD[0][0][0].values],
    'INTEGRATED VIS Radiance': [integrated_VIS_radiance],
    'Tot Radiance': [ERBE_TOT_RAD[0][0][0].values],
    'INTEGRATED TOT Radiance': [integrated_tot_radiance],
    'SW Flux': [ERBE_SW_FLUX[0][0].values],
    'INTEGRATED SW Flux': [integrated_sw_flux],
    'NIR Flux': [ERBE_NIR_FLUX[0][0].values],
    'INTEGRATED NIR Flux': [integrated_NIR_flux],
    'LW Flux': [ERBE_LW_FLUX[0][0].values],
    'INTEGRATED LW Flux': [integrated_lw_flux],
    'VIS Flux': [ERBE_VIS_FLUX[0][0].values],
    'INTEGRATED VIS Flux': [integrated_VIS_flux],
    'Tot Flux': [ERBE_TOT_FLUX[0][0].values],
    'INTEGRATED TOT Flux': [integrated_tot_flux],
    }


df = pd.DataFrame(table_v4)
pd.option_context('display.max_rows',None, 'display.max_columns',None)
df.to_csv('/Users/kese6848/modtran_analysis/modtran_analysis/data/table_draft.csv')
#why is it not showing everything :(

# df_func = pd.DataFrame(utils.table_output("FV3_Modtran6_IO_v4_scene_106.nc", 'ERBE', 0, 0, 0, 0))

sza_bins = [0, 1, 2]  # Example indices
vza_bins = [0, 1]
raa_bins = [0, 1]

all_results = []
#
# for s in sza_bins:
#     for v in vza_bins:
#         for r in raa_bins:
#             # Call your function for each geometry
#             row_data = utils.table_output("FV3_Modtran6_IO_v4_scene_106.nc", 'ERBE', r, s, v, 0)
#
#             # Convert the dictionary to a single-row DataFrame
#             all_results.append(pd.DataFrame(row_data))
#
# # Combine all rows into one final table
# final_table = pd.concat(all_results, ignore_index=True)



# pd.option_context('display.max_rows',None, 'display.max_columns',None)
# final_table.to_csv('/Users/kese6848/modtran_analysis/modtran_analysis/data/table_draft_function.csv')

from modtran_analysis.visualization import plotting
levels=[0,10,20,30]
SZA=[0,3,6,9]
for i in SZA:
    for level in levels:
        plt.figure(figsize=(10, 6))
        plotting.plot_single_spectrum(wavelength_data=wavelength_v4_lw, spectrum_data=(spectral_flux_updif_lw_ERBE_v4[i][level]), title='Long Wave Flux ERBE',
                                      SZA=ERBE_SZA_v4[i].values, scene=f'{IGBP_Land_Type_v4.values}', data_version='v4\nScene 106', label=f"level={level}")
        plt.text(.8, .85, f"Atmospheric level={level}", transform=plt.gca().transAxes,
                 ha='left', va='top', fontsize=10)
        plt.text(.8, .6, f"Integrated value={utils.integrate_spectrum(wavelength=wavelength_v4_lw[1:], spectrum_data=(utils.unit_conversion(spectral_flux_updif_lw_ERBE_v4[i][level][1:], use_microwatts=False))):.3e}", transform=plt.gca().transAxes,
                 ha='left', va='top', fontsize=10)
        plt.text(.8, .5,
                 f"Calculated value={ERBE_LW_FLUX[i][level].values:.3f}",
                 transform=plt.gca().transAxes,
                 ha='left', va='top', fontsize=10)
        plt.xscale('log')
        plt.savefig(f"/Users/kese6848/Desktop/Figures/ERBE-lw-flux-sza{i}-{level}.jpeg")
        plt.close()


plt.figure(figsize=(10, 6))
plotting.plot_single_spectrum(wavelength_data=wavelength_v4_lw, spectrum_data=spectral_radiance_toa_lw_ERBE_v4[0][0][0], title='Long Wave Radiance ERBE',
                                      SZA=f'{ERBE_SZA_v4[0].values}', RAA=f'{ERBE_RAA_v4[0].values}', VZA=f'{ERBE_VZA_v4[0].values}', scene=f'{IGBP_Land_Type_v4.values}', data_version='v4\nScene 106')
plt.text(.7, .7, f"Integrated Value={integrated_lw_radiance[0][0][0]:.3f}", transform=plt.gca().transAxes,
                 ha='left', va='top', fontsize=10)
plt.text(.7, .6, f"Calculated Value={ERBE_LW_RAD[0][0][0].values:.3f}", transform=plt.gca().transAxes,
                 ha='left', va='top', fontsize=10)
plt.xscale('log')
plt.savefig(f"/Users/kese6848/Desktop/Figures/ERBE-lw-radiance-v4.jpeg")
plt.close()

v5_table_sample = utils.table_output("FV3_Modtran6_IO_v5_scene_88.nc", 'ERBE', 0, 0, 0, 0)
df_v5 = pd.DataFrame(v5_table_sample)

sza_bins = [0, 1, 2, 3, 4, 5, 6, 7, 8 , 9]  # Example indices
vza_bins = [0, 1, 2, 3, 4, 5, 6]
raa_bins = [0, 1, 2, 3, 4, 5, 6, 7]

all_results = []

for s in sza_bins:
    for v in vza_bins:
        for r in raa_bins:
            # Call your function for each geometry
            v5_table_sample = utils.table_output("FV3_Modtran6_IO_v5_scene_88.nc", 'ERBE', r, s, v, 0)

            # Convert the dictionary to a single-row DataFrame
            all_results.append(pd.DataFrame(v5_table_sample))

# Combine all rows into one final table
final_table_v5 = pd.concat(all_results, ignore_index=True)



pd.option_context('display.max_rows',None, 'display.max_columns',None)
final_table_v5.to_csv('/Users/kese6848/modtran_analysis/modtran_analysis/data/v5-table-test.csv')



# todo still need to add the VIIRS radiance
'''
#this was a draft of how to implement the code for v0 (I specifically used this because it was the least amount of data)
#only worry about one line right now
for i in range(len(spectral_radiance_toa)):
    for j in range(len(spectral_radiance_toa[0])):
        for k in range(len(spectral_radiance_toa[0][0])):
            radiance = integrate_spectrum(wavelength, unit_conversion(spectral_radiance_toa[i][j][k]))
            table_draft['VZA'].append(VZA[i].values)
            table_draft['SZA'].append(SZA[j].values)
            table_draft['RAA'].append(RAA[k].values)
            table_draft['Radiance'].append(f'{radiance:.2f}')

            df = pd.DataFrame(table_draft)
'''


LOCAL_DATA_PATH = resources.files("modtran_analysis") / "data"
#Here I just very quickly fixed things to try the v4 data, and renamed everything after this
DATA_FILE_PATH = LOCAL_DATA_PATH / "FV3_Modtran6_IO_v5_scene_88.nc"
ds_v5 = xr.open_dataset(DATA_FILE_PATH)

# todo i would like to find a way to make importing these things more "universal" and whatnot so that i can implement it over more things
''' thinking maybe a function where i say which ADM type, like if ERBE=True then import things with ERBE and if TRMM=True then swap them out '''

wavelength_v5_sw = ds_v5['wavelength_sw']
wavelength_v5_lw = ds_v5['wavelength_lw']
wavelength_v5_tot = utils.sw_lw_wavelength(wavelength_v5_sw, wavelength_v5_lw)

IGBP_Land_Type_v5 = ds_v5['IGBP_Type_FV3']
# above all of these consistent across all viewing geometries
############
### ERBE ###
############

ERBE_RAA_v5 = ds_v5['ERBE_RAA']
ERBE_SZA_v5 = ds_v5['ERBE_SZA']
ERBE_VZA_v5 = ds_v5['ERBE_VZA']
ERBE_SW_RAD = utils.unit_conversion(ds_v5['MODTRAN6_SW_RAD_TOA_ERBE'], use_microwatts=False)
ERBE_LW_RAD = utils.unit_conversion(ds_v5['MODTRAN6_LW_RAD_TOA_ERBE'], use_microwatts=False)
ERBE_NIR_RAD = utils.unit_conversion(ds_v5['MODTRAN6_NIR_RAD_TOA_ERBE'], use_microwatts=False)
ERBE_VIS_RAD = utils.unit_conversion(ds_v5['MODTRAN6_VIS_RAD_TOA_ERBE'], use_microwatts=False)
ERBE_TOT_RAD = utils.unit_conversion(ds_v5['MODTRAN6_TOT_RAD_TOA_ERBE'], use_microwatts=False)
ERBE_SW_FLUX = utils.unit_conversion(ds_v5['MODTRAN6_SW_FLX_UPDIF_ERBE'], use_microwatts=False)
ERBE_LW_FLUX = utils.unit_conversion(ds_v5['MODTRAN6_LW_FLX_UPDIF_ERBE'], use_microwatts=False)
ERBE_NIR_FLUX = utils.unit_conversion(ds_v5['MODTRAN6_NIR_FLX_UPDIF_ERBE'], use_microwatts=False)
ERBE_VIS_FLUX = utils.unit_conversion(ds_v5['MODTRAN6_VIS_FLX_UPDIF_ERBE'], use_microwatts=False)
ERBE_TOT_FLUX = utils.unit_conversion(ds_v5['MODTRAN6_TOT_FLX_UPDIF_ERBE'], use_microwatts=False)

#these are going to be integrated
spectral_radiance_toa_sw_ERBE_v5 = ds_v5['MODTRAN6_SPECTRAL_RADIANCE_TOA_SW_WVL_ERBE']
#this has a nan values in the first spot in every array, I THINK I SHOULD JUST CHOP IT??
# todo need to do some thinking and brainstoriming here because we have some values that are nan (specifically the first value of spectra which i am unsure why) and we need to make this consistent across all of the arrays
spectral_radiance_toa_lw_ERBE_v5 = ds_v5['MODTRAN6_SPECTRAL_RADIANCE_TOA_LW_WVL_ERBE']
#todo for here i am doing just a temp fix to have a table but i need to fix this indexing

# Starting here things need to be changed across all viewing geometries, these are ONLY for [0,0,0]
spectral_radiance_toa_tot_ERBE_v5 = utils.sw_lw_radiance(spectral_radiance_toa_sw_ERBE_v5, spectral_radiance_toa_lw_ERBE_v5, RAA_bin=0, VZA_bin=0, SZA_bin=0)

# Adding the integration
#this is with the chopping of the nans
# todo i would like to to find a better way to go about this because this is janky
integrated_sw_radiance = utils.integrate_spectrum(wavelength=wavelength_v5_sw[1:], spectrum_data=utils.unit_conversion(
    spectral_radiance_toa_sw_ERBE_v5[0][0][0][1:], use_microwatts=False))
# trimming\NIR (0.7 um - 5 um) (SW starts at 0.25 um)
print(spectral_radiance_toa_sw_ERBE_v5.shape)
# todo brainstorming here -- should i use an if statement or make a function?

spectral_radiance_toa_tot_ERBE_v5 = spectral_radiance_toa_tot_ERBE_v5.assign_coords(
    wavelength=("dim_0", wavelength_v5_tot.data)
)

min_NIR = 700
max_NIR = 5000
NIR_radiance = spectral_radiance_toa_tot_ERBE_v5.where(
    (spectral_radiance_toa_tot_ERBE_v5.wavelength >= min_NIR) &
    (spectral_radiance_toa_tot_ERBE_v5.wavelength <= max_NIR),
    drop=True
)
NIR_radiance = NIR_radiance.dropna(dim="dim_0")
wavelength_NIR_radiance = NIR_radiance.wavelength

integrated_NIR_radiance = utils.integrate_spectrum(wavelength=NIR_radiance.wavelength, spectrum_data=utils.unit_conversion(
    NIR_radiance, use_microwatts=False))
integrated_lw_radiance = utils.integrate_spectrum(wavelength=wavelength_v5_lw, spectrum_data=utils.unit_conversion(
    spectral_radiance_toa_lw_ERBE_v5, use_microwatts=False))
print(integrated_lw_radiance.shape)
integrated_tot_radiance = utils.integrate_spectrum(wavelength=wavelength_v5_tot[1:], spectrum_data=utils.unit_conversion(
    spectral_radiance_toa_tot_ERBE_v5[1:], use_microwatts=False))
integrated_VIS_radiance = integrated_sw_radiance - integrated_NIR_radiance

# todo add all of the flux integration
spectral_flux_updif_sw_ERBE_v5 = ds_v5['MODTRAN6_SPECTRAL_FLUX_UPDIF_SW_ERBE'] #these have nan's in them so i need to go through and figure that oart out
#the shape of this is (10,31,1901) where is this 31 coming from?! -- sza=10, levels=31, where are the other things?!
spectral_flux_updif_lw_ERBE_v5 = ds_v5['MODTRAN6_SPECTRAL_FLUX_UPDIF_LW_ERBE'] #in units of w/cm^2/nm
# todo check for 1e15 or nans??
spectral_flux_updif_tot_ERBE_v5 = utils.sw_lw_flux(spectral_flux_sw=spectral_flux_updif_sw_ERBE_v5, spectral_flux_lw=spectral_flux_updif_lw_ERBE_v5,SZA_bin=0, levels=0)
integrated_sw_flux = utils.integrate_spectrum(wavelength=wavelength_v5_sw[1:], spectrum_data=utils.unit_conversion(
    spectral_flux_updif_sw_ERBE_v5[0][0][1:], use_microwatts=False))
integrated_lw_flux = utils.integrate_spectrum(wavelength=wavelength_v5_lw[1:], spectrum_data=(
    utils.unit_conversion(spectral_flux_updif_lw_ERBE_v5[0][0][1:], use_microwatts=False)))

print(integrated_lw_flux)

min_NIR = 700 #nanometers
max_NIR = 5000 #nanometers
#todo try with total later
NIR_flux = spectral_flux_updif_sw_ERBE_v5.isel(erbe_solar_zenith_angle=0, Levels=0).where(
    (spectral_flux_updif_sw_ERBE_v5.wavelength_sw >= min_NIR) &
    (spectral_flux_updif_sw_ERBE_v5.wavelength_sw <= max_NIR),
    drop=True)
wavelength_NIR_flux = NIR_flux.wavelength_sw.values
integrated_NIR_flux = utils.integrate_spectrum(wavelength=wavelength_NIR_flux, spectrum_data=(
    utils.unit_conversion(xr.DataArray(NIR_flux), use_microwatts=False)))
integrated_VIS_flux = integrated_sw_flux - integrated_NIR_flux
integrated_tot_flux = utils.integrate_spectrum(wavelength=wavelength_v5_tot[1:], spectrum_data=(
    utils.unit_conversion(spectral_flux_updif_tot_ERBE_v5[1:], use_microwatts=False)))

levels=[0,10,20,30]
SZA=[0,3,6,9]
for i in SZA:
    for level in levels:
        plt.figure(figsize=(10, 6))
        plotting.plot_single_spectrum(wavelength_data=wavelength_v5_lw, spectrum_data=(spectral_flux_updif_lw_ERBE_v5[i][level]), title='Long Wave Flux ERBE',
                                      SZA=ERBE_SZA_v5[i].values, scene=f'{IGBP_Land_Type_v5.values}', data_version='v5\nScene 88', label=f"level={level}")
        plt.text(.8, .85, f"Atmospheric level={level}", transform=plt.gca().transAxes,
                 ha='left', va='top', fontsize=10)
        plt.text(.8, .6, f"Integrated value={utils.integrate_spectrum(wavelength=wavelength_v5_lw[1:], spectrum_data=(utils.unit_conversion(spectral_flux_updif_lw_ERBE_v5[i][level][1:], use_microwatts=False))):.3e}", transform=plt.gca().transAxes,
                 ha='left', va='top', fontsize=10)
        plt.text(.8, .5,
                 f"Calculated value={ERBE_LW_FLUX[i][level].values:.3f}",
                 transform=plt.gca().transAxes,
                 ha='left', va='top', fontsize=10)
        plt.xscale('log')
        plt.savefig(f"/Users/kese6848/Desktop/Figures/ERBE-lw-flux-sza{i}-{level}.jpeg")
        plt.close()

plt.figure(figsize=(10, 6))
plotting.plot_single_spectrum(wavelength_data=wavelength_v5_lw, spectrum_data=spectral_radiance_toa_lw_ERBE_v5[0][0][0], title='Long Wave Radiance ERBE',
                                      SZA=f'{ERBE_SZA_v5[0].values}', RAA=f'{ERBE_RAA_v5[0].values}', VZA=f'{ERBE_VZA_v5[0].values}', scene=f'{IGBP_Land_Type_v5.values}', data_version='v5\nScene 88')
plt.text(.7, .7, f"Integrated Value={integrated_lw_radiance[0][0][0]:.3f}", transform=plt.gca().transAxes,
                 ha='left', va='top', fontsize=10)
plt.text(.7, .6, f"Calculated Value={ERBE_LW_RAD[0][0][0].values:.3f}", transform=plt.gca().transAxes,
                 ha='left', va='top', fontsize=10)
plt.xscale('log')
plt.savefig(f"/Users/kese6848/Desktop/Figures/ERBE-lw-radiance-v5.jpeg")
plt.close()

#### SOOOO many tables yay!!

sza_bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
vza_bins = [0, 1, 2, 3, 4, 5, 6]
raa_bins = [0, 1, 2, 3, 4, 5, 6, 7]

data_files = list(range(1, 129))
missing = [10, 11, 41, 54, 55, 56, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122]
for i in range(len(missing)):
    data_files.remove(missing[i])


for data_file in data_files:
    all_results = []
    for s in sza_bins:
        for v in vza_bins:
            for r in raa_bins:
                # Call your function for each geometry
                v5_table_sample = utils.table_output(f"v5/FV3_Modtran6_IO_v5_scene_{data_files[data_file-1]}.nc", 'ERBE', r, s, v, 0)

                # Convert the dictionary to a single-row DataFrame
                all_results.append(pd.DataFrame(v5_table_sample))

    # Combine all rows into one final table
    final_table_v5 = pd.concat(all_results, ignore_index=True)



    pd.option_context('display.max_rows',None, 'display.max_columns',None)
    final_table_v5.to_csv(f'/Users/kese6848/modtran_analysis/modtran_analysis/data/v5-tables/v5-table-{data_files[data_file-1]}.csv')



