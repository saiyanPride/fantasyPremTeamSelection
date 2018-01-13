#include "catch.hpp"
#include "Team.hpp"
#include <algorithm>
using namespace fantasypremierleague;
Team myTeam; // impliclty updates the team (populates starting lineup & substitutes from datasource)

TEST_CASE("whenCurrentTeamIsRetrievedStartingLineUpHas11Players")
{
    REQUIRE(myTeam.getStartingLineUp().size() == 11);
};

TEST_CASE("checkThatThereAre4Substitues")
{
    REQUIRE(myTeam.getSubstitutes().size() == 4);
}

TEST_CASE("whenTeamIsUpdatedTwiceStartingLineupHas11Players")
{
    myTeam.updateTeam();
    REQUIRE(myTeam.getStartingLineUp().size() == 11);
}

TEST_CASE("whenTeamIsUpdatedTwiceSubstitutesListHas4Players")
{
    myTeam.updateTeam();
    REQUIRE(myTeam.getSubstitutes().size() == 4);
}

TEST_CASE("whenStartingLineUpandSubstitutesAreMergedPlayersAreSortedByAverageScore")
{
    const auto &mergedTeamList = myTeam.getMergedTeamList();
    auto sortPredicate = [](const Player &a, const Player &b) {
        return a.getAvgFutureScore() > b.getAvgFutureScore();
    };
    bool isMergedListInRightOrder = std::is_sorted(mergedTeamList.begin(), mergedTeamList.end(), sortPredicate);
    REQUIRE(isMergedListInRightOrder);
}
