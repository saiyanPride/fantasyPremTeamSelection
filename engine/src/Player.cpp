#include "Player.hpp"
float Player::getValue() const
{
    return value;
};

std::string Player::getName() const
{
    return name;
};

std::string Player::getClub() const
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

PlayerPostion Player::getPosition() const{
    return position;
}


Player::~Player(){
};

Player::Player(const Player& player)
    :club(player.club), name(player.name), value(player.value),position(player.position), nextGameweekScore(player.nextGameweekScore), avgFutureScore(player.avgFutureScore)
{
    //std::cout<<"copy constructor called for "<<name<<std::endl;//DEBUG
}

Player::Player(){

}

Player& Player::operator=(const Player& player){
    if( this != &player){
        club = player.club;
        name = player.name;
        value = player.value;
        position = player.position;
        nextGameweekScore = player.nextGameweekScore;
        avgFutureScore = player.avgFutureScore;

    }
    


    return *this;
}  

Player::Player(Player&& player){
    club = player.club;
    name = player.name;
    value = player.value;
    position = player.position;
    nextGameweekScore = player.nextGameweekScore;
    avgFutureScore = player.avgFutureScore;
    //std::cout<<"Move constructor called for "<<name<<std::endl;//DEBUG
}

Player::Player(std::string _club, std::string _name, float _value,PlayerPostion _position,float _nextGameweekScore,float _avgFutureScore) 
    : club(_club), name(_name), value(_value),position(_position), nextGameweekScore(_nextGameweekScore), avgFutureScore(_avgFutureScore)
{
    //std::cout<<"Player constructor called for "<<name<<std::endl;//DEBUG
}

void Player::display() const{
    std::cout<<"{ Name : "<<name<<" },\t\t";
    std::cout<<"{ Club : "<<club<<" },\t";
    std::cout<<"{ AvgScore : "<<avgFutureScore<<" },\t";
    std::cout<<"{ NextGWScore : "<<nextGameweekScore<<" },\t";
    std::cout<<"{ Value : "<<value<<" }; "<<std::endl;
}
