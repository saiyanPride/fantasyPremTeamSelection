#ifndef FANTASY_CHIPS
#define FANTASY_CHIPS

#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <exception>
#include <map>
#include <memory>
#include "fantasyExceptions.hpp"
namespace FantasyPremTeamSelection{
class Chips{//chips are used to make changes to one's team
    static std::unique_ptr<Chips> myChips;      
    int8_t noFreeTransfers=0;
    bool wildCardExists=false,freeHitExists=false;
    bool tripleCaptainExists=false, benchBoostExists=false;

    Chips();
    void update();
    public:
    int8_t getNoAvailableFreeTransfers() const;
    bool doesWildCardExist() const;
    bool doesFreeHitExist() const;
    bool doesTripleCaptainExist() const;
    bool doesBenchBoostExist() const;
    void displayChips() const;
    static std::unique_ptr<Chips>& getChips();      
};//class Chips
}//!namespace FantasyPremTeamSelection
#endif
