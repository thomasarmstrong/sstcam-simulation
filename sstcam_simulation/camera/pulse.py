from .constants import CONTINUOUS_SAMPLE_WIDTH
from abc import ABCMeta, abstractmethod
import numpy as np
from scipy.stats import norm

__all__ = [
    "ReferencePulse",
    "GenericPulse",
    "GaussianPulse",
]


class ReferencePulse(metaclass=ABCMeta):
    def __init__(self, length):
        """
        Base for classes which define a reference pulse shape

        The pulse is evaluated on initialisation.
        For a new pulse to be defined, a new class should be initialised.

        Parameters
        ----------
        length : int
            Length of the reference pulse in nanoseconds
        """
        self.time = np.arange(0, length, CONTINUOUS_SAMPLE_WIDTH)
        pulse = self._function(self.time)
        self.y_scale = pulse.sum() * CONTINUOUS_SAMPLE_WIDTH
        self.pulse = pulse / self.y_scale

    @abstractmethod
    def _function(self, time):
        """
        Function that describes the reference pulse shape.

        Parameters
        ----------
        time : ndarray
            Time in ns to evaluate the pulse at

        Returns
        -------
        reference_pulse : ndarray
            Y values of reference pulse at the requested times  (not-normalised)
        """


class GenericPulse(ReferencePulse):
    def __init__(self, time, value):
        """
        Reference pulse defined in an array, sampled at a sub-ns level
        (the finer the sampling the better).

        Evaluation of this reference pulse is performed with a linear interpolation.

        Parameters
        ----------
        time : ndarray
            Time (ns) axis for the reference pulse
        value : ndarray
            Values of the reference pulse corresponding to the time array
        """
        self.interp_time = time
        self.interp_value = value
        length = np.round(time[-1])
        super().__init__(length=length)

    def _function(self, time):
        return np.interp(time, xp=self.interp_time, fp=self.interp_value)


class GaussianPulse(ReferencePulse):
    def __init__(self, mean=30, sigma=6, length=60):
        """
        Simple gaussian reference pulse

        Parameters
        ----------
        mean : u.Quantity[time]
            Time (ns) corresponding to centre of pulse
        sigma : u.Quantity[time]
            Standard deviation of pulse (ns)
        length : int
            Length of the reference pulse in nanoseconds
        """
        self.mean = mean
        self.sigma = sigma
        super().__init__(length)

    def _function(self, time):
        return norm.pdf(time, loc=self.mean, scale=self.sigma)
