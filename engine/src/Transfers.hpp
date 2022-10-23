#pragma once
#include <unordered_map>
#include "Player.hpp"
#include "Settings.hpp"
#include "Team.hpp"
using std::string;
using std::vector;

//TODO: make all sure all new code compiles
//TODO: start using the new functions
//TODO: add integration tests
//TODO: extend/optimise over time as needed
//TODO: add linter
namespace fantasypremierleague
{

using Players = vector<Player>;
using PotentialSquad = vector<Player>;
using PlayersByPosition = std::unordered_map<PlayerPostion,Players>;//TODO:[required?] create hash for enum as key or mapenums to string or ints
using  GoalkeeperPairs = vector< std::pair<Player,Player> >;

struct Constraints{
    const float budget;
    const int numFreeTransfers;
    const int gameWeekHorizon;//numGameWeeksToConsider
    const int costPerNonFreeTransfer; // default value in settings which is -4
};

vector<PotentialSquad> chooseTopNSquads(const Constraints& constraints, const int n, Team &currentTeam);

vector<PotentialSquad> generateTeamsThatSatisfyBudgetConstraints(const Constraints& constraints,  const PlayersByPosition& outfieldPlayerOptions, const GoalkeeperPairs& goalkeeperOptions);

void generateTeamsThatSatisfyBudgetConstraints(vector<PotentialSquad>& results, PotentialSquad& playersChosenSoFar, const float budget, const PlayersByPosition& outfieldPlayerOptions, const GoalkeeperPairs& goalkeeperOptions,
 std::unordered_map<PlayerPostion, int>& nextPlayerToConsiderIndexByPosition);

vector<PotentialSquad> getTopNSquads(const vector<PotentialSquad>& candidateSquads, const int n, Team &currentTeam, const Constraints& constraints);
}//!namespace fantasypremierleague