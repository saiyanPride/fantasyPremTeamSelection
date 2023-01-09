import json
import numpy as np
from points_predictor import Predict
from settings import FIXTURE_DIFFICULTY_RATINGS_FILEPATH, MAX_GAMEWEEKS,POINTS_PER_GOAL_FORWARD,POINTS_PER_ASSIST_FORWARD
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

    def _get_predicted_gameweek_points(self):
        """
        Predicts the player's scores for the next n gameweeks
        """

        # set predicted points for this player based on position
        if self.position == "DEF":
            return self._get_predicted_points_for_defender()
        elif self.position == "MID":
            return self._get_predicted_points_for_midfielder()
        elif self.position == "FWD":
            return self._get_predicted_points_for_forward()
        elif self.position == "GK":
            return self._get_predicted_points_for_goalkeeper()
        else:
            raise Exception(
                f"Player has invalid position ({self.position}), cannot predict points"
            )

    def _get_predicted_points_for_forward(
        self,
    ):
        """
        Sets the predicted points for a forward

        The total score is composed of:
            points_contribution_from_minutes
            points_contribution_from_goals
            points_contribution_from_assists
            points_contribution_from_bonus
        """
        #TODO NEBUG: also factor in the likelihood player will get 60mins (if really injured points is 0), if player won't play just return 0
        # create numpy array of length self.number_of_gameweeks
        n = self.number_of_gameweeks
        predicted_analytics = Predict.predict_analytics_directly_related_to_points(player=self, number_of_gameweeks=n)
        points_contribution_from_goals: np.ndarray = POINTS_PER_GOAL_FORWARD*predicted_analytics.goals
        points_contribution_from_minutes = np.zeros(n) # NEBUG: TODO: decide whether to include this or not, cna just base on goals and assists
        points_contribution_from_assists: np.ndarray = POINTS_PER_ASSIST_FORWARD*predicted_analytics.assists
        points_contribution_from_bonus = np.zeros(n) # NEBUG: TODO: decide whether to include this or not

        # predicted_points is the sum of the above 4 numpy arrays
        predicted_points = (
            points_contribution_from_goals
            + points_contribution_from_minutes
            + points_contribution_from_assists
            + points_contribution_from_bonus
        )

        # round values in predicted_points to 1 decimal place
        predicted_points = np.round(predicted_points, 1)

        # get average of numpy array predicted_points
        self.avg_predicted_points = np.mean(predicted_points)

        return predicted_points.tolist()

    def _get_predicted_points_for_midfielder(
        self, 
    ):
        return None  # TODO: NEBUG: implement this function
    
    def _get_predicted_points_for_defender(
        self, 
    ) -> list[float]:
        """Returns a list of predicted points for the next n gameweeks for a defender"""
        return None  #  TODO: NEBUG: implement this function

    def _get_predicted_points_for_goalkeeper(
        self, 
    ):
        return None  # TOOD: NEBUG: implement this function

    def getGameweekScoreEstimates(
        self, gameweekDifficultyList, currentGameWeekNo
    ):  # TODO NEBUG: DELETE THIS FUNCTION
        """
        Calculates a score out of 100 for the player
        This score gives an indication of the players chances of obtaining large fantasy points during `currentGameWeekNo`
        The rules for determining a player's score depends on his position
        Goal scoring record has a much larger contribution for striker's scores than defender's scores
        """
        maxGWD = 5.0  # GWD -> gameweek difficulty
        maxForm = 10.0
        maxBonus = currentGameWeekNo * 3.0
        maxGoalsAndAssists = currentGameWeekNo + currentGameWeekNo / 2.0

        if self.position == "DEF":
            self.gameweekScores = [
                85 * ((maxGWD - gwd + 1) / maxGWD)
                + 15 * ((self.goals + self.assists) / maxGoalsAndAssists)
                for gwd in gameweekDifficultyList
            ]
        elif self.position == "MID":
            # Score =40%(GWD),  45%(goals+assists) 10%Form   5% Bonus
            self.gameweekScores = [
                40 * ((maxGWD - gwd + 1) / maxGWD)
                + 45 * ((self.goals + self.assists) / maxGoalsAndAssists)
                + 10 * (self.form / maxForm)
                + 5 * (self.bonus / maxBonus)
                for gwd in gameweekDifficultyList
            ]
        elif self.position == "FWD":
            # Score =30%(GWD),  55%(goals+assists) 10%Form   5% Bonus
            self.gameweekScores = [
                30 * ((maxGWD - gwd + 1) / maxGWD)
                + 55 * ((self.goals + self.assists) / maxGoalsAndAssists)
                + 10 * (self.form / maxForm)
                + 5 * (self.bonus / maxBonus)
                for gwd in gameweekDifficultyList
            ]
        elif self.position == "GKP":
            # Score = 60*(GWD) + 28%(clean sheets) + 2%Bonus
            self.gameweekScores = [
                60 * ((maxGWD - gwd + 1) / maxGWD)
                + 28 * (self.cleansheets / float(currentGameWeekNo))
                + 2 * (self.bonus / maxBonus)
                for gwd in gameweekDifficultyList
            ]
        else:
            raise ValueError(
                "%s has an invalid position: %s" % (self.name, self.position)
            )
        # print ("%s score for next week is: %s " %(self.name, str(self.gameweekScores[0])))
