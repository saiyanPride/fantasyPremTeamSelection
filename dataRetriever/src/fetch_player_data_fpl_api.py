import asyncio
import json
from typing import Any, Callable

import aiohttp
from prettytable import PrettyTable

from fpl import FPL
from fpl.models.player import Player as FPLPlayer

from customDataStructures import PlayerData
from utility import warn
from settings import (
    DEFAULT_NUMBER_OF_GAMWEEKS_TO_PREDICT,
    FIXTURE_DIFFICULTY_RATINGS_FILEPATH,
    MAX_GAMEWEEKS,
)


async def initialise():
    async with aiohttp.ClientSession() as session:
        fpl_client = FPL(session)

        global CURRENT_GAMEWEEK
        CURRENT_GAMEWEEK = fpl_client.current_gameweek

        user_input = input(
            f"Do you want to continue using current gameweek = {CURRENT_GAMEWEEK}? (Y/N): "
        )
        if user_input.lower() != "y":
            # ask user to input the gameweek number to use
            CURRENT_GAMEWEEK = int(input("Please enter the gameweek number to use: "))
            warn(
                f"Using gameweek {CURRENT_GAMEWEEK} instead of current gameweek {fpl_client.current_gameweek}"
            )

        # get teams (intentionally wait until complete as other methods need this info)
        teams = await fpl_client.get_teams()
        global TEAM_ID_TO_TEAM_NAME
        TEAM_ID_TO_TEAM_NAME = {
            team.id: team.name for team in teams
        }  # type: dict[int, str], e.g. {1: "Arsenal", 2: "Aston Villa", ...}

        # create task to get players
        players_task = asyncio.create_task(fpl_client.get_players())

        # create to get fixture difficulty ratings
        fixture_difficulty_ratings_task = asyncio.create_task(
            get_and_persist_fixture_difficulty_ratings(
                fpl_client=fpl_client, current_gameweek=CURRENT_GAMEWEEK
            )
        )

        # wait for both tasks to complete
        players, fixture_difficulty_ratings_by_gameweek = await asyncio.gather(
            players_task, fixture_difficulty_ratings_task
        )

    return players, teams, fixture_difficulty_ratings_by_gameweek, CURRENT_GAMEWEEK


async def main():
    (
        players,
        teams,
        fixture_difficulty_ratings_by_gameweek,
        current_gameweek,
    ) = await initialise()

    Display.display_fixture_difficulty_ratings(fixture_difficulty_ratings_by_gameweek)

    # ask user if they wish to override fixture difficulty ratings in `FIXTURE_DIFFICULTY_RATINGS_FILEPATH`
    user_input = input(
        f"Do you want to continue using fixture difficulty ratings from {FIXTURE_DIFFICULTY_RATINGS_FILEPATH}? (Y/N): "
    )
    if user_input.lower() == "n":
        # ask user to override fixture difficulty ratings in the file and to press enter to continue
        input(
            f"Please override fixture difficulty ratings in {FIXTURE_DIFFICULTY_RATINGS_FILEPATH} and press Y to continue: "
        )
        # if user doesn't press Y, program should warn that it is using the default fixture difficulty ratings
        if user_input.lower() != "y":
            warn(f"Using default fixture difficulty ratings!!")
    player_analytics = compute_player_analytics_for_next_n_gameweeks(
        players, current_gameweek, n=5
    )

    Display.display_player_analytics(player_analytics, TEAM_ID_TO_TEAM_NAME)

    print("displaying your currently selected players")
    # ask the user to ensure they player ids for their current team selection
    current_team_selection_player_ids_file_name = "current_team_selection_player_ids.json"
    input(
        f"Please ensure that you have updated {current_team_selection_player_ids_file_name}  press enter to continue: "
    )

    # read json from file named `current_team_selection_player_ids_file_name`
    with open(current_team_selection_player_ids_file_name, "r") as f:
        my_current_selected_players_ids = json.load(f)["player_ids"]

    sort_property_lambda = lambda player: player.predicted_points[0]

    Display.display_players_by_id(player_analytics, my_current_selected_players_ids, TEAM_ID_TO_TEAM_NAME, sort_property_lambda)


