#include <memory>
#include <iostream>
#include "Team.hpp"
#include "Chips.hpp"
#include "Player.hpp"
#include "UserEngagement.hpp"

int main()
{
    using namespace fantasypremierleague;
    //TODO (low priority) conditionally update databse with player analytics based on user argument
    std::unique_ptr<Chips> &myChipsPtr = Chips::getChips();
    try
    {
        verifyGameWeekDifficultyUpdate();
        Team myTeam; //create a Team object with your current team (starting lineup, substitutes etc)
        std::shared_ptr<Team::Changes> suggestedTeamChanges = myTeam.suggestChanges();
        displaySuggestedTeamChanges(suggestedTeamChanges);
        if (shouldImplementTeamChanges())
            implementTeamChanges(suggestedTeamChanges);
    }
    catch (no_suggestions_exception e)
    {
        std::cout << e.what() << std::endl;
    }
    catch (miscellaneous_exception e)
    {
        std::cout << e.what() << std::endl;
    }
    return 0;
}
