
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
    
    # nested class that contains prediction results for goals, assists, bonus, minutes played, etc
    class PredictedAnalytics:
        def __init__(
            self,
            goals: np.ndarray,
            assists: np.ndarray,
            clean_sheets: np.ndarray = None,
            bonus: Optional[np.ndarray] = None,
            minutes_played: Optional[np.ndarray] = None,
            own_goals: Optional[np.ndarray] = None,
            goals_conceded: Optional[np.ndarray] = None,
            penalties_missed: Optional[np.ndarray] = None,
            penalties_saved: Optional[np.ndarray] = None,
            red_cards: Optional[np.ndarray] = None,
            saves: Optional[np.ndarray] = None,
            yellow_cards: Optional[np.ndarray] = None,
        ):
            self.goals = goals
            self.assists = assists
            self.bonus = bonus
            self.minutes_played = minutes_played
            self.clean_sheets = clean_sheets
            self.own_goals = own_goals
            self.goals_conceded = goals_conceded
            self.penalties_missed = penalties_missed
            self.penalties_saved = penalties_saved
            self.red_cards = red_cards
            self.saves = saves
            self.yellow_cards = yellow_cards
        

    @staticmethod
    def predict_num_clean_sheets_from_fixture_difficulty_rating(
        player,
        fixture_difficulty_rating: float
    )-> Optional[float]:
        """
        Computes the points contribution from clean sheets

        uses expected_clean_sheets_per_90 and gameweek difficulty to decide
        """
        expected_num_clean_sheets_per_90 = float(player.fpl_player.clean_sheets_per_90)
        if get_gameweek_difficulty_category(fixture_difficulty_rating) == GameWeekDifficultyCategory.EASY:
            return 1.5*expected_num_clean_sheets_per_90
        elif get_gameweek_difficulty_category(fixture_difficulty_rating) == GameWeekDifficultyCategory.MODERATE:
            return 1*expected_num_clean_sheets_per_90
        elif get_gameweek_difficulty_category(fixture_difficulty_rating) == GameWeekDifficultyCategory.HARD:
            return 0.75*expected_num_clean_sheets_per_90
        else:
            warn(f"Invalid gameweek difficulty rating={fixture_difficulty_rating} provided")

    @staticmethod
    def predict_num_goals_scored_from_fixture_difficulty_rating(
        player,
        fixture_difficulty_rating: float
    )-> Optional[float]:
        """
        Computes the points contribution from goals scored

        uses expected_goals_per_90 and gameweek difficulty to decide
        """
        expected_num_goals_per_90 = float(player.fpl_player.expected_goals_per_90)
        if get_gameweek_difficulty_category(fixture_difficulty_rating) == GameWeekDifficultyCategory.EASY:
            return 1.5*expected_num_goals_per_90 # NEBUG IMPROVEMENT: tune this FACTOR by seeing what it predicts for top & not so top players
        elif get_gameweek_difficulty_category(fixture_difficulty_rating) == GameWeekDifficultyCategory.MODERATE:
            return 1*expected_num_goals_per_90 # NEBUG IMPROVEMENT: tune this FACTOR by seeing what it predicts for top & not so top players
        elif get_gameweek_difficulty_category(fixture_difficulty_rating) == GameWeekDifficultyCategory.HARD:
            return 0.75*expected_num_goals_per_90 # NEBUG IMPROVEMENT: tune this FACTOR by seeing what it predicts for top & not so top players
        else:
            warn(f"Invalid gameweek difficulty rating={fixture_difficulty_rating} provided")

    @staticmethod
    def predict_num_assists_from_fixture_difficulty_rating(
        player,
        fixture_difficulty_rating: float
    )-> Optional[float]:
        """
        Computes the points contribution from assists

        uses expected_assists_per_90 and gameweek difficulty to decide
        """
        expected_num_assists_per_90 = float(player.fpl_player.expected_assists_per_90)
        if get_gameweek_difficulty_category(fixture_difficulty_rating) == GameWeekDifficultyCategory.EASY:
            return 1.5*expected_num_assists_per_90 # NEBUG IMPROVEMENT: tune this FACTOR by seeing what it predicts for top & not so top players
        elif get_gameweek_difficulty_category(fixture_difficulty_rating) == GameWeekDifficultyCategory.MODERATE:
            return 1*expected_num_assists_per_90
        elif get_gameweek_difficulty_category(fixture_difficulty_rating) == GameWeekDifficultyCategory.HARD:
            return 0.75*expected_num_assists_per_90
        else:
            warn(f"Invalid gameweek difficulty rating={fixture_difficulty_rating} provided")
        

    @staticmethod
    def predict_analytics_directly_related_to_points(
        player,
        number_of_gameweeks: int,
    )-> PredictedAnalytics:
        """
        Computes the expected points for the next number_of_gameweeks
        """
        expected_goals_for_gameweeks = np.zeros(number_of_gameweeks)
        expected_assists_for_gameweeks = np.zeros(number_of_gameweeks)
        expected_clean_sheets_for_gameweeks = np.zeros(number_of_gameweeks)


        for i, gameweek_fixture_difficulty_rating in enumerate(player.fixture_difficulty_ratings):
            total_expected_goals_for_gameweek = 0
            total_expected_assists_for_gameweek = 0
            total_expected_clean_sheets_for_gameweek = 0
            
            for _,fixture_difficulty_rating in gameweek_fixture_difficulty_rating.items():
                fdr = float(fixture_difficulty_rating)
                total_expected_goals_for_gameweek += Predict.predict_num_goals_scored_from_fixture_difficulty_rating(player, fdr)
                total_expected_assists_for_gameweek += Predict.predict_num_assists_from_fixture_difficulty_rating(player, fdr)
                total_expected_clean_sheets_for_gameweek += Predict.predict_num_clean_sheets_from_fixture_difficulty_rating(player, fdr)
            expected_goals_for_gameweeks[i] = round(total_expected_goals_for_gameweek, 1)
            expected_assists_for_gameweeks[i] = round(total_expected_assists_for_gameweek, 1)
            expected_clean_sheets_for_gameweeks[i] = round(total_expected_clean_sheets_for_gameweek, 1)

        return Predict.PredictedAnalytics(goals=expected_goals_for_gameweeks, assists=expected_assists_for_gameweeks, clean_sheets=expected_clean_sheets_for_gameweeks)
    
        