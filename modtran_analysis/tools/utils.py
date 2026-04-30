import numpy as np
import xarray as xr
import scipy.integrate as integrate


# todo can add an is flux true or whatever
def sw_lw_radiance(spectral_radiance_toa_sw: xr.DataArray = None, spectral_radiance_toa_lw: xr.DataArray = None, RAA_bin: float = None, VZA_bin: float = None, SZA_bin: float = None):
    '''
    Combines the spectral radiance for shortwave wavelengths and longwave wavelengths.

    Using the arrays of shortwave radiance and longwave radiance this function creates a longer array with the two arrays appended together.

    Parameters
    -----------
    spectral_radiance_toa_sw: xr.DataArray
        Input the shortwave spectral radiance for a given variable

    spectral_radiance_toa_lw: xr.DataArray
        Input the longwave spectral radiance for the same variable as the shortwave spectral radiance

    RAA_bin: str
        Input the bin of the Relative Azimuth Angle (RAA) of which you would like to observe

    VZA_bin: str
        Input the bin of the Viewing Zenith Angle (VZA) of which you would like to observe

    SZA_bin: str
        Input the bin of the Solar Zenith Angle (SZA) of which you would like to observe

    Returns
    -------
        An xr.DataArray of the total spectral radiance over all given wavelengths (both shortwave and longwave wavelengths)

    Example
    -------
        sw_lw_spectra(spectral_radiance_toa_sw, spectral_radiance_toa_lw, RAA_bin=0, VZA_bin=0, SZA_bin=0)
    '''
    spectral_radiance_toa = np.append(spectral_radiance_toa_sw[VZA_bin][SZA_bin][RAA_bin][:], spectral_radiance_toa_lw[VZA_bin][SZA_bin][RAA_bin][:])
    return xr.DataArray(spectral_radiance_toa)

def sw_lw_flux(spectral_flux_sw: xr.DataArray = None, spectral_flux_lw: xr.DataArray = None, SZA_bin: float = None, levels: float = None):
    '''
    Combines the spectral radiance for shortwave wavelengths and longwave wavelengths.

    Using the arrays of shortwave radiance and longwave radiance this function creates a longer array with the two arrays appended together.

    Parameters
    -----------
    spectral_flux_sw: xr.DataArray
        Input the shortwave spectral flux for a given variable

    spectral_flux_lw: xr.DataArray
        Input the longwave spectral flux for the same variable as the shortwave spectral flux

    SZA_bin: str
        SZA bin you wish to observe (note that this is not the same as radiance)

    levels: float
        Atmospheric levels for calculating the flux

    Returns
    -------
        An xr.DataArray of the total spectral flux over all given wavelengths (both shortwave and longwave wavelengths)

    Example
    -------
        sw_lw_flux(spectral_flux_sw, spectral_flux_lw, SZA_bin=0, levels=0)
    '''
    spectral_flux_toa = np.append(spectral_flux_sw[SZA_bin][levels][:], spectral_flux_lw[SZA_bin][levels][:])
    return xr.DataArray(spectral_flux_toa)

def sw_lw_wavelength(sw_wavelength: xr.DataArray = None, lw_wavelength: xr.DataArray = None):
    '''
    Combines the shortwave wavelengths and longwave wavelengths.

    Using the arrays of shortwave wavelengths and longwave wavelengths, this function creates a longer array with the two arrays appended together,
    creating the TOTAL wavelength values.

    Parameters
    -----------
    sw_wavelength: xr.DataArray
        Input the shortwave wavelengths of a data version.

    lw_wavelength: xr.DataArray
        Input the longwave wavelengths of a data version.


    Returns
    -------
        An xr.DataArray of the total given wavelengths (both shortwave and longwave wavelengths)

    Example
    -------
        sw_lw_wavelength(sw_wavelength, lw_wavelength)
    '''
    tot_wavelength = np.append(sw_wavelength,
                                lw_wavelength)
    return xr.DataArray(tot_wavelength)

