from lot import Lot, State

class Env:
    def __init__(self):
        self.lots = (Lot(3,3),Lot(2,4))

        self.lot1, self.lot2 = self.lots

        self.states = {(i,j):State((i,j)) for i in range(self.lot1.max_car + 1) for j in range(self.lot2.max_car + 1)}        #master list of all states indexed by their tuple values

        self.delta_probs = self._delta_probs()      #list of dictionaries with values of probability of the lot's cars changing by the key. [0] is the first lot, [1] is the second
        self.assign_state_probs()

    def assign_state_probs(self):
        for state in self.states.values():                  #goes through masterlist and assigns each state a dictionary of each possible next state and it's probability
            self.next_state_probs(state)                    #assignment function
            self.dict_trimmer(state.next_states)       #again trims down the dict removing low probability state changes
            for other in state.next_states.keys():
                state.next_state_rewards[other] = self.expected_reward(state,other)

    def expected_reward(self,state,other):
        i = 0
        tote_reward = 0
        for lot in self.lots:
            reward = 0
            tote_weight = 0
            for num_in in list(lot.probs_in.keys()):
                for num_out in list(lot.probs_out.keys()):
                    delta = num_in - num_out
                    if other.tup[i] - state.tup[i] == delta:
                        weight = lot.probs_in[num_in]*lot.probs_out[num_out]
                        tote_weight += weight
                        reward += num_out*lot.car_rental_price*weight/tote_weight
                        break
            i += 1
            tote_reward += reward
        return tote_reward


    def next_state_probs(self,og_state=None):     #will use delta_probs to figure out the probability of entering into the new states (by the og car number changing by delta)
        if og_state == None:
            og_state = self.states[(lot1.cars, lot2.cars)]  #obtains og state from the masterlist
        
        next_states = {}    #states that the environment can go to
        outside_prob = 0   #probability that environment will go out of bounds

        lot1_possible_changes = list(self.delta_probs[0].keys())
        lot2_possible_changes = list(self.delta_probs[1].keys())
        
        for change1 in lot1_possible_changes:
            lot1_state = og_state.lot1_cars + change1
            if lot1_state < 0 or lot1_state > self.lots[0].max_car: #outside flag tripped
                outside_prob += self.delta_probs[0][change1]    #add entire prob of this lot being at this state
                continue
            for change2 in lot2_possible_changes:
                lot2_state = og_state.lot2_cars + change2
                state_prob = self.delta_probs[0][change1] * self.delta_probs[1][change2]
                if lot2_state < 0 or lot2_state > self.lots[1].max_car: #outside flag tripped
                    outside_prob += state_prob   #add specific prob of both lots being at this state
                    continue

                next_states[self.states[(lot1_state,lot2_state)]] = state_prob      #gets state from master list, uses state as key, assigns its probability as value
            
        og_state.next_states = next_states
        og_state.outside_states = outside_prob


    def _delta_probs(self):      #returns a list of dictionaries with values of probability of the lot's cars changing by the key. [0] is the first lot, [1] is the second
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
    state = env.states[(1,1)]
    env.assign_state_probs()
    vi = 0
    for k,v in state.next_states.items():
        vi += v
    vo = state.outside_states
    print(vi)
    print(vo)


