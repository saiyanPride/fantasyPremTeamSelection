#ifndef FANTASY_SETTINGS
#define FANTASY_SETTINGS
#include <unordered_map>
#include <cstdint>
#include <array> 
#include <string> 

namespace FantasyPremTeamSelection{
//TODO(low priority): consider making enum have external linkage?

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
    MINREQUIRED_FORWARDS_IN_STARTING_LINEUP=1,
    MINREQUIRED_MIDFIELDERS_IN_STARTING_LINEUP=2,
    MINREQUIRED_DEFENDERS_IN_STARTING_LINEUP=3,
    MINREQUIRED_GOALKEEPERS_IN_STARTING_LINEUP=1
};

extern const uint8_t NO_FUTURE_GAMEWEEKS_TO_CONSIDER; //no of other gameweeks apart from the current one to be considered
extern const uint16_t GAMEWEEK_TEAM_SCORE_THRESHOLD;
extern const uint8_t BENCH_BOOST_SCORE_THRESHOLD;
extern const uint8_t TRIPLE_CAPTAIN_SCORE_THRESHOLD;
extern const uint16_t FREEHIT_GAMEWEEK_TEAM_SCORE_THRESHOLD;
extern const uint8_t TEAM_SIZE;
extern const uint8_t REQUIRED_NO_FORWARDS;
extern const uint8_t REQUIRED_NO_MIDFIELDER;
extern const uint8_t REQUIRED_NO_DEFENDERS;
extern const uint8_t REQUIRED_NO_GOALKEEPERS;
extern const uint8_t MINIMUM_NO_CHANGES_REQUIRED_WITH_WILDCARD;
extern const uint8_t MINIMUM_NO_CHANGES_REQUIRED_WITH_FREEHIT;
extern const uint8_t STARTING_LINE_UP_SIZE;
extern const float FORWARD_BUDGET;
extern const float MIDFIELD_BUDGET;
extern const float DEFENCE_BUDGET;
extern const float GOALKEEPER_BUDGET;


extern PlayerPostion getPositionEnum(std::string& playerPosition);
}//!namespace FantasyPremTeamSelection
#endif