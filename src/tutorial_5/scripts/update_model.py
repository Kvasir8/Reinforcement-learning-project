from sklearn import tree
import numpy as np


# Test class for the update algorithm
class Algorithm_2:
    def __init__(self, state, action, reward, next_state, S_M, A_):
        self.state = state
        self.action = action
        # self.stateSet = np.zeros(10)  # states already visited/known
        self.next_state = next_state
        self.S_M = S_M  # stateSet
        # self.reward = {'Goal': 20, 'Move_Leg': -1, 'Fail': -2, 'Fall': -20}  # just exampe values
        self.reward = reward
        # self.possibleStates = [0,1,2,3,4,5,6,7,8,9]
        # self.possibleActions = {'Left': 0, 'Right': 1, 'Kick': 2}
        self.A_ = A_
        self.transitionTree = tree.DecisionTreeClassifier()
        self.rewardTree = tree.DecisionTreeClassifier()
        # self.Pm = np.zeros((10, 3))
        # self.Rm = np.zeros((10, 3))
        self.inputTree = np.zeros(2)
        self.deltaTransition = 0
        self.deltaReward = 0
    '''
    input parameters:
    state_: current state discretized value of the distance from hip to the foot
    action: action determined by the Q-table (among 0, 1 or 2)
    reward: scalar value, given by us based on the result of the action
    next_state: state reached after the action execution
    output:
    CH_: state, if model hs changed -> currently always true, must be changed
    Reward and Transition probability predictions of shape (10,3)
    '''
    def update_model(self):
        # n_ = len(self.S_M)   # size of state_
        CH_ = False
        # Update the tree for each state feature
        # for i in range(n_):
        relative_state_change = self.next_state - self.state  # should result in -1, 0 or 1
        CH_ = self.add_experience_trans(self.state, self.action, relative_state_change)
        # Update the tree for reward
        CH_ = self.add_experience_reward(reward)    # update each tree incrementally with input vector and desired output
        ## Tree updating is done.
        # Combine results for each tree into model
        for s_M in self.S_M:
            for a_M in range(len(self.A_)):
                self.P_M[s_M, a_M] = self.combine_results(s_M, a_M)
                self.R_M[s_M, a_M] = self.get_predictions(s_M, a_M)
        print(self.P_M)
        print(self.R_M)
        return True, self.P_M, self.R_M, CH_

    # Update the tranisition tree based on the relative change of the state
    def add_experience_trans(self, state, action, relative_state_change):
        tmp = np.append(np.array(action), np.array(state))  # input vector
        self.inputTree = np.vstack((self.inputTree, tmp))
        self.deltaTransition = np.append(self.deltaTransition, relative_state_change)
        self.transitionTree = self.transitionTree.fit(self.inputTree, self.deltaTransition)
        return True

    def add_experience_reward(self, reward):
        self.deltaReward = np.append(self.deltaReward, reward)
        self.rewardTree = self.rewardTree.fit(self.inputTree, self.deltaReward)  # must be of form samples,
        return True

    # Compute probabilities of the state change
    def combine_results(self, state, action):
        prob = np.max(self.transitionTree.predict_prob([[action, state]]))
        return prob

    def get_predictions(self, state, action):
        return self.rewardTree.predict([[action, state]])


if __name__ == '__main__':
    # test with arbitrary values
    # state = np.zeros(1)
    # action = 1
    # reward = -1
    # state_ = np.array([1])
    # test = Algorithm_2()
    # test.update_model(state, action, reward, state_)