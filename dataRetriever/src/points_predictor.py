
from enum import Enum
from logging import warn
from typing import Optional
import numpy as np


class GameWeekDifficultyCategory(str, Enum):
    EASY = "EASY"
    MODERATE = "MODERATE"
    HARD = "HARD"

def get_gameweek_difficulty_category(gameweek_difficulty:float) -> GameWeekDifficultyCategory:

    if gameweek_difficulty >=1 and gameweek_difficulty <= 2.5:
        return GameWeekDifficultyCategory.EASY
    elif gameweek_difficulty >2.5 and gameweek_difficulty <= 3.5:
        return GameWeekDifficultyCategory.MODERATE
    elif gameweek_difficulty >3.5 and gameweek_difficulty <= 5:
        return GameWeekDifficultyCategory.HARD
    else:
        raise ValueError("gameweek difficulty must be a number between 1 and 5")
class Predict:
        
    @staticmethod
    def compute_points_contribution_from_minutes_played(
        player, 
    ):
        """
        Computes the points contribution from minutes played
        """
        return [] #TODO: NEBUG: implement this function OR DELETE THIS FUNCTION


    @staticmethod
    def predict_num_goals_scored_from_fixture_difficulty_rating(
        player,
        fixture_difficulty_rating: float
    )-> Optional[float]:
        """
        Computes the points contribution from goals scored

        uses expected_goals_per_90 and gameweek difficulty to decide
        """
        expected_goals_per_90 = float(player.fpl_player.expected_goals_per_90)
        if get_gameweek_difficulty_category(fixture_difficulty_rating) == GameWeekDifficultyCategory.EASY:
            return 1.5*expected_goals_per_90 #NEBUG: tune this FACTOR by seeing what it predicts for top & not so top players
        elif get_gameweek_difficulty_category(fixture_difficulty_rating) == GameWeekDifficultyCategory.MODERATE:
            return 1*expected_goals_per_90 #NEBUG: tune this FACTOR by seeing what it predicts for top & not so top players
        elif get_gameweek_difficulty_category(fixture_difficulty_rating) == GameWeekDifficultyCategory.HARD:
            return 0.75*expected_goals_per_90 #NEBUG: tune this FACTOR by seeing what it predicts for top & not so top players
        else:
            warn(f"Invalid gameweek difficulty rating={fixture_difficulty_rating} passed")

            
    @staticmethod
    def predict_number_of_goals_scored(
        player,
        number_of_gameweeks: int,
    )-> np.ndarray:
        """
        Computes the expected goals scored for the next number_of_gameweeks
        """
        expected_goals_for_gameweeks = np.zeros(number_of_gameweeks)


        for i, gameweek_fixture_difficulty_rating in enumerate(player.fixture_difficulty_ratings):
            total_expected_goals_for_gameweek = 0
            
            for _,fixture_difficulty_rating in gameweek_fixture_difficulty_rating.items():
                total_expected_goals_for_gameweek += Predict.predict_num_goals_scored_from_fixture_difficulty_rating(player, float(fixture_difficulty_rating))
            expected_goals_for_gameweeks[i] = round(total_expected_goals_for_gameweek, 1)

        return expected_goals_for_gameweeks
        

    
        