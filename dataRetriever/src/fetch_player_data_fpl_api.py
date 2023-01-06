import asyncio

import aiohttp
from prettytable import PrettyTable

from fpl import FPL
from fpl.models.player import Player as FPLPlayer

from customDataStructures import PlayerData


async def main():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        # create task to get players
        players_task = asyncio.create_task(fpl.get_players())
        # create task to get teams
        teams_task = asyncio.create_task(fpl.get_teams())

        # wait for both tasks to complete
        players, teams = await asyncio.gather(players_task, teams_task)

    team_id_to_team_name = {team.id: team.name for team in teams}

    player_analytics = compute_player_analytics_for_next_n_gameweeks(players, n=5)
    display_player_analytics(player_analytics, team_id_to_team_name)


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


def display_player_analytics(
    player_analytics: list[PlayerData], team_id_to_team_name: dict[int, str]
):
    player_table = PrettyTable()
    player_table.field_names = [
        "Player",
        "Club",
        "Position",
        "Price",
        "Form",
        "MinutesPlayed",
        "Goals",
        "Assists",
        "Bonus",
        "Cleansheets",
        "AvgPredictedPoints",
    ]
    player_table.align["Player"] = "l"  # Left align player names

    # sort the players by their form
    player_analytics.sort(key=lambda player: player.form, reverse=True)

    # for each player, add a row to the table
    for player in player_analytics[:50]:
        player_table.add_row(
            [
                player.name,
                team_id_to_team_name[player.club_id],
                player.position,
                player.value,
                player.form,
                player.minutesPlayed,
                player.goals,
                player.assists,
                player.bonus,
                player.cleansheets,
                player.avg_predicted_points,
            ]
        )

    print(player_table)


def compute_player_analytics_for_next_n_gameweeks(
    players: list[FPLPlayer], n: int
) -> list[PlayerData]:
    """
    n: the number of gameweeks to predict points for
    """
    player_analytics = []

    for player in players:
        player_data = PlayerData(
            name=player.web_name,
            club=None, #TODO: NEBUG: add club name
            club_id=player.team,
            position=convert_element_type_to_position(player.element_type),
            value=player.now_cost / 10,
            form=player.form,
            minutesPlayed=player.minutes,
            goals=player.goals_scored,
            assists=player.assists,
            bonus=player.bonus,
            cleansheets=player.clean_sheets,
        )
        player_data.predict_gameWeek_points(n) #TODO: NEBUG: IMPLEMENT THIS
        player_analytics.append(player_data)

    return player_analytics


if __name__ == "__main__":
    asyncio.run(main())
