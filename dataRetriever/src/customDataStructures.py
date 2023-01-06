import json
import numpy as np
from settings import FIXTURE_DIFFICULTY_RATINGS_FILEPATH

class Status(object):
    def __init__(self, isWildCardAvailable, isFreehitAvailable, isTripleCaptainAvailable, isBenchBoostAvailable, noFreeTransfersAvailable, bankBalance, gameweekNo):
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
            'isWildCardAvailable': self.isWildCardAvailable,
            'isFreehitAvailable': self.isFreehitAvailable,
            'isTripleCaptainAvailable': self.isTripleCaptainAvailable,
            'isBenchBoostAvailable': self.isBenchBoostAvailable,
            'noFreeTransfersAvailable': self.noFreeTransfersAvailable,
            'bankBalance': self.bankBalance,
            'gameweekNo': self.gameweekNo
        }
        return json.dumps(self.statusDictionary)


class PlayerData(object):

    def __init__(self, club, club_id, name, position, value, form, minutesPlayed, goals, assists, bonus, cleansheets):
        self.club = club
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
        self.predicted_points = []
        self.avg_predicted_points = None

    def predict_gameWeek_points(self, n):
        """
        Predicts the player's scores for the next n gameweeks
        """

        # get fixture difficulty rating from FIXTURE_DIFFICULTY_RATINGS_FILEPATH json file
        with open(FIXTURE_DIFFICULTY_RATINGS_FILEPATH, 'r') as f:
            fixture_dfficulty_rating_by_gameweek = json.load(f)


        # get fixture difficulty rating for the next n gameweeks for this player's club




        if self.position == 'DEF':
            self.set_predicted_points_for_defender(n) #TODO: NEBUG: implement this function
        elif self.position == 'MID':
            self.set_predicted_points_for_midfielder(n) #TODO: NEBUG: implement this function
        elif self.position == 'FWD':
            self.set_predicted_points_for_forward(n) #TODO: NEBUG: implement this function
        elif self.position == 'GK':
            self.set_predicted_points_for_goalkeeper(n) #TODO: NEBUG: implement this function
        else:
            raise Exception(f"Player has invalid position ({self.position}), cannot predict points")


    def set_predicted_points_for_defender(self, n):
        return None #  TODO: NEBUG: implement this function

    def set_predicted_points_for_midfielder(self, n):
        return None #TODO: NEBUG: implement this function

    def set_predicted_points_for_goalkeeper(self, n):
        return None #TOOD: NEBUG: implement this function

    def set_predicted_points_for_forward(self, n):
        """
        Sets the predicted points for a forward

        The total score is composed of:
            points_contribution_from_minutes
            points_contribution_from_goals 
            points_contribution_from_assists 
            points_contribution_from_bonus 
        """
        # create numpy array of length n
        points_contribution_from_goals  = np.zeros(n) #todo: NEBUG: implement this using fixture difficulty rating, average goals scored, and players form
        points_contribution_from_minutes = np.zeros(n)
        points_contribution_from_assists = np.zeros(n)
        points_contribution_from_bonus = np.zeros(n)

        # self.predicted_points is the sum of the above 4 arrays
        self.predicted_points = points_contribution_from_minutes + points_contribution_from_goals + points_contribution_from_assists + points_contribution_from_bonus
        
        # self.predicted_points is converted to list of doubles
        self.predicted_points = self.predicted_points.tolist()

        # set self.avg_predicted_points to be average of self.predicted_points
        self.avg_predicted_points = sum(self.predicted_points) / len(self.predicted_points)

        



    def getGameweekScoreEstimates(self, gameweekDifficultyList, currentGameWeekNo): # TODO NEBUG: DELETE THIS FUNCTION
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

        if self.position == 'DEF':
            self.gameweekScores = [85 * ((maxGWD - gwd + 1) / maxGWD) + 15 * (
                (self.goals + self.assists) / maxGoalsAndAssists) for gwd in gameweekDifficultyList]
        elif self.position == 'MID':
            # Score =40%(GWD),  45%(goals+assists) 10%Form   5% Bonus
            self.gameweekScores = [40 * ((maxGWD - gwd + 1) / maxGWD) + 45 * ((self.goals + self.assists) / maxGoalsAndAssists) + 10 * (
                self.form / maxForm) + 5 * (self.bonus / maxBonus) for gwd in gameweekDifficultyList]
        elif self.position == 'FWD':
            # Score =30%(GWD),  55%(goals+assists) 10%Form   5% Bonus
            self.gameweekScores = [30 * ((maxGWD - gwd + 1) / maxGWD) + 55 * ((self.goals + self.assists) / maxGoalsAndAssists) + 10 * (
                self.form / maxForm) + 5 * (self.bonus / maxBonus) for gwd in gameweekDifficultyList]
        elif self.position == 'GKP':
            # Score = 60*(GWD) + 28%(clean sheets) + 2%Bonus
            self.gameweekScores = [60 * ((maxGWD - gwd + 1) / maxGWD) + 28 * (self.cleansheets / float(
                currentGameWeekNo)) + 2 * (self.bonus / maxBonus) for gwd in gameweekDifficultyList]
        else:
            raise ValueError(
                '%s has an invalid position: %s' % (self.name, self.position))
        # print ("%s score for next week is: %s " %(self.name, str(self.gameweekScores[0])))
