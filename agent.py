
class Agent:
    def __init__(self,env):
        self.env = env

        self.posible_moves = [i for i in range(-5,6)]

        self.cost2move = 2

        self.profit = 0

    def move_cars(self):
        
        self.env.lot1.cars -= n
        self.env.lot2.cars += n

        self.profit -= n*self.cost2move