def unit_conversion(radiance: xr.DataArray | float, use_microwatts: bool = True):
    '''
    This function converts radiance values from (micro-watts / steradians / cm^2 / nm) to (Watts / steradians / m^2 / nm)

    radiance: xr.DataArray or float
        Radiance array from the input data

    use_microwatts: bool
        If True, convert radiance from microwatts to watts

    Returns an array of corrected units
    '''
    if isinstance(radiance, float) or isinstance(radiance, xr.DataArray):
        watt_conversion = 1
        if use_microwatts:
            watt_conversion = 10 ** -6
        cmsquared_to_msquared_conv = 10000
        return radiance * watt_conversion * cmsquared_to_msquared_conv
        #confused what thw row below is even doing?
        # cmsquared_to_msquares = microwatts_to_watts * 10000  # m^2, cm is in the denominator for these units
        # return cmsquared_to_msquares

    else:
        raise TypeError(f"Expected 'float' or DataArray for radiance, got {type(radiance).__name__} instead.")


def integrate_spectrum(wavelength, spectrum_data):
    '''
    integrating spectral radiances for modtran data using the simpson method
    THIS IF FOR JUST ONE SPECTRUM
    Parameters
    ----------
    wavelength : xr.DataArray

    spectrum_data : xr.DataArray
        Function we are integrating over
    Returns
    -------
    result : float
       Integrated spectral radiance
    '''

    x = np.asarray(wavelength)
    y = np.asarray(spectrum_data)
    result = integrate.simpson(y, x)
    return result



