#include "Settings.hpp"
namespace fantasypremierleague
{
extern const uint8_t NO_FUTURE_GAMEWEEKS_TO_CONSIDER = 4;
extern const uint16_t GAMEWEEK_TEAM_SCORE_THRESHOLD = 1050;
extern const uint8_t BENCH_BOOST_SCORE_THRESHOLD = 240;
extern const uint8_t TRIPLE_CAPTAIN_SCORE_THRESHOLD = 85;
extern const uint16_t FREEHIT_GAMEWEEK_TEAM_SCORE_THRESHOLD = 800;
extern const uint8_t TEAM_SIZE = 15;
extern const uint8_t REQUIRED_NO_FORWARDS = 3;
extern const uint8_t REQUIRED_NO_MIDFIELDER = 5;
extern const uint8_t REQUIRED_NO_DEFENDERS = 5;
extern const uint8_t REQUIRED_NO_GOALKEEPERS = 2;
extern const uint8_t STARTING_LINE_UP_SIZE = 11;
extern const uint8_t MINIMUM_NO_CHANGES_REQUIRED_WITH_WILDCARD = 2;
extern const uint8_t MINIMUM_NO_CHANGES_REQUIRED_WITH_FREEHIT = 2;
extern const float FORWARD_BUDGET = 25.5;
extern const float MIDFIELD_BUDGET = 30;
extern const float DEFENCE_BUDGET = 33.5;
extern const float GOALKEEPER_BUDGET = 11;
extern const std::string STATUS_FILE_PATH = "../../dataRetriever/dataFiles/status.json";

PlayerPostion getPositionEnum(std::string &playerPosition)
{
    PlayerPostion result;
    if (playerPosition.compare("FWD") == 0)
    {
        result = PlayerPostion::FORWARD;
    }
    else if (playerPosition.compare("MID") == 0)
    {
        result = PlayerPostion::MIDFIELDER;
    }
    else if (playerPosition.compare("DEF") == 0)
    {
        result = PlayerPostion::DEFENDER;
    }
    else
    {
        result = PlayerPostion::GOALKEEPER;
    }
    return result;
}
} //!namespace fantasypremierleague