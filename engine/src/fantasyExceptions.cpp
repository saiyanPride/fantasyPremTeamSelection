#include "fantasyExceptions.hpp"
const char * insufficient_budget_exception::what() const _NOEXCEPT
{
    return "impossible to get players with given budget";
}


const char * transfer_imbalance_exception::what() const _NOEXCEPT
{
    return "The number of players to be sold must equal the number of players to be bought";
}

const char * no_suggestions_exception::what() const _NOEXCEPT
{
    return "No suggestions being recommended";
}

const char * starting_lineup_size_exception::what() const _NOEXCEPT
{
    return msg;
}

starting_lineup_size_exception::starting_lineup_size_exception(const char * _msg):msg(_msg){};

const char * miscellaneous_exception::what() const _NOEXCEPT
{
    return msg;
}

miscellaneous_exception::miscellaneous_exception(const char * _msg):msg(_msg){};


