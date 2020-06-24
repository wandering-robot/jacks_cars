from environment import Env
from agent import Agent

class Main:
    def __init__(self):
        self.env = Env()
        self.agent = Agent(self.env)

        self.discount = 0.9
        self.epsilon = 0.01

    def policy_evaluation(self):
        i = 0
        while True:
            delta = 0
            for state in self.env.states.values():
                v = state.value
                v_s = 0
                for new_state, prob in state.next_states.items():
                    v_s += prob*(state.next_state_rewards[new_state] + self.discount*new_state.value)
                state.value = v_s
                delta = max(delta, abs(v_s - v))
            if delta < self.epsilon:
                break
            else:
                i += 1
        return i

    def policy_improvement(self):
        i = 0
        while True:
            stable = True
            for state in self.env.states.values():
                close = False
                pi = state.policy
                action = 0
                value = 0
                for n in self.agent.posible_moves:
                    try:
                        new_state = self.env.states[state.move_cars(n)]
                    except:
                        continue        #index not in bounds therefore illegal move
                    v_s = 0
                    for new_new_state, prob in new_state.next_states.items():
                        v_s += prob*(new_new_state.next_state_rewards[new_new_state] - abs(n)*self.agent.cost2move + self.discount*new_new_state.value)
                    if abs(v_s - value) < 0.01:
                        close = True
                    if v_s >= value:
                        value = v_s
                        action = n
                if action != pi and not close:
                    stable = False
                state.policy = action
            if stable:
                break
            i += 1
            if i % 20 == 0:
                print(i)

                

if __name__ == '__main__':
    main = Main()
    while True:
        i = main.policy_evaluation()
        main.policy_improvement()
        if i < 1:
            break
    for state in main.env.states.values():
        print(f'State {state} -> Value = {state.value:.3f} Policy = {state.policy}')

    matrix = [[None for _ in range(21)] for _ in range(21)]
    for state in main.env.states.values():
        i,j = state.tup
        matrix[i][j] = state.policy
    for row in matrix:
        print(row)