#include "Player.hpp"
float Player::getValue() const
{
    return value;
};

const char *Player::getName() const
{
    return name;
};

Club Player::getClub() const
{
    return club;
};

bool Player::operator==(const Player &other) const
{
    return name == other.name && club == other.club && value == other.value;
}

bool Player::operator()(const Player &player1, const Player &player2) const
{
    return player1.getGameWeekScoreEstimate() > player2.getGameWeekScoreEstimate();
}

uint8_t Player::getGameWeekScoreEstimate() const
{
    return gameWeekScoreEstimate;
}

PlayerPostion Player::getPosition() const{
    return position;
}

Player::Player() {}

Player::Player(uint8_t _score, Club _club, const char *_name, float _value,PlayerPostion _position) 
    : gameWeekScoreEstimate(_score), club(_club), name(_name), value(_value),position(_position)
{
}

void Player::display() const{
    std::cout<<"Name"<<name<<std::endl;
    std::cout<<"Value"<<value<<std::endl;
    //TODO3: print club as well
}
