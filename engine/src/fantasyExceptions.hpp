#ifndef FANTASY_EXCEPTIONS
#define FANTASY_EXCEPTIONS
#include <exception>
namespace FantasyPremTeamSelection{
class insufficient_budget_exception : public std::exception
{
    public:
    const char *what() const _NOEXCEPT;
};

class transfer_imbalance_exception : public std::exception
{
    public:
    const char *what() const _NOEXCEPT;
};

class no_suggestions_exception : public std::exception
{
    public:
    const char *what() const _NOEXCEPT;
};

class starting_lineup_size_exception : public std::exception
{
    const char * msg;
    public:
    starting_lineup_size_exception(const char * _msg);
    const char *what() const _NOEXCEPT;
};

class miscellaneous_exception : public std::exception
{
    const char * msg;
    public:
    miscellaneous_exception(const char * _msg);
    const char *what() const _NOEXCEPT;
};
}//!namespace FantasyPremTeamSelection
#endif