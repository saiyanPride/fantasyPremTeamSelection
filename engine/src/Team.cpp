#include "Team.hpp"
#include "ProprietaryAlgorithms.hpp"
#include <vector>
#include <exception>
#include <iostream>
#include <memory>
#include "Chips.hpp"
using namespace ProprietaryAlgorithms;

void Team::updateTeam(){
    // TODO2 query database for current team
    // TODO2 define startingLineUp, substitutes & captains
    //each player's members fields must be initialised accurately!
};

Team::Team()
{
    updateTeam();
};

std::shared_ptr<Team::Changes> Team::suggestChanges()
{ //need to pass gameweeks from main
    bool aChipHasBeenUsed = false;

    std::shared_ptr<Team::Changes> suggestedChanges(nullptr);
    //determine the best chip to use to effect changes
    determineIfWildCardOrFreeHitShouldBeConsidered(*this);
    if (shouldConsiderWildCard && Chips::getChips().doesWildCardExist())
        aChipHasBeenUsed = attemptWildCard(*this, suggestedChanges);
    if (!aChipHasBeenUsed && shouldConsiderFreeHit && Chips::getChips().doesFreeHitExist())
        aChipHasBeenUsed = attemptFreeHit(*this, suggestedChanges);
    if (!aChipHasBeenUsed && Chips::getChips().getNoAvailableFreeTransfers() > 0)
        aChipHasBeenUsed = attemptFreeTransfers(suggestedChanges);
    /*TODO at this point if suggestedChanges holds a nullptr i.e. none of above operations provided a recommendation
    then make suggestedChanges hold the existing team so that decisions on the starting lineup, captaincy as well as the
    benchboost, and triplecaptain chips can be made
    
    if(!aChipHasBeenUsed){//existing team is being retained
        suggestedChanges.reset(...);//provide constructor that enambles explicit conversion
        of Team to changes object to facilitate

    }
    */
    setStartingLineUp(suggestedChanges);
    attemptBenchBoost(suggestedChanges);
    attemptTripleCaptain(suggestedChanges);
    if (suggestedChanges.get() == nullptr)
    {
        throw no_suggestions_exception();
    }
    return suggestedChanges;
};

const std::vector<Player> &Team::getStartingLineUp() const
{
    return startingLineUp;
};
const std::vector<Player> &Team::getSubstitutes() const
{
    return substitutes;
};

void Team::setShouldConsiderWildcard(bool value)
{
    shouldConsiderWildCard = value;
}
void Team::setShouldConsiderFreeHit(bool value)
{
    shouldConsiderFreeHit = value;
}

void Team::setCaptains(std::shared_ptr<Player> _captain, std::shared_ptr<Player> _viceCaptain)
{
    captain = _captain;
    viceCaptain = _viceCaptain;
}
uint8_t Team::getGameWeekNo() const
{
    return gameweekNo;
}

std::shared_ptr<Team::Changes> Team::getChanges(std::vector<Player> &_newTeam) const
{
    std::vector<Player> toSell;
    std::vector<Player> toBuy;

    //players in both current and new team are retained, those just in current team should be sold and those just in the new team should be bought
    //create hashtable of current team's players to track their frequency in current and new team lists
    std::unordered_map<Player, uint8_t> frequencyOfPlayersInCurrentTeam;
    for (auto currentPlayer : startingLineUp)
        frequencyOfPlayersInCurrentTeam.insert(std::make_pair(currentPlayer, 1));
    for (auto currentPlayer : substitutes)
        frequencyOfPlayersInCurrentTeam.insert(std::make_pair(currentPlayer, 1));
    /*traverse list of new teams and for each player in new list, check for hit in frequencyOfPlayersInCurrentTeam
        //if hit, then team member should be retained
        //else, then the team member is new (should be bought)
    */

    //determine players that need to sold and bought
    for (auto newPlayer : _newTeam)
    {
        if (frequencyOfPlayersInCurrentTeam.find(newPlayer) != frequencyOfPlayersInCurrentTeam.end())
        {                                                    //hit so player retained
            frequencyOfPlayersInCurrentTeam[newPlayer] += 1; //update frequency of retained player to enable distinction between current players that will be sold
        }
        else
        { //miss, so player needs to be bought
            toBuy.push_back(newPlayer);
        }
    }

    //traverse frequencyOfPlayersInCurrentTeam to determine players to sell
    for (auto playerFrequencyPair : frequencyOfPlayersInCurrentTeam)
    { //players in current team with frequency of 1 should be sold
        if (playerFrequencyPair.second == 1)
            toSell.push_back(playerFrequencyPair.first);
    }

    //players sold must match players bought
    if (toSell.size() != toBuy.size())
        throw transfer_imbalance_exception();

    std::shared_ptr<Changes> changes(new Changes(toSell, toBuy, _newTeam));
    return changes;
}

std::vector<Player> Team::getMergedTeamList() const
{ //TODO3: optimise so that this computation only happens once
    std::vector<Player> mergedTeamList(startingLineUp);
    mergedTeamList.insert(mergedTeamList.end(), substitutes.begin(), substitutes.end());
    return mergedTeamList;
}

void Team::Changes::setSuggestedStartingLineUp(std::vector<Player> &_suggestedStartingLineUp)
{
    suggestedStartingLineUp = _suggestedStartingLineUp;
}
void Team::Changes::setSuggestedSubstitutes(std::vector<Player> &_suggestedSubstitutes)
{
    suggestedSubstitutes = _suggestedSubstitutes;
}

void Team::Changes::setCaptains()
{
    if (suggestedStartingLineUp.size() != STARTING_LINE_UP_SIZE)
    {
        throw starting_lineup_size_exception("In order to reccomend captain and vice captain, the starting line up selection must be complete");
    }
    captain = &suggestedStartingLineUp[0];     //player with highest score
    viceCaptain = &suggestedStartingLineUp[1]; //player with second highest score
}

Team::Changes::~Changes()
{
    if (captain != nullptr)
        delete captain;
    if (viceCaptain != nullptr)
        delete viceCaptain;
}

std::size_t Team::Changes::getNoChanges() const
{
    if (toSell.size() == toBuy.size())
        return toSell.size();
    else
        throw transfer_imbalance_exception();
}

Player Team::Changes::getCaptain()
{
    if (captain!=nullptr) return *captain;
    else throw miscellaneous_exception("You don't have a captain");
}

Player Team::Changes::getViceCaptain()
{
    if (viceCaptain!=nullptr) return *viceCaptain;
    else throw miscellaneous_exception("You don't have a vice captain");
}
std::vector<Player> Team::Changes::getSuggestedSubstitutes()
{
    return suggestedSubstitutes;
}
std::vector<Player> Team::Changes::getSuggestedStartingLineUp(){
    return suggestedStartingLineUp;
}

void Team::Changes::recommendTripleCaptain(){
    useTripleCaptain=true;
}
void Team::Changes::recommendBenchBoost(){
    useBenchBoost=true;
}      

const bool Team::Changes::isBenchBoostRecommended() const{
    return useBenchBoost;
}

const bool Team::Changes::isTripleCaptainRecommended() const{
    return useTripleCaptain;
}