async def get_and_persist_fixture_difficulty_ratings(
    fpl_client: FPL, current_gameweek, n=DEFAULT_NUMBER_OF_GAMWEEKS_TO_PREDICT
):
    # TODO: IMPROVEMENT:  use a more sophisticated method of determining the fixture difficulty ratings
    """
    Gets the fixture difficulty ratings for the next n gameweeks
    Note that a gameweek can have >=1 fixtures
    """
    # get fixture difficulty ratings for the next n gameweeks
    fixture_difficulty_ratings_by_gameweek = {}

    # create task to get fixtures for gameweeks between current_gameweek and min(current_gameweek+n, 38)
    fixtures_tasks = []
    for gameweek in range(
        current_gameweek, min(current_gameweek + n, MAX_GAMEWEEKS + 1)
    ):
        fixtures_tasks.append(
            asyncio.create_task(fpl_client.get_fixtures_by_gameweek(gameweek))
        )

    # wait for all tasks to complete
    fixtures_by_gameweek = await asyncio.gather(*fixtures_tasks)

    # for each gameweek, get the fixture difficulty ratings
    for gameweek, fixtures in zip(
        range(current_gameweek, min(current_gameweek + n, MAX_GAMEWEEKS + 1)),
        fixtures_by_gameweek,
    ):
        fixture_difficulty_ratings_by_gameweek[gameweek] = {}
        # for each fixture, get the fixture difficulty rating
        for fixture in fixtures:
            home_team_name = TEAM_ID_TO_TEAM_NAME[fixture.team_h]
            away_team_name = TEAM_ID_TO_TEAM_NAME[fixture.team_a]
            difficulty_rating_for_home_team = fixture.team_h_difficulty
            difficulty_rating_for_away_team = fixture.team_a_difficulty

            fixture_difficulty_ratings_for_current_gameweek = (
                fixture_difficulty_ratings_by_gameweek[gameweek]
            )

            # add the fixture difficulty rating to the datastructure
            if home_team_name not in fixture_difficulty_ratings_for_current_gameweek:
                fixture_difficulty_ratings_for_current_gameweek[home_team_name] = {}
            if away_team_name not in fixture_difficulty_ratings_for_current_gameweek:
                fixture_difficulty_ratings_for_current_gameweek[away_team_name] = {}

            # raise warning if 2 teams appear to be playing each other twice in the same gameweek (it is possible but rare)
            if (
                away_team_name
                in fixture_difficulty_ratings_for_current_gameweek[home_team_name]
                or home_team_name
                in fixture_difficulty_ratings_for_current_gameweek[away_team_name]
            ):
                warn(
                    f"{home_team_name} is playing {away_team_name} twice in the same gameweek, verify this is correct"
                )
                # ask user to verify this is correct
                user_input = input("Is this correct? (Y/N): ")
                if user_input.lower() != "y":
                    raise ValueError(
                        f"{home_team_name} is playing {away_team_name} twice in the same gameweek, verify this is correct"
                    )

            fixture_difficulty_ratings_for_current_gameweek[home_team_name][
                away_team_name
            ] = difficulty_rating_for_home_team
            fixture_difficulty_ratings_for_current_gameweek[away_team_name][
                home_team_name
            ] = difficulty_rating_for_away_team

    # persist fixture_difficulty_ratings_by_gameweek to disk and override the existing file
    with open(FIXTURE_DIFFICULTY_RATINGS_FILEPATH, "w") as f:
        json.dump(fixture_difficulty_ratings_by_gameweek, f)
    return fixture_difficulty_ratings_by_gameweek


def convert_element_type_to_position(element_type: int) -> str:
    """
    The FPL API uses an integer (element_type) to represent the position of a player.
    """
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


