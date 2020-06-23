from lot import Lot

class Env:
    def __init__(self):
        self.lots = (Lot(3,3),Lot(2,4))

        self.states = {(i,j):0 for i in range(self.lots[0].max_car + 1) for j in range(self.lots[1].max_car + 1)}

        self.delta_probs = self._delta_probs()

    def next_state_probs(self,og_state=None):     #will use delta_probs to figure out the probability of entering into the new states (by the og car number changing by delta)
        if og_state == None:
            og_state = tuple((lot.cars for lot in self.lots))
        
        next_states = {}

        lot1_possible_changes = list(self.delta_probs[0].keys())
        lot2_possible_changes = list(self.delta_probs[1].keys())

        for change1 in lot1_possible_changes:
            lot1_state = og_state[0] + change1
            if lot1_state < 0:
                continue
            for change2 in lot2_possible_changes:
                lot2_state = og_state[1] + change2
                if lot2_state < 0:
                    continue
                next_states[(lot1_state,lot2_state)] = self.delta_probs[0][change1] * self.delta_probs[1][change2]
        return next_states


    def _delta_probs(self):      #returns a dictionary with values of probability of the lot's cars changing by the key. [0] is the first lot, [1] is the second
        lot_probs = [None,None]
        i = 0
        for lot in self.lots:
            delta_probs = {}
            for num_in in list(lot.probs_in.keys()):
                for num_out in list(lot.probs_out.keys()):
                    delta = num_in - num_out
                    old_prob = delta_probs.setdefault(delta)
                    if old_prob != None:
                        delta_probs[delta] += lot.probs_in[num_in]*lot.probs_out[num_out]
                    else:
                        delta_probs[delta] = lot.probs_in[num_in]*lot.probs_out[num_out]
            lot_probs[i] = delta_probs
            i += 1
        return lot_probs
    
    @staticmethod
    def dict_trimmer(dick):
        """will use to remove possibilities under a certain percentage"""
        to_remove = []
        for k,v in dick.items():
            if v < 0.001:
                to_remove.append(k)
        for k in to_remove:
            del dick[k]

if __name__ == '__main__':
    env = Env()
    delta_probs = env.delta_probs
    # for asd in delta_probs:
    #     env.dict_trimmer(asd)
    #     print(asd,'\n')
    next_state_probs = env._next_state_probs((10,10))
    print(len(next_state_probs))
    env.dict_trimmer(next_state_probs)
    print(len(next_state_probs))




