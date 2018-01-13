#ifndef FANTASY_CHIPS
#define FANTASY_CHIPS

#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <exception>
#include <unordered_map>
#include <memory>
#include <algorithm>
#include "Settings.hpp"
#include "FantasyExceptions.hpp"
#include "Logger.hpp"
namespace fantasypremierleague
{
// Chips enable users to perform actions not normally available
// These new actions can significantly boost the user's points tally during a gameweek
// For example the wildcard chip when available, can be used to make unlimited changes to one's team without any point deductions
// See https://fantasy.premierleague.com/help/ for more information
// The `Chips` class stores data pertaining to the availability of chips to the user
class Chips
{
    static std::shared_ptr<Chips> myChips; //singleton
    int8_t noFreeTransfers = 0;
    bool wildCardExists = false, freeHitExists = false, tripleCaptainExists = false, benchBoostExists = false;

    Chips();
    void update();

  public:
    int8_t getNoAvailableFreeTransfers() const;
    bool doesWildCardChipExist() const;
    bool doesFreeHitChipExist() const;
    bool doesTripleCaptainChipExist() const;
    bool doesBenchBoostChipExist() const;
    void displayChips() const;
    static std::shared_ptr<Chips> &getChips(); //returns the singleton Chips obect
};
} //!namespace fantasypremierleague
#endif
