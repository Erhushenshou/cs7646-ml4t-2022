import QLearner as ql
learner = ql.QLearner(num_states=100,
                      num_actions=4,
                      alpha=0.2,
                      gamma=0.9,
                      rar=0.98,
                      radr=0.999,
                      dyna=0,
                      verbose=False)
s = 99 # our initial state
a = learner.querysetstate(s) # action for state s
s_prime = 5 # the new state we end up in after taking action a in state s
r = 0 # reward for taking action a in state s
next_action = learner.query(s_prime, r)
print(learner.T_c)
print(learner.T_c.shape)
print(learner.T)
print(learner.T.shape)