"""
3 reward systems

    1. Elimination reward = N^2*E*F

    where:
        N - the total amount initially at the begining of the round
        E - is the eliminated ratio percentage in decimal form
        F - Factor to scale down the final number

    2. Based on the difference in shannon entropy before and after the round

    3. Final reward is based on whether the final guess was right:
        +1 if correct
        -1 if wrong

    Notes:
        1 and 2 are rewarded after each round and accumulate
        3 is rewarded only at the end of the 5th round
        All points are then added up and passed to the questions selector nn for training
"""


class RewardSystem:
    """Calculates question rewards and final game rewards for the QuestionSelector.
    Uses a simple reinforcement learning approach based on game feedback."""

    def __init__(self,):
        self.elmination_points = 0
        self.entropy_points = 0
        self.final_guess_points = 0
        
