#ifndef FANTASY_TEAM
#define FANTASY_TEAM
#include <vector>
#include <memory>
#include <unordered_map>
#include <utility>
#include <algorithm>
#include "Player.hpp"
#include "FantasyExceptions.hpp"
namespace fantasypremierleague
{
class Team
{
  std::vector<Player> startingLineUp;
  std::vector<Player> substitutes;
  std::shared_ptr<Player> captain, viceCaptain;
  bool shouldConsiderWildCard = false, shouldConsiderFreeHit = false;
  uint8_t gameweekNum;

public:
  class Changes;
  Team();
  std::shared_ptr<Changes> suggestChanges(); // recommends transfers and chips to play
  void updateTeam();                         // ensures current startingLineUp & substitutes are up to date
  const std::vector<Player> &getStartingLineUp() const;
  const std::vector<Player> &getSubstitutes() const;
  uint8_t getGameWeekNum() const;
  void setShouldConsiderWildcard(bool);
  void setShouldConsiderFreeHit(bool);
  void setCaptains(const std::shared_ptr<Player> &_captain, const std::shared_ptr<Player> &_viceCaptain);
  std::shared_ptr<Changes> getChangesRequiredToFormNewTeam(std::vector<Player> &newTeam) const; // determines changes required to convert existing team to `newTeam`
  std::vector<Player> getMergedTeamList() const;
};

class Team::Changes
{
  std::vector<Player> suggestedStartingLineUp; //TODO: must be sorted by score in descending order, ensure unit test captures this
  std::vector<Player> suggestedSubstitutes;    //TODO: must be sorted by score in descending order ensure unit test captures this
  Player *captain, *viceCaptain;
  bool useTripleCaptain, useBenchBoost;

public:
  const std::vector<Player> toSell;
  const std::vector<Player> toBuy;
  const std::vector<Player> newTeam;
  Changes() = delete;
  Changes(std::vector<Player> &_toSell, std::vector<Player> &_toBuy, std::vector<Player> &_newTeam) : toSell(_toSell), toBuy(_toBuy), newTeam(_newTeam), captain(nullptr), viceCaptain(nullptr),
                                                                                                      useTripleCaptain(false), useBenchBoost(false){};
  ~Changes();
  void setSuggestedStartingLineUp(std::vector<Player> &);
  void setSuggestedSubstitutes(std::vector<Player> &);
  void setCaptains();
  Player getCaptain();
  Player getViceCaptain();
  std::vector<Player> &getSuggestedSubstitutes();
  std::vector<Player> &getSuggestedStartingLineUp();
  std::size_t getNumChanges() const;
  void recommendTripleCaptain();
  void recommendBenchBoost();
  bool isBenchBoostRecommended() const;
  bool isTripleCaptainRecommended() const;
};
} // !namespace fantasypremierleague
#endif