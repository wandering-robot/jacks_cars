import math as m
from random import choices

class Lot:
    lot_num = 0
    max_car = 20

    def __init__(self,av_in,av_out):
        self.name = Lot.lot_num     #to autoname the lots
        Lot.lot_num += 1

        self.av_in = av_in
        self.av_out = av_out

        self.probs_in = self.poisson_probs(av_in)   
        self.probs_out = self.poisson_probs(av_out)

        self.cars = 0

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

if __name__ == "__main__":
    lot1 = Lot(3,3)
    print(lot1.probs_in)
    print(lot1.out_demand())



