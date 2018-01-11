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

namespace fantasypremierleague{
  void determineIfWildCardOrFreeHitShouldBeConsidered(Team& currentTeam);
  bool attemptWildCard(const Team &currentTeam, std::shared_ptr<Team::Changes>);
  bool attemptFreeHit(const Team &currentTeam, std::shared_ptr<Team::Changes>);
  bool attemptFreeTransfers(std::shared_ptr<Team::Changes>);
  bool attemptTeamImprovement(int8_t minNoTransfers, int8_t maxNoTransfers,std::shared_ptr<Team::Changes>, uint8_t noGameWeeksToConsider = NO_FUTURE_GAMEWEEKS_TO_CONSIDER);
  bool attemptSquadOverhaul(const Team &currentTeam, std::shared_ptr<Team::Changes> suggestedChanges, uint8_t noFutureGameWeeksToConsider=0);
  void attemptBenchBoost(std::shared_ptr<Team::Changes> suggestedChanges);  
  void attemptTripleCaptain(std::shared_ptr<Team::Changes> suggestedChanges);
  void setStartingLineUp(std::shared_ptr<Team::Changes> suggestedChanges);
  std::vector<Player> getTopPlayersWithinBudget(uint8_t desiredNoPlayers, const std::vector<Player> &playerListDesc, float budgetLeft);

  class DataRetriever
  {
      DataRetriever();
      sql::Driver *driver;
      std::unique_ptr<sql::Connection> con;
      std::unique_ptr<sql::Statement> stmt;

    public:
      static DataRetriever& getDataRetriever();
      std::vector<Player> getPlayersByScoreDesc(uint8_t startGameWeekNo, uint8_t endGameWeekNo, PlayerPostion);
      float getPlayersAverageScoreForPeriod(std::vector<Player> playerList,uint8_t startGameWeekNo, uint8_t endGameWeekNo);
      std::shared_ptr<std::vector<Player>> getBestPlayersInPosition(std::string position, bool isDescendingOrder);
      std::shared_ptr<std::vector<Player>> getBestNPlayersOverall(uint16_t noPlayers);
      std::shared_ptr< std::vector<Player> > getPlayersMatchingQuery(std::string query);
      void displayAnalytics(Team&);
      std::unique_ptr<sql::Statement>& getStatement();
  };
}//!namespace fantasypremierleague
#endif

/*
//Context: objective is to make 1 improvement
  //determine best 10 outfield players

  query existing ds

  //get best strikers
  "SELECT * FROM PlayerStats WHERE Position='FWD' ORDER BY AvgScore DESC"

  //get best midfielders
"SELECT * FROM PlayerStats WHERE Position='MID' ORDER BY AvgScore DESC"

  //get best defenders
"SELECT * FROM PlayerStats WHERE Position='DEF' ORDER BY AvgScore DESC"

  //get best goalkeepers
"SELECT Name, Value, Form , Bonus, Cleansheets, AvgScore FROM PlayerStats WHERE Position='GKP' ORDER BY AvgScore DESC"



  //of the worst 4, highlight the best replacements for each of them then recommend the best transfer
  loop through sorted list of player in same position & stop when bank balance + sale revenue can buy a player in the list that is not the player & is better

//print the top 10 players in each position (incl goalkeeper),


//list the top 5 best players overall (captaincy candidates)

SELECT * FROM PlayerStats ORDER BY AvgScore DESC limit 5



*/