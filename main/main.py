import numpy as np
from base import compute, plotter

import warnings
warnings.filterwarnings('ignore')

"""
    0th item of nash list is optimal screening probability
    1th item of nash list is optimal (strategic) good submission probability
    2th item of nash list is optimal bad submission probability
"""

model = compute.Compute()
plotter = plotter.Plotter()


def calculate(param, range_):
    nash_list = []
    baseline = {}
    param_range = np.linspace(range_[0], range_[1], model.var_dict.get('step'))

    for elem in param_range:
        baseline[param] = elem
        nash_list.append(model.nash(baseline, is_profiling=False))

    plotter.plot_nash(param_range, range_, param, nash_list)


calculate('initial_wealth', [1, 3])
calculate('risk_preference', [1, 3])
calculate('strategic_good', [0, 1])

