#ifndef FANTASY_PLAYER
#define FANTASY_PLAYER
#include <iostream>
#include "Settings.hpp"
namespace fantasypremierleague
{
class Player
{
    std::string name, club;
    float value, nextGameweekScore, avgFutureScore;
    PlayerPostion position;

  public:
    ~Player();
    Player();
    Player(const Player &);
    Player(Player &&);
    Player(const std::string &_club, const std::string &_name, float _value, const PlayerPostion &_position, float _nextGameweekScore, float _avgFutureScore);
    float getValue() const;
    const std::string &getClub() const;
    const std::string &getName() const;
    float getNextGameWeekScore() const;
    float getAvgFutureScore() const;
    const PlayerPostion &getPosition() const;
    Player &operator=(const Player &other);
    bool operator==(const Player &other) const;
    bool operator()(const Player &player1, const Player &player2) const; // returns true if player1 has a greater estimated next gameweek score than player2
    void display() const;
};
} //!namespace fantasypremierleague

template <>
struct std::hash<fantasypremierleague::Player>
{
    std::size_t operator()(const fantasypremierleague::Player &player) const
    {
        using std::hash;

        return hash<std::string>()(player.getName()) ^ hash<std::string>()(player.getClub()) ^ hash<float>()(player.getValue());
    }
};
#endif