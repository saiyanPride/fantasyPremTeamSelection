#include "Team.hpp"
#include "ProprietaryAlgorithms.hpp"
#include <vector>
#include <exception>
#include <iostream>
#include <memory>
#include "Chips.hpp"
#include "mysql_connection.h"
#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>
using namespace ProprietaryAlgorithms;


Team::Team()
{
    updateTeam();
};

/*
- Retrieves current team (starters & substitutes) from datastore and updates corresponding data members
- Captain & vice captain are intentionally not retrieved, as recommendation algo will suggest best 
choices for these roles whether transfers are suggested or not
*/
void Team::updateTeam(){
    // TODO(high priority) query database for current team
    //query database for current team players 
    const char *currentPlayersSql = "SELECT Club, Name, Position, FirstGameweekScore, AvgScore FROM PlayerStats WHERE isFirstTeam > 0 ORDER BY AvgScore DESC";
    try {
        sql::Driver *driver;
        sql::Connection *con;
        sql::Statement *stmt;
        sql::ResultSet *res;
        std::string password;

        /* Create a connection */
        driver = get_driver_instance(); 
        std::cout<<"[PROMPT] Please enter your database password"<<std::endl;     
        std::cin>>password;
        con = driver->connect("tcp://localhost:3306", "fantasydev", password);
        con->setSchema("fantasyPremierLeague");//USE fantasy database
        stmt = con->createStatement();
        res = stmt->executeQuery("SELECT * FROM PlayerStats WHERE isFirstTeam > 0 ORDER BY AvgScore DESC");
        while (res->next()) {//TODO create player objects and store in appropriate member list based on player being starter/sub
            //TODO use enums for db column names!!
            std::cout << res->getString("Club");
            std::cout << res->getString("Name");
            std::cout << res->getString("Position");
            std::cout << res->getDouble("Value") << std::endl;
        }
        delete res;
        delete stmt;
        delete con;

        } catch (sql::SQLException &e) {
        std::cout << "[ERROR]: SQLException in " << __FILE__;
        std::cout << "[ERROR] " << e.what();
        std::cout << "[ERROR] (MySQL error code: " << e.getErrorCode();
        std::cout << ", SQLState: " << e.getSQLState() << " )" << std::endl;
        }
    // TODO(high priority) define startingLineUp, substitutes
    //instantiate Player objects & group starters separately from substitutes
    //each player's object member fields must be initialised accurately!
};

std::shared_ptr<Team::Changes> Team::suggestChanges()
{ //need to pass gameweeks from main
    bool aChipHasBeenUsed = false;
    std::unique_ptr<Chips>& myChips = Chips::getChips();
    std::shared_ptr<Team::Changes> suggestedChanges(nullptr);
    //determine the best chip to use to effect changes
    determineIfWildCardOrFreeHitShouldBeConsidered(*this);
    if (shouldConsiderWildCard && myChips->doesWildCardExist())
        aChipHasBeenUsed = attemptWildCard(*this, suggestedChanges);
    if (!aChipHasBeenUsed && shouldConsiderFreeHit && myChips->doesFreeHitExist())
        aChipHasBeenUsed = attemptFreeHit(*this, suggestedChanges);
    if (!aChipHasBeenUsed && myChips->getNoAvailableFreeTransfers() > 0)
        aChipHasBeenUsed = attemptFreeTransfers(suggestedChanges);
    /*TODO(high priority) at this point if suggestedChanges holds a nullptr i.e. none of above operations provided a recommendation
    then make suggestedChanges hold the existing team so that decisions on the starting lineup, captaincy as well as the
    benchboost, and triplecaptain chips can be made
    
    if(!aChipHasBeenUsed){//existing team is being retained
        suggestedChanges.reset(...);//provide constructor that enables explicit conversion
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
{ //TODO(low priority): optimise so that this computation only happens once
    //i.e. make mergedTeamList an instance member than can be updated if the team changes
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