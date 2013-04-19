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
from qiime.stats import quantile
from SCGM.profile import compare_profiles

def bootstrap_profiles(profiles, alpha=0.05, repetitions=1000,
    randfunc=randint):
    """Performs bootstrapping over the sample 'profiles'

    Inputs:
        profiles: list of profiles
        alpha: defines the confidence interval as 1 - alpha
        repetitions: number of bootstrap iterations
        randfunc: random function for generate the bootstrap samples

    Returns:
        profile: the bootstrapped profile of the profiles list
        sample_mean: the bootstrap mean of the amount shared
        sample_stdev: the bootstrap standard deviation of the amount shared
        ci: the confidence interval for the bootstrap mean
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
    sample_stdev = std(boot_shared)
    # Compute the confidence interval for the bootstrapped data
    # using bootstrap percentile interval
    ci = quantile(boot_shared, [alpha/2, 1-(alpha/2)])
    # Compute the bootstrapped profile of the profiles list
    boot_profile = {}
    for key in profiles[0]:
        # Get an array with the data for this taxonomy
        tax_data = [prof[key] for prof in boot_profiles]
        # Get the mean
        tax_mean = mean(tax_data)
        # Get the standard deviation
        tax_stdev = std(tax_mean)
        # Get the confidence intervals
        tax_ci = quantile(tax_data, [alpha/2, 1-(alpha/2)])
        # Store the values in the bootstrapped profile
        boot_profile[key] = (tax_mean, tax_stdev, tax_ci[0], tax_ci[1])

    return boot_profile, sample_mean, sample_stdev, ci