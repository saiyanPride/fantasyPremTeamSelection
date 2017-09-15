#ifndef FANTASY_ALGO
#define FANTASY_ALGO
#include <cstdint>
#include "Team.hpp"
#include "Settings.hpp"
#include "Chips.hpp"
#include <memory>
#include <numeric>
#include <vector>
#include <stack>
#include <stdexcept>
#include <iostream>
#include <utility>
#include "fantasyExceptions.hpp"
namespace ProprietaryAlgorithms
{
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

  public:
    static DataRetriever getDataRetriever();
    std::vector<Player> getPlayersByScoreDesc(uint8_t startGameWeekNo, uint8_t endGameWeekNo, PlayerPostion);
    float getPlayersAverageScoreForPeriod(std::vector<Player> playerList,uint8_t startGameWeekNo, uint8_t endGameWeekNo);
};
}
#endif

