
from customDataStructures import PlayerData

import numpy as np

class Predict:

    @staticmethod
    def compute_points_contribution_from_minutes_played(
        player: PlayerData, 
    ):
        """
        Computes the points contribution from minutes played
        """
        # get the player's minutes played so far
        season_minutes_played = player.minutes
        season_theoretical_max_possible_minutes = None

    