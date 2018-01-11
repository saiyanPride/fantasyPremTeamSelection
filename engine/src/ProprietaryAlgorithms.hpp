#ifndef FANTASY_ALGO
#define FANTASY_ALGO
#include <cstdint>
#include <cppconn/driver.h>
#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>
#include <memory>
#include <numeric>
#include <vector>
#include <stack>
#include <stdexcept>
#include <iostream>
#include <utility>
#include "Team.hpp"
#include "Settings.hpp"
#include "Chips.hpp"
#include "FantasyExceptions.hpp"
#include "mysql_connection.h"
#include "mysql_connection.h"

namespace fantasypremierleague
{
void determineIfWildCardOrFreeHitShouldBeConsidered(Team &currentTeam);
bool improvedTeamFoundWithWildCard(const Team &currentTeam, std::shared_ptr<Team::Changes>);
bool improvedTeamFoundWithFreeHit(const Team &currentTeam, std::shared_ptr<Team::Changes>);
bool improvedTeamFoundWithFreeTransfers(std::shared_ptr<Team::Changes>);
bool attemptTeamImprovement(int8_t minNoTransfers, int8_t maxNoTransfers, std::shared_ptr<Team::Changes>, uint8_t noGameWeeksToConsider = NO_FUTURE_GAMEWEEKS_TO_CONSIDER);
bool attemptSquadOverhaul(const Team &currentTeam, std::shared_ptr<Team::Changes> suggestedChanges, uint8_t noFutureGameWeeksToConsider = 0);
void recommendBenchBoostIfWorthwhile(std::shared_ptr<Team::Changes> suggestedChanges); // evaluates the worthwhileness of using the bench boost chip & updates `suggestedChanges` to reflect this opinion
void recommendTripleCaptainIfWorthwhile(std::shared_ptr<Team::Changes> suggestedChanges);
void setStartingLineUp(std::shared_ptr<Team::Changes> suggestedChanges);
std::vector<Player> getTopPlayersWithinBudget(uint8_t desiredNoPlayers, const std::vector<Player> &playerListDesc, float budgetLeft); // extracts the top `desiredNoPlayers` from playerListDesc whose total value <= `budgetLeft`

// The `DataRetriever` class is used to query the current datasource (e.g. database) for player related analytics which informs decision-making
class DataRetriever
{
  DataRetriever();
  sql::Driver *driver;
  std::unique_ptr<sql::Connection> connection;
  std::shared_ptr<sql::Statement> statement;

public:
  static DataRetriever &getDataRetriever();
  std::vector<Player> getPlayersByScoreDesc(uint8_t startGameWeekNo, uint8_t endGameWeekNo, PlayerPostion);
  float getPlayersAverageScoreForPeriod(std::vector<Player> playerList, uint8_t startGameWeekNo, uint8_t endGameWeekNo);
  std::shared_ptr<std::vector<Player>> getBestPlayersInPosition(std::string position, bool isDescendingOrder);
  std::shared_ptr<std::vector<Player>> getBestPlayersOverall(uint16_t noPlayers);
  std::shared_ptr<std::vector<Player>> getPlayersMatchingQuery(std::string query);
  void displayAnalytics(Team &);
  std::shared_ptr<sql::Statement> &getStatement();
};
} //!namespace fantasypremierleague
#endif

