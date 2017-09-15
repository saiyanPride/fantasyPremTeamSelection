class Status(object):
    def __init__(self, isWildCardAvailable, isFreehitAvailable, isTripleCaptainAvailable, isBenchBoostAvailable, noFreeTransfersAvailable, bankBalance, gameweekNo):
        self.isWildCardAvailable = isWildCardAvailable
        self.isFreehitAvailable = isFreehitAvailable
        self.isTripleCaptainAvailable = isTripleCaptainAvailable
        self.isBenchBoostAvailable = isBenchBoostAvailable
        self.noFreeTransfersAvailable = noFreeTransfersAvailable
        self.bankBalance = bankBalance
        self.gameweekNo = gameweekNo


class TeamMember(object):
    def __init__(self, teamId, playerId, isStarting, isSubstitute, isCaptain, isViceCaptain):
        self.teamId = teamId
        self.playerId = playerId
        self.isStarting = isStarting
        self.isSubstitute = isSubstitute
        self.isCaptain = isCaptain
        self.isViceCaptain = isViceCaptain


class PlayerData(object):
    def __init__(self, club, name, position, value, form, minutesPlayed):
        self.club = club
        self.name = name
        self.position = position
        self.value = value
        self.form = form
        self.minutesPlayed = minutesPlayed
        self.goals=''
        self.assists=''
        self.bonus=''
        self.cleansheets=''
        self.gameweekScores=[]

    def getGameweekScoreEstimates(self,gameweekDifficultyList, currentGameWeekNo):
        """
        In order to determine % contribution of (goals+assists) to a players score. The best case is taken as follows:
        - players scores every gameweek and assists every other gamweek (suited to striker) OR
        - players assists every gameweek and scores every other gamweek (suited to MF)
        """
        maxGWD = 5.0 # GWD -> gameweek difficulty
        maxForm=10.0 #
        maxBonus=currentGameWeekNo*3.0
        maxGoalsAndAssists=currentGameWeekNo+currentGameWeekNo/2.0

        if self.position == 'DEF':
            self.gameweekScores=[ 85*((maxGWD-gwd+1)/maxGWD)+ 15*((self.goals+self.assists)/maxGoalsAndAssists) for gwd in gameweekDifficultyList]
        elif self.position == 'MID':
            #Score =40%(GWD),  45%(goals+assists) 10%Form   5% Bonus 
            self.gameweekScores=[ 40*((maxGWD-gwd+1)/maxGWD)+ 45*((self.goals+self.assists)/maxGoalsAndAssists)+10*(self.form/maxForm) +5*(self.bonus/maxBonus) for gwd in gameweekDifficultyList]
        elif self.position == 'FWD':
            # Score =30%(GWD),  55%(goals+assists) 10%Form   5% Bonus 
            self.gameweekScores=[ 30*((maxGWD-gwd+1)/maxGWD)+ 55*((self.goals+self.assists)/maxGoalsAndAssists)+10*(self.form/maxForm) + 5*(self.bonus/maxBonus) for gwd in gameweekDifficultyList]
        elif self.position == 'GKP':
            # Score = 60*(GWD) + 28%(clean sheets) + 2%Bonus
            self.gameweekScores=[ 60*((maxGWD-gwd+1)/maxGWD)+ 28*(self.cleansheets/float(currentGameWeekNo)) + 2*(self.bonus/maxBonus) for gwd in gameweekDifficultyList]       
        else:
            raise ValueError(
                '%s has an invalid position: %s' %(self.name, self.position))
        print ("%s score for next week is: %s " % (self.name, str(self.gameweekScores[0]) ) )