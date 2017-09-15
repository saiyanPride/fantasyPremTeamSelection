#include "catch.hpp"
#include "Team.hpp"

TEST_CASE("whenCurrentTeamIsRetrievedStartingLineUpHas11Players"){
    Team myTeam;
    myTeam.updateTeam();
    REQUIRE(myTeam.getStartingLineUp().size()==11);
};

TEST_CASE("checkThatThereAre4Substitues"){
    Team myTeam;
    myTeam.updateTeam();
    REQUIRE(myTeam.getSubstitutes().size()==4);
}