class Display:
    @staticmethod
    def display_fixture_difficulty_ratings(fixture_difficulty_ratings_by_gameweek):
        # pretty print the dictionary fixture_difficulty_ratings_by_gameweek
        print("Fixture difficulty ratings by gameweek:")
        for (
            gameweek,
            fixture_difficulty_ratings,
        ) in fixture_difficulty_ratings_by_gameweek.items():
            print(f"Gameweek {gameweek}:")
            # pretty print fixture_difficulty_ratings for each team this gameweek in a table
            table = PrettyTable()
            table.field_names = ["Team", "Fixture Difficulty Rating"]
            for (
                team_name,
                fixture_difficulty_rating,
            ) in fixture_difficulty_ratings.items():
                table.add_row([team_name, fixture_difficulty_rating])
            print(table)

    @staticmethod
    def display_fixture_difficulty_ratings_using_the_fpl_FDR_function(
        fdrs: dict[str, dict[str, int]]
    ):
        # pretty print the fdrs
        fdr_table = PrettyTable()
        fdr_table.field_names = ["Team", "Opponent", "Difficulty Rating"]
        fdr_table.align["Team"] = "l"  # Left align team names
        fdr_table.align["Opponent"] = "l"  # Left align opponent names
        for team, opponents in fdrs.items():
            for opponent, difficulty_rating in opponents.items():
                fdr_table.add_row([team, opponent, difficulty_rating])
        print(fdr_table)

    # create a static method to display players whose id is in a set provided, and order by their score
           
    @staticmethod
    def display_players_by_id(
        player_analytics: list[PlayerData], player_ids: set[int], team_id_to_team_name: dict[int, str],
        get_player_property_to_sort_by: Callable[[PlayerData], Any]
    ):
        player_table = PrettyTable()
        player_table.field_names = [
            "Id",
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
            "PredictedPoints",
            "Score",
        ]
        player_table.align["Player"] = "l"

        player_analytics.sort(key=get_player_property_to_sort_by, reverse=True)

        # create deep copy of player_ids
        player_ids_copy = player_ids.copy()
        for player_data in player_analytics:
            if not player_ids_copy: # all players have been added
                break
            if player_data.fpl_player.id in player_ids_copy:
                player_table.add_row(
                    [
                        player_data.fpl_player.id,
                        player_data.name,
                        team_id_to_team_name[player_data.club_id],
                        player_data.position,
                        player_data.value,
                        player_data.form,
                        player_data.minutesPlayed,
                        player_data.goals,
                        player_data.assists,
                        player_data.bonus,
                        player_data.cleansheets,
                        player_data.avg_predicted_points,
                        player_data.predicted_points,
                        player_data.score,
                    ]
                )
                # remove player.id from player_ids_copy
                player_ids_copy.remove(player_data.fpl_player.id)
        print(player_table)

    @staticmethod
    def display_player_analytics(
        player_analytics: list[PlayerData], team_id_to_team_name: dict[int, str]
    ):
        player_table = PrettyTable()
        player_table.field_names = [
            "Id",
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
            "PredictedPoints",
            "Score",
        ]
        player_table.align["Player"] = "l"  # Left align player names

        # sort the players by their form
        player_analytics.sort(
            key=lambda player: player.avg_predicted_points * player.form, reverse=True
        )

        max_num_players_to_display = 50
        positions_to_display = {"GK", "DEF", "MID", "FWD"}
        player_id_filter = {}

        num_players_added_to_table = 0
        for player in player_analytics:
            # NEBUG if player.minutesPlayed < 900: continue # only show players who have played at least 900 minutes
            if num_players_added_to_table >= max_num_players_to_display:
                break
            else:
                if player.position not in positions_to_display:
                    continue
                if player_id_filter and player.fpl_player.id not in player_id_filter:
                    continue

            player_table.add_row(
                [
                    player.fpl_player.id,
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
                    player.predicted_points,
                    player.score,
                ]
            )
            num_players_added_to_table += 1

        print(player_table)


def compute_player_analytics_for_next_n_gameweeks(
    players: list[FPLPlayer], current_gameweek: int, n: int
) -> list[PlayerData]:
    """
    n: the number of gameweeks to predict points for
    """
    player_analytics = []

    for player in players:
        player_data = PlayerData(
            name=player.web_name,
            club_name=TEAM_ID_TO_TEAM_NAME[player.team],
            club_id=player.team,
            position=convert_element_type_to_position(player.element_type),
            value=player.now_cost / 10,
            form=player.form,
            minutesPlayed=player.minutes,
            goals=player.goals_scored,
            assists=player.assists,
            bonus=player.bonus,
            cleansheets=player.clean_sheets,
            start_gameweek=current_gameweek,
            number_of_gameweeks=n,
            fpl_player=player,
        )
        player_analytics.append(player_data)

    return player_analytics


if __name__ == "__main__":
    asyncio.run(main())
