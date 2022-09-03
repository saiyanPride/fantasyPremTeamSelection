#pragma once
#include <unordered_map>
#include "Player.hpp"
#include "Settings.hpp"
using std::string;
using std::vector;

namespace fantasypremierleague
{

using Players = vector<Player>;
using PotentialSquad = vector<Player>;
using PlayersByPosition = std::unordered_map<PlayerPostion,Players>;//TODO: create hash for enum as key or mapenums to string or ints
using  GoalkeeperPairs = vector< std::pair<Player,Player> >;

struct Constraints{
    const float budget;
    const int numFreeTransfers;
    const int gameWeekHorizon;//numGameWeeksToConsider
    const int costPerNonFreeTransfer; // default value in settings which is -4
};

//TODO: define this class somewhere FPLAnalytics
/*
result is of form {
    "FORWARD" : {},
    "MIDFIELDER" : {},
    "DEFENDER" : {},
    "GOALKEEPER" : {}
}
*/

class FPLAnalytics;
PotentialSquad chooseTopNSquads(const Constraints& constraints, const int n);

vector<PotentialSquad> generateTeamsThatSatisfyBudgetConstraints(const Constraints& constraints,  const PlayersByPosition& outfieldPlayerOptions, const GoalkeeperPairs& goalkeeperOptions);

void generateTeamsThatSatisfyBudgetConstraints(vector<PotentialSquad>& results, PotentialSquad& playersChosenSoFar, const float budget, const PlayersByPosition& outfieldPlayerOptions, const GoalkeeperPairs& goalkeeperOptions,
 std::unordered_map<PlayerPostion, int>& nextPlayerToConsiderIndexByPosition);

/*

gameWeekHorizon: numberOfGameWeeks to consider

This should filter out squads that can't be achieved via numberOfAvailableFreeTransfers and any other relevant constraint
*/
vector<PotentialSquad> filterForViableSquads(vector<PotentialSquad>& squads, const Constraints& constraints);


/*

//TODO: implementation
once all potential squads have been ranked
for each one we determine the number of free transfers needed to achieve, if value <= available free transfers => include in result
*/
vector<PotentialSquad> getAttainableSquadsByNumberOfFreeTransfers(vector<PotentialSquad>& squads, const Constraints& constraints);

};// ! namespace fantasypremierleague