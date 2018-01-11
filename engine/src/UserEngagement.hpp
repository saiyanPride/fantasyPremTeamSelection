#ifndef FANTASY_USER_ENGAGEMENT
#define FANTASY_USER_ENGAGEMENT
#include <memory>
#include <iostream>
#include "Team.hpp"
#include "Chips.hpp"
#include "Player.hpp"
namespace fantasypremierleague{
    void displaySuggestedTeamChanges(std::shared_ptr<Team::Changes> suggestedTeamChanges);
    bool shouldImplementTeamChanges();
    void implementTeamChanges(std::shared_ptr<Team::Changes> suggestedTeamChanges);
    void verifyGameWeekDifficultyUpdate();// verifies that user's view of upcoming match results 
                                          // has been expressed in the database gameweek difficulty data
}//!fantasypremierleague
#endif