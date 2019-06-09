import numpy as np
import matplotlib.pyplot as plt
from base import compute, plotter

model = compute.Compute()
plotter = plotter.Plotter()


def plot(uncertain_dict):

    range_ = np.linspace(0, 1, model.var_dict.get('step'))
    scale = 2
    f = plt.figure(figsize=(10, 3))
    plt_number = 1

    for parameter, values in uncertain_dict.items():

        nominal = model.var_dict.get(parameter)
        plt.subplot(1, len(uncertain_dict), plt_number)
        title = str(parameter) + ': baseline = ' + str(nominal)
        line_dots = ['-', '-.']
        color_list = ['dodgerblue', 'orange']
        line_number = 0

        for val in values:
            robust_nash_nonprof = []
            robust_nash_prof = []
            for budget in range_:
                uncertain_dict_ = {parameter: [nominal*val, nominal*(scale-val)]}
                robust_nash_nonprof.append(
                    model.robust_nash(uncertain_dict=uncertain_dict_, budget_of_uncertainty=budget, is_profiling=False))
                robust_nash_prof.append(
                    model.robust_nash(uncertain_dict=uncertain_dict_, budget_of_uncertainty=budget, is_profiling=True))
            plt.plot(range_, [item[3] for item in robust_nash_nonprof], c=color_list[line_number],
                     linestyle=line_dots[line_number],
                     label=[nominal*val, nominal*(scale-val)])
            plt.plot(range_, [item[3] for item in robust_nash_prof], c=color_list[line_number],
                     linestyle=line_dots[line_number],
                     label=[nominal * val, nominal * (scale - val)])
            plt.title(title)
            plt.xlabel(r'Budget of Uncertainty $\Gamma$')
            plt.ylabel('Price of Robustness')
            plt.ylim([0, 40])
            # plt.legend(frameon=False, prop={'size': 10})
            line_number += 1

        plt_number += 1

    plt.tight_layout()
    plt.show()
    f.savefig('budget_vs_price.pdf')


plot({'reward_bad': [0, 0.75], 'cost_bad': [0, 0.75], 'risk_preference': [0.05, 0.75]})
