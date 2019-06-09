import numpy as np
import matplotlib.pyplot as plt
from base import compute, plotter

model = compute.Compute()
plotter = plotter.Plotter()
policies = [False, True]  # False: non-profiling True: profiling


def calculate_POR(uncertain_dict):

    range_ = np.linspace(0, 1, model.var_dict.get('step'))
    scale = 2
    f = plt.figure(figsize=(9, 5))
    plt_number = 1
    color_list = ['dodgerblue', 'red', 'orange']

    for policy in policies:

        for parameter, values in uncertain_dict.items():

            nominal = model.var_dict.get(parameter)
            plt.subplot(2, len(uncertain_dict), plt_number)
            title = str(parameter) + ': base = ' + str(nominal)
            line_dots = ['-', '--', '-.']
            line_number = 0

            for val in values:
                robust_nash = []
                for budget in range_:
                    uncertain_dict_ = {parameter: [nominal*val, nominal*(scale-val)]}
                    robust_nash.append(model.robust_nash(uncertain_dict=uncertain_dict_,
                                                         budget_of_uncertainty=budget, is_profiling=policy))
                plt.plot(range_, [item[3] for item in robust_nash],
                         c=color_list[line_number], linestyle=line_dots[line_number],
                         label=[nominal*val, nominal*(scale-val)])
                plt.title(title, fontsize=11)
                plt.xlabel(r'Budget of Uncertainty $\Gamma$')
                plt.ylabel('Price of Robustness')
                # plt.ylim([0, 80])
                plt.legend(frameon=False, prop={'size': 9})
                line_number += 1

            plt_number += 1

    plt.tight_layout()
    plt.show()


calculate_POR({'reward_good': [0.05, 0.5, 0.75], 'cost_good': [0, 0.5, 0.75], 'strategic_good': [0.72, 0.800, 0.96]})
# calculate_POR({'reward_bad': [0, 0.5, 0.75], 'cost_bad': [0, 0.5, 0.75], 'risk_preference': [0.05, 0.5, 0.75]})


def calculate_measures(uncertain_dict):

    range_ = np.linspace(0, 1, model.var_dict.get('step'))
    f = plt.figure(figsize=(10, 5))
    plt_number = 1

    ### non-pofiling ###
    util_list = [r'$\Phi$', r'$p_g$', r'$p_b$']
    line_dots = ['-', '--', '-.']
    colors = ['dodgerblue', 'orange', 'magenta']

    for parameter, values in uncertain_dict.items():

        plt.subplot(2, len(uncertain_dict), plt_number)
        nominal = model.var_dict.get(parameter)
        title = str(parameter) + ': base = ' + str(nominal)
        line_number = 0

        for i in range(3):
            robust_nash = []
            for budget in range_:
                solution = model.robust_nash(uncertain_dict={parameter: values},
                                             budget_of_uncertainty=budget, is_profiling=False)
                robust_nash.append(solution)
            plt.plot(range_, [item[i][0] for item in robust_nash],
                     c=colors[line_number], linestyle=line_dots[line_number], linewidth=2)
            plt.title(title)
            plt.xlabel(r'Budget of Uncertainty $\Gamma$')
            plt.ylabel('Scr./Subm. Probability')
            plt.ylim([-0.02, 1.02])
            line_number += 1

        fig_num = '(a' + str(plt_number) + ") non-profiling"
        plt.text(0, 0.4, fig_num, fontweight="bold")
        plt_number += 1

    plt.legend(util_list, frameon=False, prop={'size': 14}, loc='upper left', bbox_to_anchor=(1, 1))

    ### profiling ###
    util_list = [r'$\Phi_1$', r'$\Phi_2$', r'$p_{g1}$', r'$p_{g2}$', r'$p_{b1}$', r'$p_{b2}$']
    lines = ['-', '-', '--', '--', '-.', '-.']
    colors = ['dodgerblue', 'red', 'orange', 'green', 'magenta', 'brown']

    for parameter, values in uncertain_dict.items():

        plt.subplot(2, len(uncertain_dict), plt_number)
        nominal = model.var_dict.get(parameter)
        title = str(parameter) + ': base = ' + str(nominal)
        line_number = 0

        for i in range(3):
            robust_nash = []
            for budget in range_:
                solution = model.robust_nash(uncertain_dict={parameter: values},
                                             budget_of_uncertainty=budget, is_profiling=True)
                robust_nash.append(solution)
            plt.plot(range_, [item[i][0] for item in robust_nash],
                     c=colors[line_number], linestyle=lines[line_number], linewidth=2)
            line_number += 1
            plt.plot(range_, [item[i][1] for item in robust_nash],
                     c=colors[line_number], linestyle=lines[line_number], linewidth=2)
            plt.title(title)
            plt.xlabel(r'Budget of Uncertainty $\Gamma$')
            plt.ylabel('Scr./Subm. Probability')
            plt.ylim([-0.02, 1.02])
            line_number += 1

        fig_num = '(b' + str(plt_number-3) + ") profiling"
        plt.text(0, 0.15, fig_num, fontweight="bold")
        plt_number += 1

    plt.legend(util_list, frameon=False, prop={'size': 12}, loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()


# calculate_measures({'reward_bad': [0, 4], 'cost_bad': [0, 2], 'risk_preference': [0.05, 1.95]})

