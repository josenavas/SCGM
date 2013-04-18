#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from numpy import array, mean, std
from numpy.random import randint
from scipy.stats import t
from math import pi as PI
from math import sqrt
from SCGM.profile import compare_profiles

def bootstrap_profiles(profiles, alpha=0.05, repetitions=1000,
    randfunc=randint):
    """Performs bootstrapping over the sample 'profiles'

    Inputs:
        profiles: list of profiles
        alpha: defines the confidence interval as 1 - alpha
        repetitions: number of bootstrap iterations
        randfunc: random function for generate the bootstrap samples
    """

    length = len(profiles)
    boot_shared = []
    boot_profiles = []
    for i in range(repetitions):
        # Construct the bootstrap sample
        resample = [profiles[randfunc(0, length)] for j in range(length)]
        profile = compare_profiles(resample)
        # Store the amount shared
        boot_shared.append(1.0 - profile['not_shared'])
        # Store the result profile
        boot_profiles.append(profile)
    # Convert data to a numpy array
    boot_shared = array(boot_shared)
    # Get the mean and the standard deviation of the shared data
    sample_mean = mean(boot_shared)
    sample_std_dev = std(boot_shared)
    # Compute the confidence interval for the sample mean
    # Given that the resamples are i.i.d, we can use the 
    # Central Limit Theorem to compute the confidence interval
    t_a = t.pdf(alpha/2, length-1)
    delta = t_a * sample_std_dev / sqrt(length)
    print sample_mean-delta, sample_mean+delta
    profile = compare_profiles(profiles)
    print 1.0 - profile['not_shared']