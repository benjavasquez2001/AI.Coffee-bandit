import numpy as np

class EpsilonGreedyBandit:
    def __init__(self, arms, epsilon=0.1):
        self.arms = arms
        self.epsilon = epsilon
        self.counts = {arm: 0 for arm in arms}
        self.values = {arm: 0.0 for arm in arms}

    def choose_arm(self):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.arms)
        else:
            return max(self.arms, key=lambda arm: self.values[arm])

    def update(self, chosen_arm, reward):
        self.counts[chosen_arm] += 1
        n = self.counts[chosen_arm]
        value = self.values[chosen_arm]
        # incremental average
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[chosen_arm] = new_value

    def get_stats(self):
        return {
            "counts": self.counts,
            "values": self.values
        }
