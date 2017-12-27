#ifndef FANTASY_PLAYER
#define FANTASY_PLAYER
#include <iostream>
#include "Settings.hpp"
namespace FantasyPremTeamSelection{
class Player
{
    std::string name,club;
    float value, nextGameweekScore, avgFutureScore;
    PlayerPostion position;

  public:
    ~Player();
    Player();
    Player(const Player&);
    Player(Player&&);
    Player(std::string _club, std::string _name, float _value,PlayerPostion _position,float _nextGameweekScore,float _avgFutureScore);
    float getValue() const;
    std::string getClub() const;
    std::string getName() const;
    float getNextGameWeekScore() const;
    float getAvgFutureScore() const;
    PlayerPostion getPosition() const;
    Player& operator=(const Player &other);
    bool operator==(const Player &other) const;
    bool operator()(const Player &player1, const Player &player2) const;//functor used for comparisons
    void display() const;
};
}//!namespace FantasyPremTeamSelection

template <>
struct std::hash<FantasyPremTeamSelection::Player>
{
    std::size_t operator()(const FantasyPremTeamSelection::Player &player) const
    {
        using std::hash;

        return hash<std::string>()(player.getName()) ^ hash<std::string>()(player.getClub()) ^ hash<float>()(player.getValue());
    }
    //TODO(medium priority): improve this hash functor to guaranteee a unique hashcode for each player
};
#endif