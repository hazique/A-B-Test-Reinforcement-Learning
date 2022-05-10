from abc import (
    ABC,
    abstractmethod,
)
import numpy as np
from collections import defaultdict
from typing import List

class Bandit:
    def __init__(self, p: float, id):
        """
        Simulates bandit.
        Args:
            p: Probability of success.
        """
        self.p = p
        self.id = id

    def pull(self):
        """
        Simulate pulling the arm of the bandit.
        """
        return np.random.binomial(1, self.p, size=1)[0]

class NoBanditsError(Exception):
    ...


class BanditRewardsLog:
    def __init__(self):
        self.total_actions = 0
        self.total_rewards = 0
        self.all_rewards = []
        self.record = defaultdict(lambda: dict(actions=0, reward=0))

    def record_action(self, bandit, reward):
        self.total_actions += 1
        self.total_rewards += reward
        self.all_rewards.append(reward)
        self.record[bandit.id]['actions'] += 1
        self.record[bandit.id]['reward'] += reward

    def __getitem__(self, bandit):
        return self.record[bandit.id]


class Agent(ABC):
    def __init__(self):
        self.rewards_log = BanditRewardsLog()
        self._bandits = None

    @property
    def bandits(self) -> List[Bandit]:
        if not self._bandits:
            raise NoBanditsError()
        return self._bandits

    @bandits.setter
    def bandits(self, val: List[Bandit]):
        self._bandits = val

    @abstractmethod
    def take_action(self):
        ...

    def take_actions(self, n: int):
        for _ in range(n):
            self.take_action()



class EpsilonGreedyAgent(Agent):
    def __init__(self, rewards_log, banditas, epsilon: float = None):
        '''
        If epsilon=None it defaults to epsilon = 1 / #actions.
        '''
        super().__init__()
        self.epsilon = epsilon
        if rewards_log:
            self.rewards_log = rewards_log
        if banditas:
            self.bandits = banditas

    def get_random_bandit(self):
        bandit = np.random.choice(self.bandits)
        return bandit

    def _get_current_best_bandit(self) -> Bandit:
        estimates = []
        for bandit in self.bandits:
            bandit_record = self.rewards_log[bandit]
            if not bandit_record['actions']:
                estimates.append(0)
            else:
                estimates.append(bandit_record['reward'] / bandit_record['actions'])

        return self.bandits[np.argmax(estimates)]

    def choose_bandit(self):
        epsilon = self.epsilon or 1 / (1 + self.rewards_log.total_actions)

        p = np.random.uniform(0, 1, 1)
        if p < epsilon:
            bandit = self.get_random_bandit()
        else:
            bandit = self._get_current_best_bandit()

        return bandit.id


    def take_action(self, bandit_id, result):
        current_bandit = list(filter((lambda x: x.id == bandit_id), self.bandits))[0]
        # current_bandit = self._choose_bandit()
        # reward = current_bandit.pull()
        self.rewards_log.record_action(current_bandit, result)

    def __repr__(self):
        return 'EpsilonGreedyAgent(epsilon={})'.format(self.epsilon)