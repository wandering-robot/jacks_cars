
class Agent:
    def __init__(self,env):
        self.env = env
        self.policy = {(i,j):0 for i in range(self.env.lots[0].max_car + 1) for j in range(self.env.lots[1].max_car + 1)}

        self.cost2move = 2

        self.profit = 0

    def move_cars(self):
        
        self.env.lots[0].cars -= n
        self.env.lots[0].cars += n

        self.profit -= n*self.cost2move


