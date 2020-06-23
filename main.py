from environment import Env
from agent import Agent

class Main:
    def __init__(self):
        self.env = Env()
        self.agent = Agent(self.env)

    def policy_evaluation(self):
        delta = 0
        while True:
            for state in self.env.states.keys():
                v = self.env.states[state]
                

if __name__ == '__main__':
    main = Main()
    main.policy_evaluation()