def table_output(filename: str, ADM_type: str, RAA_bin: float, SZA_bin: float, VZA_bin: float, flux_level: float):
    '''
    This function creates a dictionary of Modtran data outputs (want to make it so that it gives a pandas table??)

    Parameters
    ----------
    filename: str
        The file name of the data you wish to look at.
        This path needs to be in along the lines of '~/modtran_analysis/modtran_analysis/data' (in the data folder of where you
        are working within the modtran_analysis folder)

    ADM_type : str
        Type of ADM, (i.e. 'ERBE', 'CERES-TRMM')

    RAA_bin : float
        Relative Azimuth Angle bin
        for ERBE: [0,1,2,3,4,5,6,7]
        for CERES-TRMM: [0,1,2,3,4,5,6,7,8,9]

    SZA_bin : float
        Solar Zenith Angle bin
        for ERBE: [0,1,2,3,4,5,6,7,8,9]
        for CERES-TRMM: [0,1,2,3,4,5,6,7,8]

    VZA_bin : float
        Viewing Zenith Angle bin
        for ERBE: [0,1,2,3,4,5,6]
        for CERES-TRMM: [0,1,2,3,4,5,6,7,8]

    flux_level: float
        Flux level of the modtran data
        flux level zero is the top of the atmosphere, flux level 31 is the surface of the Earth


    Returns
    -------
    A dictionary of the modtran data outputs, along with unit converted data and integrated spectra to compare with modtran calculated data.
    '''
    from importlib import resources
    from libera_utils.scene_id import IGBPSurfaceType


    LOCAL_DATA_PATH = resources.files("modtran_analysis") / "data"
    DATA_FILE_PATH = LOCAL_DATA_PATH / filename
    ds = xr.open_dataset(DATA_FILE_PATH)
    wavelength_sw = ds['wavelength_sw']
    wavelength_lw = ds['wavelength_lw']
    wavelength_tot = sw_lw_wavelength(wavelength_sw, wavelength_lw)
    IGBP_Land_Type = ds.get('IGBP_Type', ds.get('IGBP_Type_FV3'))
    surface = IGBPSurfaceType(IGBP_Land_Type).trmm_surface_type.name

    RAA = ds[f'{ADM_type}_RAA']
    SZA = ds[f'{ADM_type}_SZA']
    VZA = ds[f'{ADM_type}_VZA']
    SW_RAD = unit_conversion(ds[f'MODTRAN6_SW_RAD_TOA_{ADM_type}'], use_microwatts=False)
    LW_RAD = unit_conversion(ds[f'MODTRAN6_LW_RAD_TOA_{ADM_type}'], use_microwatts=False)
    NIR_RAD = unit_conversion(ds[f'MODTRAN6_NIR_RAD_TOA_{ADM_type}'], use_microwatts=False)
    VIS_RAD = unit_conversion(ds[f'MODTRAN6_VIS_RAD_TOA_{ADM_type}'], use_microwatts=False)
    TOT_RAD = unit_conversion(ds[f'MODTRAN6_TOT_RAD_TOA_{ADM_type}'], use_microwatts=False)
    SW_FLUX = unit_conversion(ds[f'MODTRAN6_SW_FLX_UPDIF_{ADM_type}'], use_microwatts=False)
    LW_FLUX = unit_conversion(ds[f'MODTRAN6_LW_FLX_UPDIF_{ADM_type}'], use_microwatts=False)
    NIR_FLUX = unit_conversion(ds[f'MODTRAN6_NIR_FLX_UPDIF_{ADM_type}'], use_microwatts=False)
    VIS_FLUX = unit_conversion(ds[f'MODTRAN6_VIS_FLX_UPDIF_{ADM_type}'], use_microwatts=False)
    TOT_FLUX = unit_conversion(ds[f'MODTRAN6_TOT_FLX_UPDIF_{ADM_type}'], use_microwatts=False)



    # Metadata labels: (VZA, SZA, RAA, Spectral)
    # Shapes: ERBE=(7, 10, 8, nw), TRMM=(9, 9, 10, nw)
    nv, ns, nr, nw = ds[f'MODTRAN6_SPECTRAL_RADIANCE_TOA_SW_WVL_{ADM_type}'].shape
    data = ds[f'MODTRAN6_SPECTRAL_RADIANCE_TOA_SW_WVL_{ADM_type}'].values

    # Reconstruction Logic:
    # The data was flattened in (VZA, RAA, SZA) order
    # So we reshape to (VZA, RAA, SZA, nw)
    fixed_data = data.reshape(nv, nr, ns, nw)
    # Then transpose back to (VZA, SZA, RAA, nw) to match metadata labels
    spectral_radiance_toa_sw = fixed_data.transpose(0, 2, 1, 3)



    # Metadata labels: (VZA, SZA, RAA, Spectral)
    # Shapes: ERBE=(7, 10, 8, nw), TRMM=(9, 9, 10, nw)
    nv, ns, nr, nw = ds[f'MODTRAN6_SPECTRAL_RADIANCE_TOA_LW_WVL_{ADM_type}'].shape
    data = ds[f'MODTRAN6_SPECTRAL_RADIANCE_TOA_LW_WVL_{ADM_type}'].values

    # Reconstruction Logic:
    # The data was flattened in (VZA, RAA, SZA) order
    # So we reshape to (VZA, RAA, SZA, nw)
    fixed_data = data.reshape(nv, nr, ns, nw)
    # Then transpose back to (VZA, SZA, RAA, nw) to match metadata labels
    spectral_radiance_toa_lw = fixed_data.transpose(0, 2, 1, 3)


    spectral_radiance_toa_tot = sw_lw_radiance(spectral_radiance_toa_sw,
                                                             spectral_radiance_toa_lw, RAA_bin, VZA_bin,
                                                             SZA_bin)
    integrated_sw_radiance = integrate_spectrum(wavelength=wavelength_sw[1:],
                                                spectrum_data=unit_conversion(
                                                    xr.DataArray(spectral_radiance_toa_sw[VZA_bin][SZA_bin][RAA_bin][1:]),
                                                    use_microwatts=False))

    spectral_radiance_toa_tot = spectral_radiance_toa_tot.assign_coords(
        wavelength=("dim_0", wavelength_tot.data)
    )

    min_NIR = 700
    max_NIR = 5000
    NIR_radiance = spectral_radiance_toa_tot.where(
        (spectral_radiance_toa_tot.wavelength >= min_NIR) &
        (spectral_radiance_toa_tot.wavelength <= max_NIR),
        drop=True
    )
    NIR_radiance = NIR_radiance.dropna(dim="dim_0")
    wavelength_NIR_radiance = NIR_radiance.wavelength

    integrated_NIR_radiance = integrate_spectrum(wavelength=NIR_radiance.wavelength,
                                                 spectrum_data=unit_conversion(NIR_radiance, use_microwatts=False))
    integrated_lw_radiance = integrate_spectrum(wavelength=wavelength_lw,
                                                spectrum_data=unit_conversion(xr.DataArray(spectral_radiance_toa_lw),
                                                                              use_microwatts=False))
    integrated_tot_radiance = integrate_spectrum(wavelength=wavelength_tot[1:],
                                                 spectrum_data=unit_conversion(spectral_radiance_toa_tot[1:],
                                                                               use_microwatts=False))
    integrated_VIS_radiance = integrated_sw_radiance - integrated_NIR_radiance

    spectral_flux_updif_sw = ds[f'MODTRAN6_SPECTRAL_FLUX_UPDIF_SW_{ADM_type}']
    spectral_flux_updif_lw = ds[f'MODTRAN6_SPECTRAL_FLUX_UPDIF_LW_{ADM_type}']
    integrated_sw_flux = integrate_spectrum(wavelength=wavelength_sw[1:],
                                            spectrum_data=unit_conversion(
                                                spectral_flux_updif_sw[SZA_bin][flux_level][1:], use_microwatts=False))
    integrated_lw_flux = integrate_spectrum(wavelength=wavelength_lw[1:], spectrum_data=(
        unit_conversion(spectral_flux_updif_lw[SZA_bin][flux_level][1:], use_microwatts=False)))

    spectral_flux_updif_tot = sw_lw_flux(
        spectral_flux_sw=spectral_flux_updif_sw,
        spectral_flux_lw=spectral_flux_updif_lw,
        SZA_bin=SZA_bin,
        levels=flux_level
    )
    min_NIR = 700  # nanometers
    max_NIR = 5000  # nanometers
    # todo try with total later
    NIR_flux = spectral_flux_updif_sw.isel(erbe_solar_zenith_angle=SZA_bin, Levels=flux_level).where(
        (spectral_flux_updif_sw.wavelength_sw >= min_NIR) &
        (spectral_flux_updif_sw.wavelength_sw <= max_NIR),
        drop=True)
    wavelength_NIR_flux = NIR_flux.wavelength_sw.values
    integrated_NIR_flux = integrate_spectrum(wavelength=wavelength_NIR_flux, spectrum_data=(
        unit_conversion(xr.DataArray(NIR_flux), use_microwatts=False)))
    integrated_VIS_flux = integrated_sw_flux - integrated_NIR_flux
    integrated_tot_flux = integrate_spectrum(wavelength=wavelength_tot[1:], spectrum_data=(
        unit_conversion(spectral_flux_updif_tot[1:], use_microwatts=False)))
    import modtran_analysis.visualization.plotting as plotting
    import matplotlib.pyplot as plt
    diff = abs(integrated_sw_radiance - SW_RAD[RAA_bin][SZA_bin][VZA_bin].values) / SW_RAD[RAA_bin][SZA_bin][VZA_bin].values
    if diff > 0.03:
        plt.figure(figsize=(10, 6))
        plotting.plot_single_spectrum(wavelength_data=wavelength_tot,
                                      spectrum_data=spectral_radiance_toa_tot,
                                      title=f'Totoal Radiance {ADM_type}',
                                      SZA=f'{SZA[SZA_bin].values}', RAA=f'{RAA[RAA_bin].values}',
                                      VZA=f'{VZA[VZA_bin].values}', scene=f'{IGBP_Land_Type.values}',
                                      data_version=filename.translate(str.maketrans('', '', 'FV3_Modtran6_IO.nce')))

        plt.text(.7, .7, f"Integrated Value={integrated_sw_radiance:.3f}", transform=plt.gca().transAxes,
                 ha='left', va='top', fontsize=10)
        plt.text(.7, .6, f"Calculated Value={SW_RAD[RAA_bin][SZA_bin][VZA_bin].values:.3f}", transform=plt.gca().transAxes,
                 ha='left', va='top', fontsize=10)
        plt.xscale('log')
        folder_path = f"/Users/kese6848/Desktop/Figures/{filename.replace('.nc', '')}_graphs"
        import os
        os.makedirs(folder_path, exist_ok=True)
        plt.savefig(f"{folder_path}/wacky-wavelength-VZA{VZA_bin}_SZA{SZA_bin}_RAA{RAA_bin}.jpeg")
        plt.close()

    table_dict = {
        'ADM-Type': [ADM_type],
        'VZA': [VZA[VZA_bin].values],
        'RAA': [RAA[RAA_bin].values],
        'SZA': [SZA[SZA_bin].values],
        'IGBP Scene': [surface],
        'SW Radiance': [f'{SW_RAD[RAA_bin][SZA_bin][VZA_bin].values:.3f}'],
        'INTEGRATED SW Radiance': [f'{integrated_sw_radiance:.3f}'],
        'NIR Radiance': [f'{NIR_RAD[RAA_bin][SZA_bin][VZA_bin].values:.3f}'],
        'INTEGRATED NIR Radiance': [f'{integrated_NIR_radiance:.3f}'],
        'LW Radiance': [f'{LW_RAD[RAA_bin][SZA_bin][VZA_bin].values:.3f}'],
        'INTEGRATED LW Radiance': [f'{integrated_lw_radiance[VZA_bin][SZA_bin][RAA_bin]:.3f}'],
        'VIS Radiance': [f'{VIS_RAD[RAA_bin][SZA_bin][VZA_bin].values:.3f}'],
        'INTEGRATED VIS Radiance': [f'{integrated_VIS_radiance:.3f}'],
        'Tot Radiance': [f'{TOT_RAD[RAA_bin][SZA_bin][VZA_bin].values:.3f}'],
        'INTEGRATED TOT Radiance': [f'{integrated_tot_radiance:.3f}'],
        'SW Flux': [f'{SW_FLUX[SZA_bin][flux_level].values:.3f}'],
        'INTEGRATED SW Flux': [f'{integrated_sw_flux:.3f}'],
        'NIR Flux': [f'{NIR_FLUX[SZA_bin][flux_level].values:.3f}'],
        'INTEGRATED NIR Flux': [f'{integrated_NIR_flux:.3f}'],
        'LW Flux': [f'{LW_FLUX[SZA_bin][flux_level].values:.3f}'],
        'INTEGRATED LW Flux': [f'{integrated_lw_flux:.3f}'],
        'VIS Flux': [f'{VIS_FLUX[SZA_bin][flux_level].values:.3f}'],
        'INTEGRATED VIS Flux': [f'{integrated_VIS_flux:.3f}'],
        'Tot Flux': [f'{TOT_FLUX[SZA_bin][flux_level].values:.3f}'],
        'INTEGRATED TOT Flux': [f'{integrated_tot_flux:.3f}'],
    }

    import pandas as pd
    final_table = pd.DataFrame(table_dict)
    return pd.DataFrame(table_dict), final_table

