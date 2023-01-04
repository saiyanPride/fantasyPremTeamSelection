import asyncio

import aiohttp
from prettytable import PrettyTable

from fpl import FPL

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
        teams = await fpl.get_teams()

    team_id_to_team_name = {team.id: team.name for team in teams}

    top_performers = sorted(
        players, key=lambda x: x.goals_scored + x.assists, reverse=True)

    player_table = PrettyTable()
    player_table.field_names = ["Player", "Club", "Position", "Price", "Form", "MinutesPlayed", "Goals", "Assists", "Bonus", "Cleansheets"]
    player_table.align["Player"] = "l" # Left align player names

    for player in top_performers[:20]:
        player_table.add_row([player.web_name, team_id_to_team_name[player.team], convert_element_type_to_position(player.element_type),
        player.now_cost/10, player.form, player.minutes,
        player.goals_scored, player.assists, player.bonus, player.clean_sheets])

    print(player_table)


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

if __name__ == "__main__":
    asyncio.run(main())