import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import math
from importlib import resources

def plot_viewing_geometry(geometry_data: xr.DataArray, geometry_type: str, bins_visible: str, data_version: str):
    '''
    Creating a plot of the different windows of viewing for the MODTRAN6 data

    Using the different perspectives of viewing geometry (Relative Azimuth Angle, Viewing Zenith Angle,
    and Solar Zenith Angle), you can compare what viewing angles are in specific bins of that data.
    The unfiltered bins are regression coefficients for angular bin definition.

    Parameters
    -----------
    geometry_data: xr.DataArray
        this is the Xarray DataArray of the actual geometry data

    geometry_type: str
        this is a string that can be "RAA", "VZA", or "SZA". These are used to define the plot titles
        based on which geometry is in use.

    bins_visible: str
        this is also a string that can be: None, "Unfiltering", "ERBE", or "TRMM". This defines what
        bins will appear in the plot.

    data_version: str
        String stating which MODTRAN6 data version you are using, for view on the graphs.

    Returns
    ______
    Returns a plot of the different windows of viewing for the MODTRAN6 data for Unfiltering, ERBE, or CERES-TRMM data.

    '''

    bins_visible_values = {"None":[np.zeros(len(geometry_data))],
                    "Unfiltering": {"RAA":[15,60,120,165,180], "SZA":[22.2,41.4,60,75.5,85], "VZA":[15,30,45,60,90]},
                    "ERBE":{"RAA":[0,9,30,60,90,120,150,171,180],"SZA":[0,25.84,36.87,45.57,53.13,60.00,66.42,72.54,78.46,84.26,90.00],
                            "VZA":[0,15,27,39,51,63,75,90]},
                    "TRMM":{"RAA":[0,10,30,50,70,90,110,130,150,170,180], "SZA":[0,10,20,30,40,50,60,70,80,90],
                            "VZA":[0,10,20,30,40,50,60,70,80,90]}}
    # ERBE data from
    # https://doi.org/10.3390/rs14040887

    # TRMM data from
    # https://ceres.larc.nasa.gov/documents/STM/2001-01/pdf/Loeb_Angular_Distrib.pdf


    plt.scatter(np.arange(0,len(geometry_data)),geometry_data, marker='o', s=100)
    plt.xlabel('Index')
    plt.ylabel(f'{geometry_type} \n [degrees]')
    plt.title(f'{geometry_type} with {bins_visible} bins')
    ticker.AutoLocator()
    plt.ylim(0, math.ceil(np.max(geometry_data)/10)*10)
    plt.xlim(-1, len(geometry_data))
    x= (len(geometry_data)/2)
    y= (math.ceil(np.max(geometry_data)/10)*10)*.95
    plt.text(x, y, f'Data Version: {data_version}', ha='center', fontsize=12, color='gray')
    match bins_visible:
        case "Unfiltering" | "ERBE" | "TRMM":
            for i in range(len(bins_visible_values[bins_visible][geometry_type])):
                plt.axhline(bins_visible_values[bins_visible][geometry_type][i], linestyle='--', linewidth=1)


from modtran_analysis.tools import utils

def plot_single_spectrum(wavelength_data: xr.DataArray, spectrum_data: xr.DataArray = None, title: str = None,
                         RAA: str = None, SZA: str = None, VZA: str = None, scene: str = None, data_version: str = None,
                         label: str = None, print_max_radiance=True):
    '''
    Creates a plot of the spectral radiance data over the wavelength range

    Providing the wavelength, you are able to add the spectral data for different viewing geometries of the
    MODTRAN data. You are also given the option of adding a plot title, and the values for the different viewing
    geometries.

    Parameters
    ----------

    wavelength_data: xr.DataArray
        this is the Xarray DataArray of the actual wavelength data that we are integrating values over

    spectrum_data: xr.DataArray
        This is the Xarray DataArray of the actual spectral radiance data we are observing from various
        viewing geometries
        This is expected in the units of [micro-W SR-1 CM-2 / NM]
            Example- spectrum_data=spectrum_data[VZA_angle][SZA_angle][RAA_angle][:]

    title: str
        this is the title of the plot you wish to display

    RAA: str
        this is the RAA value that we are plotting in spectrum_data. This will be displayed as a
        text box on the plot

    SZA: str
        this is the SZA value that we are plotting in spectrum_data. This will be displayed as a
        text box on the plot

    VZA: str
        this is the VZA value that we are plotting in spectrum_data. This will be displayed as a
        text box on the plot

    scene: str
        this is the IGBP scene that we are plotting in spectrum_data. This will be displayed as a
        text box on the plot

    data_version: str
        this is the data version that we are plotting. This will be displayed as a text box on the plot

    label: str
        optional label for the plot

    print_max_radiance: bool
        This tool only comes in handy for when plotting individual spectral radiance data (one viewing geometry).
        If you are plotting more than one, make sure to turn off this feature.


    Returns
    -------

    A spectral plot for a given viewing geometries for MODTRAN data
    '''
    spectrum_data= utils.unit_conversion(spectrum_data)
    plt.plot(wavelength_data, spectrum_data, label=label)
    plt.ylabel('Spectrally-Resolved TOA Radiance \n[$Watts/steradians/m^2/nm$]', fontsize=10)
    plt.xlabel('Wavelength (nm)', fontsize=10)
    plt.title(title, fontsize=10)
    plt.text(.8, .8, f"Version = {data_version}", transform=plt.gca().transAxes,
             ha='left', va='top', fontsize=10)
    if RAA is not None:
        plt.text(.8, .95 , f"RAA = {RAA} $\degree$", transform=plt.gca().transAxes,
            ha= 'left', va= 'top', fontsize=10)
    if SZA is not None:
        plt.text(.8, .9 , f"SZA = {SZA} $\degree$", transform=plt.gca().transAxes,
            ha= 'left', va= 'top', fontsize=10)
    if VZA is not None:
        plt.text(.8, .85 , f"VZA = {VZA} $\degree$", transform=plt.gca().transAxes,
            ha= 'left', va= 'top', fontsize=10)
    #TODO I am not the most content with what this is doing so I need to think about a way to make it nicer
    if print_max_radiance:
        plt.text(.5, .95 , f"Max Radiance = {spectrum_data.max(): .2e} \n[$Watts/steradians/m^2/nm$]", transform=plt.gca().transAxes,
            ha= 'center', va= 'top', fontsize=10, bbox=dict(facecolor='white', alpha=0.6))
    plt.text(.5, .80, f"IGBP Land Type = {scene}", transform=plt.gca().transAxes,ha= 'center',
             va= 'top', fontsize=10, bbox=dict(facecolor='white', alpha=0.6))
