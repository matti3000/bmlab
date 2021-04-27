import logging
import numpy as np


logger = logging.getLogger(__name__)


class EvaluationModel(object):

    def __init__(self):

        self.nr_brillouin_peaks = 1

        self.results = {
            # Fitted values
            'brillouin_peak_position': [],   # [pix] Brillouin peak position
            'brillouin_peak_fwhm': [],       # [pix] Brillouin peak FWHM
            'brillouin_peak_intensity': [],  # [a.u.] Brillouin peak intensity

            'rayleigh_peak_position': [],   # [pix] Rayleigh peak position
            'rayleigh_peak_fwhm': [],       # [pix] Rayleigh peak FWHM
            'rayleigh_peak_intensity': [],  # [a.u.] Rayleigh peak intensity

            'intensity': [],                # [a.u.] Overall intensity of image
            'time': [],                     # [s] The time the measurement
                                            #     point was taken at

            # Derived values
            'brillouin_shift': [],          # [pix] Brillouin frequency shift
            'brillouin_shift_f': [],        # [GHz] Brillouin frequency shift
            'brillouin_peak_fwhm_f': [],    # [GHz] Brillouin peak FWHM
        }

        self.parameters = {
            'brillouin_shift_p': {      # Brillouin frequency shift
                'unit', 'pix',
                'symbol', r'$\nu_\mathrm{B}$',
                'label', 'Brillouin frequency shift'
            },
            'brillouin_shift_f': {      # Brillouin frequency shift
                'unit', 'GHz',
                'symbol', r'$\nu_\mathrm{B}$',
                'label', 'Brillouin frequency shift'
            },
            'brillouin_fwhm_p': {       # Brillouin peak width
                'unit', 'pix',
                'symbol', r'$\Delta_\mathrm{B}$',
                'label', 'Brillouin peak width'
            },
            'brillouin_fwhm_f': {       # Brillouin peak width
                'unit', 'GHz',
                'symbol', r'$\Delta_\mathrm{B}$',
                'label', 'Brillouin peak width'
            }
        }

    def get_parameters(self):
        return self.parameters

    def initialize_results_arrays(self, dims):
        shape_general = (
            dims['dim_x'],
            dims['dim_y'],
            dims['dim_z'],
            dims['nr_images'],
        )

        self.results['intensity'] = np.empty(shape_general)
        self.results['intensity'][:] = np.nan

        self.results['time'] = np.empty(shape_general)
        self.results['time'][:] = np.nan

        shape_brillouin = (
            dims['dim_x'],
            dims['dim_y'],
            dims['dim_z'],
            dims['nr_images'],
            dims['nr_brillouin_regions'],
            dims['nr_brillouin_peaks'],
        )

        self.results['brillouin_peak_position'] = np.empty(shape_brillouin)
        self.results['brillouin_peak_position'][:] = np.nan

        self.results['brillouin_peak_fwhm'] = np.empty(shape_brillouin)
        self.results['brillouin_peak_fwhm'][:] = np.nan

        self.results['brillouin_peak_intensity'] = np.empty(shape_brillouin)
        self.results['brillouin_peak_intensity'][:] = np.nan

        self.results['brillouin_shift'] = np.empty(shape_brillouin)
        self.results['brillouin_shift'][:] = np.nan

        self.results['brillouin_shift_f'] = np.empty(shape_brillouin)
        self.results['brillouin_shift_f'][:] = np.nan

        self.results['brillouin_peak_fwhm_f'] = np.empty(shape_brillouin)
        self.results['brillouin_peak_fwhm_f'][:] = np.nan

        shape_rayleigh = (
            dims['dim_x'],
            dims['dim_y'],
            dims['dim_z'],
            dims['nr_images'],
            dims['nr_rayleigh_regions'],
        )

        self.results['rayleigh_peak_position'] = np.empty(shape_rayleigh)
        self.results['rayleigh_peak_position'][:] = np.nan

        self.results['rayleigh_peak_fwhm'] = np.empty(shape_rayleigh)
        self.results['rayleigh_peak_fwhm'][:] = np.nan

        self.results['rayleigh_peak_intensity'] = np.empty(shape_rayleigh)
        self.results['rayleigh_peak_intensity'][:] = np.nan
