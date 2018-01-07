#ifndef FANTASY_TEAM
#define FANTASY_TEAM
#include <vector>
#include <memory>
#include <unordered_map>
#include <utility>
#include <algorithm>
#include "Player.hpp"
#include "fantasyExceptions.hpp"
namespace FantasyPremTeamSelection{
class Team{
    
    std::vector<Player> startingLineUp;
    std::vector<Player> substitutes;
    std::shared_ptr<Player> captain,viceCaptain;
    bool shouldConsiderWildCard=false,shouldConsiderFreeHit=false;
    uint8_t gameweekNo;
    
    public:
     class Changes;
     Team();
     std::shared_ptr<Changes> suggestChanges();
     void updateTeam();
     const std::vector<Player>& getStartingLineUp() const;
     const std::vector<Player>& getSubstitutes() const;
     uint8_t getGameWeekNo() const;
     void setShouldConsiderWildcard(bool);
     void setShouldConsiderFreeHit(bool);
     void setCaptains(std::shared_ptr<Player> _captain,std::shared_ptr<Player> _viceCaptain);
     std::shared_ptr<Changes> getChanges(std::vector<Player>& _newTeam) const;
     std::vector<Player> getMergedTeamList() const;
};

class Team::Changes{
        std::vector<Player> suggestedStartingLineUp;//must be sorted by score in descending order, ensure unit test captures this
        std::vector<Player> suggestedSubstitutes;////must be sorted by score in descending order ensure unit test captures this
        Player *captain, *viceCaptain;
        bool useTripleCaptain,useBenchBoost;
    public:
        const std::vector<Player> toSell;
        const std::vector<Player> toBuy;
        const std::vector<Player> newTeam;
        Changes()=delete;
        Changes(std::vector<Player>& _toSell,std::vector<Player>& _toBuy, std::vector<Player>& _newTeam):
        toSell(_toSell),toBuy(_toBuy),newTeam(_newTeam),captain(nullptr),viceCaptain(nullptr),
        useTripleCaptain(false),useBenchBoost(false)
        {};
        ~Changes();
        void setSuggestedStartingLineUp(std::vector<Player>&);
        void setSuggestedSubstitutes(std::vector<Player>&);
        void setCaptains();
        Player getCaptain();
        Player getViceCaptain();
        std::vector<Player> getSuggestedSubstitutes();
        std::vector<Player> getSuggestedStartingLineUp();
        std::size_t getNoChanges() const;
        void recommendTripleCaptain();
        void recommendBenchBoost();
        const bool isBenchBoostRecommended() const;
        const bool isTripleCaptainRecommended() const;
};
}//!namespace FantasyPremTeamSelection
#endif