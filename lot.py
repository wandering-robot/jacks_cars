import math as m
from random import choices

class Lot:
    lot_num = 1
    max_car = 20

    car_rental_price = 10

    def __init__(self,av_in,av_out):
        self.name = Lot.lot_num     #to autoname the lots
        Lot.lot_num += 1

        self.av_in = av_in
        self.av_out = av_out

        self.probs_in = self.poisson_probs(av_in)   
        self.probs_out = self.poisson_probs(av_out)

        self.cars = 0

    def __repr__(self):
        return f'{self.av_in,self.av_out}'

    def in_demand(self):
        return choices(list(self.probs_in.keys()), list(self.probs_in.values()))[0]

    def out_demand(self):
        return choices(list(self.probs_out.keys()), list(self.probs_out.values()))[0]

    def poisson_probs(self,av): #create lists that have the index' probability of occurance given the average and a poisson distribution
        prob_dict = {}
        i = 0
        while True:
            prob_i = (av**i)*m.exp(-av)/m.factorial(i)
            prob_dict[i]=prob_i
            i += 1
            if prob_i < 0.01:
                break
        return prob_dict

class State(Lot):
    def __init__(self,tup):
        self.tup = tup
        self.lot1_cars, self.lot2_cars = self.tup
        
        self.value = 0
        self.policy = 0

        self.next_states = None
        self.next_state_rewards = {}

    def __repr__(self):
        return f'{self.tup}'

    def move_cars(self,n):
        lot1_cars, lot2_cars = self.lot1_cars - n, self.lot2_cars + n
        return (lot1_cars,lot2_cars)

if __name__ == "__main__":
    l1 = Lot(2,3)


