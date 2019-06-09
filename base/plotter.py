import matplotlib.pyplot as plt


class Plotter:

    measure_list = ['Screening Probability', 'Good App.Sub. Probability', 'Bad App.Sub. Probability']
    util_list = ['appr. 1', 'appr. 2', 'good 1', 'good 2', 'bad 1', 'bad 2']
    color_list = ['dodgerblue', 'red', 'orange', 'green', 'magenta', 'brown']
    # color_list = ['dodgerblue', 'red']

    def plot_nash(self, x, range_, label, nash):
        plt.figure(figsize=(12, 3))
        for i in range(3):
            plt.subplot(1, 4, i+1)
            plt.plot(x, [item[i][0] for item in nash], c='b', marker='v', label='app type I')
            plt.plot(x, [item[i][1] for item in nash], c='r', marker='*', label='app type II')
            plt.title(self.measure_list[i])
            plt.xlabel(label)
            plt.xlim(range_)
            plt.ylim([0, 1])
            plt.legend()

        plt.subplot(1, 4, 4)
        plt.plot(x, [item[3] for item in nash], c='m', marker='+')
        plt.title('Approver\'s Utility')
        plt.xlabel(label)
        plt.xlim(range_)

        plt.tight_layout()
        plt.show()

