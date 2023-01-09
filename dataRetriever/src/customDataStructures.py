import json
import numpy as np
from settings import POINTS_PER_ASSIST_DEFENDER, POINTS_PER_ASSIST_GOALKEEPER, POINTS_PER_ASSIST_MIDFIELDER, POINTS_PER_GOAL_DEFENDER, POINTS_PER_GOAL_GOALKEEPER, POINTS_PER_GOAL_MIDFIELDER
from points_predictor import Predict
from settings import FIXTURE_DIFFICULTY_RATINGS_FILEPATH, MAX_GAMEWEEKS,POINTS_PER_GOAL_FORWARD,POINTS_PER_ASSIST_FORWARD, POINTS_PER_CLEAN_SHEET_FORWARD,POINTS_PER_CLEAN_SHEET_GOALKEEPER,POINTS_PER_CLEAN_SHEET_DEFENDER,POINTS_PER_CLEAN_SHEET_MIDFIELDER 
from fpl.models.player import Player as FPLPlayer

class Status(object):
    def __init__(
        self,
        isWildCardAvailable,
        isFreehitAvailable,
        isTripleCaptainAvailable,
        isBenchBoostAvailable,
        noFreeTransfersAvailable,
        bankBalance,
        gameweekNo,
    ):
        self.isWildCardAvailable = isWildCardAvailable
        self.isFreehitAvailable = isFreehitAvailable
        self.isTripleCaptainAvailable = isTripleCaptainAvailable
        self.isBenchBoostAvailable = isBenchBoostAvailable
        self.noFreeTransfersAvailable = noFreeTransfersAvailable
        self.bankBalance = bankBalance
        self.gameweekNo = gameweekNo

    def getJson(self):
        """
        Returns JSON string representation of `Status` object
        """
        self.statusDictionary = {
            "isWildCardAvailable": self.isWildCardAvailable,
            "isFreehitAvailable": self.isFreehitAvailable,
            "isTripleCaptainAvailable": self.isTripleCaptainAvailable,
            "isBenchBoostAvailable": self.isBenchBoostAvailable,
            "noFreeTransfersAvailable": self.noFreeTransfersAvailable,
            "bankBalance": self.bankBalance,
            "gameweekNo": self.gameweekNo,
        }
        return json.dumps(self.statusDictionary)


class PlayerData(object):
    def __init__(
        self,
        club_name,
        club_id,
        name,
        position,
        value,
        form,
        minutesPlayed,
        goals,
        assists,
        bonus,
        cleansheets,
        start_gameweek: int,
        number_of_gameweeks: int,
        fpl_player: FPLPlayer,
    ):
        self.club_name = club_name
        self.club_id: int = club_id
        self.name = name
        self.position = position
        self.value = value
        self.form = form
        self.minutesPlayed = minutesPlayed
        self.goals = goals
        self.assists = assists
        self.bonus = bonus
        self.cleansheets = cleansheets
        self.start_game_week: int = start_gameweek
        self.number_of_gameweeks: int = number_of_gameweeks
        self.fpl_player: FPLPlayer = fpl_player

        self.fixture_difficulty_ratings = self._get_fixture_diffiulty_ratings_from_file(start_gameweek, number_of_gameweeks)
        self.predicted_points = self._get_predicted_gameweek_points()
        self.avg_predicted_points = None

    def _get_fixture_diffiulty_ratings_from_file(self,start_gameweek: int, n: int)->list[dict[str, int]]:
        assert n >3, "n must be greater than 3"
        
        # get fixture difficulty rating from FIXTURE_DIFFICULTY_RATINGS_FILEPATH json file
        with open(FIXTURE_DIFFICULTY_RATINGS_FILEPATH, "r") as f:
            fixture_dfficulty_rating_by_gameweek = json.load(f)

        # TODO: FUTURE: improve to use fixture difficulty based on player's position (and if possible based on the player himself as well)

        # get fixture difficulty rating for the next n gameweeks for this player's club
        end_gameweek = min(start_gameweek + n-1, MAX_GAMEWEEKS)

        fixture_difficulty_ratings: list[dict[str, int]] = [
            fixture_dfficulty_rating_by_gameweek[str(gameweek)][self.club_name]
            for gameweek in range(start_gameweek, end_gameweek+1)
        ]

        return fixture_difficulty_ratings


    def _get_points_per_goal_based_on_position(self):
        if self.position == "FWD":
            return POINTS_PER_GOAL_FORWARD
        elif self.position == "MID":
            return POINTS_PER_GOAL_MIDFIELDER
        elif self.position == "DEF":
            return POINTS_PER_GOAL_DEFENDER
        elif self.position == "GK":
            return POINTS_PER_GOAL_GOALKEEPER
        else:
            raise Exception(
                f"Player has invalid position ({self.position}), cannot get points per goal"
            )

    def _get_points_per_assist_based_on_position(self):
        if self.position == "FWD":
            return POINTS_PER_ASSIST_FORWARD
        elif self.position == "MID":
            return POINTS_PER_ASSIST_MIDFIELDER
        elif self.position == "DEF":
            return POINTS_PER_ASSIST_DEFENDER
        elif self.position == "GK":
            return POINTS_PER_ASSIST_GOALKEEPER
        else:
            raise Exception(
                f"Player has invalid position ({self.position}), cannot get points per assist"
            )
    def _get_points_per_cleansheet_based_on_position(self):
        if self.position == "FWD":
            return POINTS_PER_CLEAN_SHEET_FORWARD
        elif self.position == "MID":
            return POINTS_PER_CLEAN_SHEET_MIDFIELDER
        elif self.position == "DEF":
            return POINTS_PER_CLEAN_SHEET_DEFENDER
        elif self.position == "GK":
            return POINTS_PER_CLEAN_SHEET_GOALKEEPER
        else:
            raise Exception(
                f"Player has invalid position ({self.position}), cannot get points per cleansheet"
            )
    def _get_predicted_gameweek_points(self) -> list[float]:
        """
        Predicts the player's points for the next n gameweeks
        """
        POINTS_PER_GOAL = self._get_points_per_goal_based_on_position()
        POINTS_PER_ASSIST = self._get_points_per_assist_based_on_position()
        POINTS_PER_CLEAN_SHEET = self._get_points_per_cleansheet_based_on_position()

        n = self.number_of_gameweeks
        predicted_analytics = Predict.predict_analytics_directly_related_to_points(player=self, number_of_gameweeks=n)
        points_contribution_from_goals: np.ndarray = POINTS_PER_GOAL*predicted_analytics.goals
        points_contribution_from_assists: np.ndarray = POINTS_PER_ASSIST*predicted_analytics.assists
        points_contribution_from_clean_sheets: np.ndarray = POINTS_PER_CLEAN_SHEET*predicted_analytics.clean_sheets

        # let's assume everyone gets max points for minutes
        # if minutes are equal for any 2 players, the one with goals, assists, cleansheets will rank higher
        points_contribution_from_minutes = np.full(n, 2) 
        # NEBUG: optional: improvement: consider whether working out bonus estimate is worth it
        points_contribution_from_bonus = np.full(n, 1)
        
        # NEBUG: TODO add metrics that apply to mf, def and goalies

        predicted_points = (
            points_contribution_from_goals
            + points_contribution_from_assists
            + points_contribution_from_bonus
            + points_contribution_from_minutes
            + points_contribution_from_clean_sheets
        )

        # round values in predicted_points to 1 decimal place
        predicted_points = np.round(predicted_points, 1)

        # get average of numpy array predicted_points
        self.avg_predicted_points = np.mean(predicted_points)

        return predicted_points.tolist()