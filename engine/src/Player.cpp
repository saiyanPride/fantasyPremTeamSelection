#include "Player.hpp"
namespace fantasypremierleague
{
float Player::getValue() const
{
    return value;
};

const std::string &Player::getName() const
{
    return name;
};

const std::string &Player::getClub() const
{
    return club;
};

bool Player::operator==(const Player &other) const
{
    return name == other.name && club == other.club && value == other.value;
}

bool Player::operator()(const Player &player1, const Player &player2) const
{
    return player1.getNextGameWeekScore() > player2.getNextGameWeekScore();
}

float Player::getNextGameWeekScore() const
{
    return nextGameweekScore;
}

const PlayerPostion &Player::getPosition() const
{
    return position;
}

float Player::getAvgFutureScore() const
{
    return avgFutureScore;
}

Player::~Player(){};

Player::Player(const Player &player)
    : club(player.club), name(player.name), value(player.value), position(player.position),
      nextGameweekScore(player.nextGameweekScore), avgFutureScore(player.avgFutureScore)
{
}

Player::Player()
{
}

Player &Player::operator=(const Player &player)
{
    if (this != &player)
    {
        club = player.club;
        name = player.name;
        value = player.value;
        position = player.position;
        nextGameweekScore = player.nextGameweekScore;
        avgFutureScore = player.avgFutureScore;
    }
    return *this;
}

Player::Player(Player &&player)
{
    club = player.club;
    name = player.name;
    value = player.value;
    position = player.position;
    nextGameweekScore = player.nextGameweekScore;
    avgFutureScore = player.avgFutureScore;
}

Player::Player(const std::string &_club, const std::string &_name, float _value, const PlayerPostion &_position, float _nextGameweekScore, float _avgFutureScore)
    : club(_club), name(_name), value(_value), position(_position), nextGameweekScore(_nextGameweekScore), avgFutureScore(_avgFutureScore)
{
}

void Player::display() const
{
    std::cout << "{ Name : " << name << " },\t\t";
    std::cout << "{ Club : " << club << " },\t";
    std::cout << "{ AvgScore : " << avgFutureScore << " },\t";
    std::cout << "{ NextGWScore : " << nextGameweekScore << " },\t";
    std::cout << "{ Value : " << value << " }; " << std::endl;
}
} //!namespace fantasypremierleague