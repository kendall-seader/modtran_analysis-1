import pytest
from modtran_analysis.tools import utils
import xarray as xr
import xarray.testing as xrt
import numpy as np



def test_radiance_valid_float():
    assert utils.unit_conversion(5000.0) == 50.0

def test_radiance_valid_array():
    result = utils.unit_conversion(xr.DataArray([5, 500, 5000]))
    expected = xr.DataArray([0.05, 5.0, 50.0])
    xrt.assert_allclose(result, expected)


@pytest.mark.parametrize(("bad_input", "expected_exception"), [
    ('string', TypeError)])
def test_radiance_invalid(bad_input, expected_exception):
    with pytest.raises(expected_exception):
        utils.unit_conversion(bad_input)


def test_sw_lw_spectra_combination():
    sw_data = xr.DataArray(np.array([[[[1, 2, 3]]]]))
    lw_data = xr.DataArray(np.array([[[[4, 5]]]]))

    combined = utils.sw_lw_spectra(sw_data, lw_data, RAA_bin=0, VZA_bin=0, SZA_bin=0)
    assert isinstance(combined, xr.DataArray)
    assert combined.shape[0] == 5
    np.testing.assert_array_equal(combined.values, np.array([1, 2, 3, 4, 5]))


def test_sw_lw_spectra_empty_arrays():
    sw_data = xr.DataArray(np.zeros((1,1,1,0)))
    lw_data = xr.DataArray(np.zeros((1,1,1,0)))

    combined = utils.sw_lw_spectra(sw_data, lw_data, RAA_bin=0, VZA_bin=0, SZA_bin=0)
    assert combined.shape[0] == 0
    assert isinstance(combined, xr.DataArray)


def test_sw_lw_wavelength_combination():
    sw_wavelength = xr.DataArray(np.array([400, 500, 600]))
    lw_wavelength = xr.DataArray(np.array([700, 800]))

    combined = utils.sw_lw_wavelength(sw_wavelength, lw_wavelength)
    assert isinstance(combined, xr.DataArray)
    assert combined.shape[0] == 5
    np.testing.assert_array_equal(combined.values, np.array([400, 500, 600, 700, 800]))


def test_sw_lw_wavelength_empty_arrays():
    sw_wavelength = xr.DataArray(np.array([]))
    lw_wavelength = xr.DataArray(np.array([]))

    combined = utils.sw_lw_wavelength(sw_wavelength, lw_wavelength)
    assert isinstance(combined, xr.DataArray)
    assert combined.shape[0] == 0

def test_unit_conversion_float_microwatts():
    # testing units of [microwatts/steradian/cm^2/nm] converted
    radiance = 1.0
    result = utils.unit_conversion(radiance, use_microwatts=True)

    expected = 1.0 * 1e-6 * 10000
    assert result == pytest.approx(expected)

def test_unit_conversion_dataarray_microwatts():
    # testing units of [microwatts/steradian/cm^2/nm] converted AS AN ARRAY
    radiance = xr.DataArray(
        np.array([1.0, 2.0, 3.0]),
        dims=["wavelength"],
        coords={"wavelength": [400, 500, 600]},
    )

    result = utils.unit_conversion(radiance, use_microwatts=True)

    expected = radiance * 1e-6 * 10000
    xr.testing.assert_allclose(result, expected)

def test_unit_conversion_float_watts():
    # testing units of [watts/steradian/cm^2/nm]
    radiance = 1.0
    result = utils.unit_conversion(radiance, use_microwatts=False)

    expected = 1.0 * 10000
    assert result == pytest.approx(expected)

def test_unit_conversion_invalid_type():
    with pytest.raises(TypeError):
        utils.unit_conversion([1, 2, 3])  # list is not allowed

#todo WRITE THE TEST FOR THE INTEGRATION FUNCTION