def table_summary (filename, table_path):
    '''
    In this, we want to parse Modtran data files and get the useful information and plots out from it.
    While we do still have the function to give us specific data, this one is entirely just to give us the
    overall idea of what this data file says.

    Parameters
    ----------
    filename : str

    table : dict
    MUST be the table from utils.table_output

    Returns
    -------
    - Scene type of the file
    - The maximum radiance and flux and what viewing geometry this occurs at
    - A representational numerical plot of flux values across viewing geometries; calculating the mean and standard deviation
    of the data (
    - lat and lon of the file
    - TRMM surface type
    - cloud fraction number from test file
    - calculate actural ERBE scene id


    '''
    from importlib import resources
    import numpy as np
    import pandas as pd
    import xarray as xr
    import matplotlib.pyplot as plt
    table = pd.read_csv(table_path)
    column_names = ['<anonymous>',
        'ADM-Type',
        'VZA',
        'RAA',
        'SZA',
        'IGBP Scene',
        'SW Radiance',
        'INTEGRATED SW Radiance',
        'NIR Radiance',
        'INTEGRATED NIR Radiance',
        'LW Radiance',
        'INTEGRATED LW Radiance',
        'VIS Radiance',
        'INTEGRATED VIS Radiance',
        'Tot Radiance',
        'INTEGRATED TOT Radiance',
        'SW Flux',
        'INTEGRATED SW Flux',
        'NIR Flux',
        'INTEGRATED NIR Flux',
        'LW Flux',
        'INTEGRATED LW Flux',
        'VIS Flux',
        'INTEGRATED VIS Flux',
        'Tot Flux',
        'INTEGRATED TOT Flux']
    new_header = table.iloc[0]
    table = table[1:]
    table.columns = column_names
    table.reset_index(drop=True, inplace=True)
    if isinstance(table, np.ndarray) and table.ndim == 3:
        # .reshape(560, 25) or .squeeze() removes the middle "1"
        table = table.reshape(table.shape[0], table.shape[2])
        # If table is a LIST of lists of lists:
    elif isinstance(table, list) and len(np.array(table).shape) == 3:
        table = [row[0] for row in table]
    LOCAL_DATA_PATH = resources.files("modtran_analysis") / "data"
    DATA_FILE_PATH = LOCAL_DATA_PATH / filename
    ds = xr.open_dataset(DATA_FILE_PATH)
    scene_data = LOCAL_DATA_PATH / 'fv3_subset_for_ceres-trmm_erbe_scenes.txt'
    scene_data = pd.read_csv(scene_data, sep=',')
    filename_index = int(str(filename)[28:-3]) #based off the naming convention of "v5/FV3_Modtran6_IO_v5_scene_1.nc"
    # scene 1 (data name) = row 1 of the scene data file *supposedly*, we are checking that here
    # table = pd.DataFrame(table)
    # print(table.columns)
    # surface_type = table['IGBP Scene']
    ADM_type = table['ADM-Type']
    max_index = table['Tot Radiance'].idxmax()
    table['SZA'] = pd.to_numeric(table['SZA'], errors='coerce')

    highest_sun_idx = table['SZA'].idxmin()

    highest_sun_row = table.loc[highest_sun_idx]


    # Need to calculate the cloud cover of the file
    import libera_utils.scene_id as scene_id
    from libera_utils.config import config
    from libera_utils.scene_definitions import SceneDefinition
    import pathlib
    scene_defs = [SceneDefinition(pathlib.Path(config.get("ERBE_SCENE_DEFINITION")))]

    df = xr.Dataset({
    "igbp_surface_type":    int(ds['IGBP_Type_FV3'].data),
    "clear_area": (1-scene_data[' cldc'][filename_index])*100})

    footprint_data = scene_id.FootprintData(df)
    footprint_data.identify_scenes(scene_definitions=scene_defs)


    table['Tot Radiance'] = pd.to_numeric(table['Tot Radiance'], errors='coerce')
    table['Tot Flux'] = pd.to_numeric(table['Tot Flux'], errors='coerce')
    table['INTEGRATED TOT Radiance'] = pd.to_numeric(table['INTEGRATED TOT Radiance'], errors='coerce')
    table['INTEGRATED TOT Flux'] = pd.to_numeric(table['INTEGRATED TOT Flux'], errors='coerce')
    # 2. Find the index (the "where")
    max_rad_idx = table['Tot Radiance'].idxmax()
    max_flux_idx = table['Tot Flux'].idxmax()
    max_int_rad_idx = table['INTEGRATED TOT Radiance'].idxmax()
    max_int_flux_idx = table['INTEGRATED TOT Flux'].idxmax()

    min_rad_idx = table['Tot Radiance'].idxmin()
    min_flux_idx = table['Tot Flux'].idxmin()
    min_int_rad_idx = table['INTEGRATED TOT Radiance'].idxmin()
    min_int_flux_idx = table['INTEGRATED TOT Flux'].idxmin()


    # 3. Extract the full row data
    max_rad_row = table.loc[max_rad_idx]
    max_flux_row = table.loc[max_flux_idx]
    max_int_rad_row = table.loc[max_int_rad_idx]
    max_int_flux_row = table.loc[max_int_flux_idx]

    min_rad_row = table.loc[min_rad_idx]
    min_flux_row = table.loc[min_flux_idx]
    min_int_rad_row = table.loc[min_int_rad_idx]
    min_int_flux_row = table.loc[min_int_flux_idx]

    # 4. Print the specific details
    import os
    output_dir = "data/v5-summaries"
    os.makedirs(output_dir, exist_ok=True)
    clean_name = filename.split('/')[-1]
    output_path = os.path.join(output_dir, f"data-summary-{clean_name}")
    with open(output_path, "w") as f:
        f.write(f'''----------DATA SUMMARY OF FILE {filename}---------
ADM Type = {ADM_type[0]}

latitude/longitude of file = {ds['FV3_lat'].values} {ds['FV3_lat'].units}, {ds['FV3_lon'].values} {ds['FV3_lon'].units}
compared lat/lon = {scene_data[' lat(deg)'][filename_index-1]} Degrees, {scene_data[' lon(deg)'][filename_index-1]} Degrees

IGBP Surface Type = {int(ds['IGBP_Type_FV3'].values)}
Cloud Fraction = {float(footprint_data._data['cloud_fraction'])} (from text file)
ERBE ID = {float(footprint_data._data['scene_id_erbe'])}
Libera Utils Surface Type = {float(footprint_data._data['surface_type'])}


---Radiance---
Max Radiance =  {max_rad_row['Tot Radiance']} at VZA={max_rad_row['VZA']}, RAA={max_rad_row['RAA']}, SZA={max_rad_row['SZA']}
Max Integrated Radiance = {max_int_rad_row['INTEGRATED TOT Radiance']} at VZA={max_int_rad_row['VZA']}, RAA={max_int_rad_row['RAA']}, SZA={max_int_rad_row['SZA']}

Min Radiance =  {min_rad_row['Tot Radiance']} at VZA={min_rad_row['VZA']}, RAA={min_rad_row['RAA']}, SZA={min_rad_row['SZA']}
Min Integrated Radiance =  {min_int_rad_row['INTEGRATED TOT Radiance']} at VZA={min_int_rad_row['VZA']}, RAA={min_int_rad_row['RAA']}, SZA={min_int_rad_row['SZA']}


---Flux---
Max Flux = {max_flux_row['Tot Flux']} at VZA={max_flux_row['VZA']},RAA={max_flux_row['RAA']}, SZA={max_flux_row['SZA']}
Max Integrated Flux = {max_int_flux_row['INTEGRATED TOT Flux']} at VZA={max_int_flux_row['VZA']},RAA={max_int_flux_row['RAA']}, SZA={max_int_flux_row['SZA']}

Min Flux = {min_flux_row['Tot Flux']} at VZA={min_flux_row['VZA']},RAA={min_flux_row['RAA']}, SZA={min_flux_row['SZA']}
Min Integrated Flux = {min_int_flux_row['INTEGRATED TOT Flux']} at VZA={min_int_flux_row['VZA']},RAA={min_int_flux_row['RAA']}, SZA={min_int_flux_row['SZA']}

The sun is highest at Index: {highest_sun_idx} (Least amount of scattering)
Minimum SZA: {highest_sun_row['SZA']} degrees
Corresponding Tot Radiance: {highest_sun_row['Tot Radiance']}
Corresponding Tot Flux: {highest_sun_row['Tot Flux']}
''')




