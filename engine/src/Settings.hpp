#ifndef FANTASY_SETTINGS
#define FANTASY_SETTINGS
#include <unordered_map>
#include <cstdint>
#include <array>
#include <string>
// See https://fantasy.premierleague.com/help/ for fantasy premier league rules if any term used is unclear
namespace fantasypremierleague
{

enum class Club
{
    ARSENAL,
    CHELSEA,
    BOURNEMOUTH,
    BRIGHTON,
    BURNLEY,
    CRYSTAL_PALACE,
    EVERTON,
    HUDDERSFIELD,
    LEICESTER,
    LIVERPOOL,
    MANUTD,
    MANCHESTER_CITY,
    NEWCASTLE,
    SOUTHAMPTON,
    SPURS,
    STOKE,
    SWANSEA,
    WATFORD,
    WESTBROM,
    WESTHAM
};

enum class TRANSFER_ACTIONS
{
    BUY,
    SELL
};

enum class PlayerPostion
{
    FORWARD,
    MIDFIELDER,
    DEFENDER,
    GOALKEEPER
};

enum MinRequiredPlayersByPostion
{
    MINREQUIRED_FORWARDS_IN_STARTING_LINEUP = 1,
    MINREQUIRED_MIDFIELDERS_IN_STARTING_LINEUP = 2,
    MINREQUIRED_DEFENDERS_IN_STARTING_LINEUP = 3,
    MINREQUIRED_GOALKEEPERS_IN_STARTING_LINEUP = 1
};

extern const uint8_t NO_FUTURE_GAMEWEEKS_TO_CONSIDER;        // the number of other gameweeks apart from the current one to be considered
extern const uint16_t GAMEWEEK_TEAM_SCORE_THRESHOLD;         // an estimated starting lineup gameweek score below this value is considered low
extern const uint8_t BENCH_BOOST_SCORE_THRESHOLD;            // If the total score for substitutes is at least this value, the bench is considered strong
extern const uint8_t TRIPLE_CAPTAIN_SCORE_THRESHOLD;         // an individual player whose score is at least equal to this threshold, is considered a good candidate for the triple captain chip
extern const uint16_t FREEHIT_GAMEWEEK_TEAM_SCORE_THRESHOLD; // algo will consider using the freehit chip if the estimated gameweek score is less than this value
extern const uint8_t TEAM_SIZE;                              //
extern const uint8_t REQUIRED_NO_FORWARDS;
extern const uint8_t REQUIRED_NO_MIDFIELDER;
extern const uint8_t REQUIRED_NO_DEFENDERS;
extern const uint8_t REQUIRED_NO_GOALKEEPERS;
extern const uint8_t MINIMUM_NO_CHANGES_REQUIRED_WITH_WILDCARD;
extern const uint8_t MINIMUM_NO_CHANGES_REQUIRED_WITH_FREEHIT;
extern const uint8_t MAX_NUMBER_OF_BETTER_SQUADS_TO_CONSIDER_DURING_OVERHAULS;
extern const uint8_t STARTING_LINE_UP_SIZE;
extern const float FORWARD_BUDGET; // max budget for forwards
extern const float MIDFIELD_BUDGET;
extern const float DEFENCE_BUDGET;
extern const float GOALKEEPER_BUDGET; 
extern const std::string STATUS_FILE_PATH;

PlayerPostion getPositionEnum(std::string &playerPosition);
} //!namespace fantasypremierleague
#endif