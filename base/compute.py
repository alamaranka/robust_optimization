import numpy as np


class Compute:

    var_dict = {}

    def __init__(self):
        self.set_initials()
        print('Compute is initialized!')

    def set_initials(self):
        self.var_dict = {'R': 1, 'C': 10, 'reward_good': 1, 'cost_good': 1, 'cost_bad': 1, 'reward_bad': 2, 'alp_1': 0.6,
                         'bet_1': 0.98, 'bet_2': 0.80, 'Lambda': 75, 'service_rate': 10,
                         'initial_wealth': 1, 'risk_preference': 1, 'strategic_good': .95, 'step': 10, 'step_budget': 10}
        self.var_dict['alp_2'] = 1 - self.var_dict.get('alp_1')

    def good_arr(self):
        good_arr_1 = self.var_dict.get('alp_1') * self.var_dict.get('bet_1') * self.var_dict.get('Lambda')
        good_arr_2 = self.var_dict.get('alp_2') * self.var_dict.get('bet_2') * self.var_dict.get('Lambda')
        return [good_arr_1, good_arr_2]

    def bad_arr(self):
        bad_arr_1 = self.var_dict.get('alp_1') * (1 - self.var_dict.get('bet_1')) * self.var_dict.get('Lambda')
        bad_arr_2 = self.var_dict.get('alp_2') * (1 - self.var_dict.get('bet_2')) * self.var_dict.get('Lambda')
        return [bad_arr_1, bad_arr_2]

    def actual_good_arr(self, pg):
        s = self.var_dict.get('strategic_good')
        n = 1 - s
        actual_good_arr_1 = (pg[0] * s + n) * self.good_arr()[0]
        actual_good_arr_2 = (pg[1] * s + n) * self.good_arr()[1]
        return [actual_good_arr_1, actual_good_arr_2]

    def actual_bad_arr(self, pb):
        actual_bad_arr_1 = pb[0] * self.bad_arr()[0]
        actual_bad_arr_2 = pb[1] * self.bad_arr()[1]
        return [actual_bad_arr_1, actual_bad_arr_2]

    def congestion(self, phi, pg, pb):
        lambda_b = phi[0] * self.actual_bad_arr(pb)[0] + phi[1] * self.actual_bad_arr(pb)[1]
        lambda_g = phi[0] * self.actual_good_arr(pg)[0] + phi[1] * self.actual_good_arr(pg)[1]
        return 1 / (self.var_dict.get('service_rate') - (lambda_g + lambda_b))

    def j_approver(self, phi, pg, pb):
        actual_good_arr_1, actual_good_arr_2 = self.actual_good_arr(pg)
        actual_bad_arr_1, actual_bad_arr_2 = self.actual_bad_arr(pb)
        return self.var_dict.get('R') * (actual_good_arr_1 + actual_good_arr_2) - \
               self.var_dict.get('C') * ((1 - phi[0]) * actual_bad_arr_1 + (1 - phi[1]) * actual_bad_arr_2)

    def u_bad(self, phi, pb):
        w = self.var_dict.get('initial_wealth')
        a = self.var_dict.get('risk_preference')
        x_1 = w + self.var_dict.get('reward_bad')
        x_2 = w - self.var_dict.get('cost_bad')
        ub_1 = (1 - pb[0]) * pow(w, a) + pb[0] * ((1 - phi[0]) * pow(x_1, a) + phi[0] * pow(x_2, a))
        ub_2 = (1 - pb[1]) * pow(w, a) + pb[1] * ((1 - phi[1]) * pow(x_1, a) + phi[1] * pow(x_2, a))
        return [ub_1, ub_2]

    def u_good(self, phi, pg, pb):
        ug_1 = pg[0] * (self.var_dict.get('reward_good') - self.var_dict.get('cost_good') * phi[0] * self.congestion(phi, pg, pb))
        ug_2 = pg[1] * (self.var_dict.get('reward_good') - self.var_dict.get('cost_good') * phi[1] * self.congestion(phi, pg, pb))
        return [ug_1, ug_2]

    def bad_best_response(self, phi):
        w = self.var_dict.get('initial_wealth')
        a = self.var_dict.get('risk_preference')
        x_1 = w + self.var_dict.get('reward_bad')
        x_2 = w - self.var_dict.get('cost_bad')
        deterrence_level = (pow(x_1, a) - pow(w, a)) / (pow(x_1, a) - pow(x_2, a))

        # decision of type 1 bad applicants
        if phi[0] < deterrence_level:
            pb_best_1 = 1
        else:
            pb_best_1 = 0

        # decision of type 2 bad applicants
        if phi[1] < deterrence_level:
            pb_best_2 = 1
        else:
            pb_best_2 = 0
        return [pb_best_1, pb_best_2]

    def good_best_response(self, phi, bad_best_response):
        s = self.var_dict.get('strategic_good')
        n = 1 - s
        good_arr_1, good_arr_2 = self.good_arr()
        actual_bad_arr_1, actual_bad_arr_2 = self.actual_bad_arr(bad_best_response)

        # decision of type 1 good applicants
        if phi[0] == 0:
            pg_best_1 = 1
        else:
            bar_lambda_good_1 = self.var_dict.get('service_rate') - (phi[0] * actual_bad_arr_1 +
                                                                     phi[1] * actual_bad_arr_2 +
                                                                     phi[0] * n * good_arr_1 +
                                                                     phi[1] * n * good_arr_2) - \
                                                                     phi[0] * self.var_dict.get('cost_good') / self.var_dict.get('reward_good')
            rate = phi[0] * good_arr_1
            rate_rev = 1 / rate
            pg_best_1 = rate_rev * max(min(bar_lambda_good_1, rate), 0)

        # decision of type 2 good applicants
        if phi[1] == 0:
            pg_best_2 = 1
        else:
            bar_lambda_good_2 = self.var_dict.get('service_rate') - (phi[0] * actual_bad_arr_1 +
                                                                     phi[1] * actual_bad_arr_2 +
                                                                     phi[0] * n * good_arr_1 +
                                                                     phi[1] * n * good_arr_2) - \
                                                                     phi[1] * self.var_dict.get('cost_good') / self.var_dict.get('reward_good')
            rate = phi[1] * good_arr_2
            rate_rev = 1 / rate
            traffic = bar_lambda_good_2 - (phi[0] * pg_best_1 * good_arr_1)
            pg_best_2 = rate_rev * max(min(traffic, rate), 0)

        return [pg_best_1, pg_best_2]

    def nash(self, my_dict={}, is_profiling=True):

        for key, value in my_dict.items():
            self.var_dict[key] = value

        phi = [np.linspace(0, 1, self.var_dict.get('step')), np.linspace(0, 1, self.var_dict.get('step'))]
        optimal = -10 ** 6

        if is_profiling:
            for phi_1 in phi[0]:
                for phi_2 in phi[1]:
                    pb_best = self.bad_best_response([phi_1, phi_2])
                    pg_best = self.good_best_response([phi_1, phi_2], pb_best)
                    j = self.j_approver([phi_1, phi_2], pg_best, pb_best)

                    if j > optimal:
                        optimal = j
                        phi_star = [phi_1, phi_2]
                        pg_star = pg_best
                        pb_star = pb_best
        else:
            for phi_1, phi_2 in zip(phi[0], phi[1]):
                pb_best = self.bad_best_response([phi_1, phi_2])
                pg_best = self.good_best_response([phi_1, phi_2], pb_best)
                j = self.j_approver([phi_1, phi_2], pg_best, pb_best)

                if j > optimal:
                    optimal = j
                    phi_star = [phi_1, phi_2]
                    pg_star = pg_best
                    pb_star = pb_best

        return [phi_star, pg_star, pb_star, optimal]

    def robust_nash(self, my_dict={}, uncertain_dict={}, budget_of_uncertainty=0, is_profiling=True):

        """
            uncertain_dict is the set of uncertain parameters and bounded intervals of each.
        """

        optimal_robust = 10 ** 6
        nash_nominal = self.nash(my_dict, is_profiling)

        lower = list(uncertain_dict.values())[0][0]
        upper = list(uncertain_dict.values())[0][1]

        nominal = (lower + upper) / 2
        half_length = (upper - lower) / 2
        budget_constraint = half_length * budget_of_uncertainty
        param_range = np.linspace(nominal - budget_constraint, nominal + budget_constraint, self.var_dict.get('step_budget'))

        for param in param_range:

            parameter = list(uncertain_dict.keys())[0]
            self.var_dict[parameter] = param
            results_set = self.nash(my_dict, is_profiling)

            if results_set[3] < optimal_robust:

                optimal_robust = results_set[3]
                phi_star_robust = results_set[0]

                self.set_initials()
                pb_star_robust = self.bad_best_response(phi_star_robust)
                pg_star_robust = self.good_best_response(phi_star_robust, pb_star_robust)

                price_of_robustness = ((nash_nominal[3] - optimal_robust) / nash_nominal[3]) * 100

        self.set_initials()

        return [phi_star_robust, pg_star_robust, pb_star_robust, price_of_robustness]
