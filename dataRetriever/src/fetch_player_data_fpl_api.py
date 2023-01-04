import asyncio

import aiohttp
from prettytable import PrettyTable

from fpl import FPL
from fpl.models.player import Player as FPLPlayer

from customDataStructures import PlayerData

"""
NEBUG DELETE
self.club = club
        self.name = name
        self.position = position
        self.value = value
        self.form = form
        self.minutesPlayed = minutesPlayed
        self.goals = ''
        self.assists = ''
        self.bonus = ''
        self.cleansheets = ''
        self.gameweekScores = []

"""
async def main():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        players = await fpl.get_players()
        teams = await fpl.get_teams()#TODO: NEBUG: make sure you are using ayncio properly

    team_id_to_team_name = {team.id: team.name for team in teams}

    player_analytics = compute_player_analytics_for_next_n_gameweeks(players, n = 5)
    display_player_analytics(player_analytics,team_id_to_team_name)


def convert_element_type_to_position(element_type: int) -> str:
    # use a switch statement to convert the element type to a position
    if element_type == 1:
        return "GK"
    elif element_type == 2:
        return "DEF"
    elif element_type == 3:
        return "MID"
    elif element_type == 4:
        return "FWD"
    else:
        return "Unknown"


def display_player_analytics(player_analytics: list[PlayerData], team_id_to_team_name: dict[int, str]):
    player_table = PrettyTable()
    player_table.field_names = ["Player", "Club", "Position", "Price", "Form", "MinutesPlayed", "Goals", "Assists", "Bonus", "Cleansheets", "AvgPredictedPoints"]
    player_table.align["Player"] = "l" # Left align player names
    
    # sort the players by their form
    player_analytics.sort(key=lambda player: player.form, reverse=True)

    # for each player, add a row to the table
    for player in player_analytics[:50]:
        player_table.add_row([player.name, team_id_to_team_name[player.club_id], player.position, player.value, player.form, player.minutesPlayed, player.goals, player.assists, player.bonus, player.cleansheets, player.avg_predicted_points])

    print(player_table)

def compute_player_analytics_for_next_n_gameweeks(players: list[FPLPlayer], n: int) -> list[PlayerData]:
    """
    n is the number of gameweeks to predict points for
    """
    player_analytics = []

    for player in players:
        player_data = PlayerData()
        player_data.name = player.web_name
        player_data.club_id = player.team
        player_data.position = convert_element_type_to_position(player.element_type)
        player_data.value = player.now_cost/10
        player_data.form = player.form
        player_data.minutesPlayed = player.minutes
        player_data.goals = player.goals_scored
        player_data.assists = player.assists
        player_data.bonus = player.bonus
        player_data.cleansheets = player.clean_sheets
        #player_data.predictGameWeekScores(n) # TODO: implement this function NEBUG
        player_analytics.append(player_data)
    
    return player_analytics


if __name__ == "__main__":
    asyncio.run(main())