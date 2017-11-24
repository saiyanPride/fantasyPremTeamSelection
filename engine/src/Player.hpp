#ifndef FANTASY_PLAYER
#define FANTASY_PLAYER
#include <iostream>
#include "Settings.hpp"
class Player
{
    uint8_t gameWeekScoreEstimate;//estimate score for the current game week i.e. the one that a team can be chosen for
    Club club;
    const char *name;
    float value;
    PlayerPostion position;

  public:
    Player();
    Player(uint8_t,Club,const char *,float,PlayerPostion);
    float getValue() const;
    Club getClub() const;
    const char *getName() const;
    uint8_t getGameWeekScoreEstimate() const;
    PlayerPostion getPosition() const;
    bool operator==(const Player &other) const;
    bool operator()(const Player &player1, const Player &player2) const;//functor used for comparisons
    void display() const;
};

namespace std {
template <>
struct std::hash<Player>
{
    std::size_t operator()(const Player &player) const
    {
        using std::hash;

        return hash<const char *>()(player.getName()) ^ hash<Club>()(player.getClub()) ^ hash<float>()(player.getValue());
    }
    //TODO(medium priority): improve this hash functor to guaranteee a unique hashcode for each player
};
}

#endif