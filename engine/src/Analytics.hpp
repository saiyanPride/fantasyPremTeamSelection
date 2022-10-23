#pragma once
#include "Transfers.hpp"
#include "Player.hpp"
using std::vector;

namespace fantasypremierleague
{

class FplAnalytics{ //TODO: impl

    const Constraints constraints;
    public:
        FplAnalytics(const Constraints& constraints_): constraints(constraints_){};
        Players getPrunedStrikers();//TODO: impl
        Players getPrunedMidfielders();//TODO: impl
        Players getPrunedDefenders();//TODO: impl
        vector< std::pair<Player,Player> > getPrunedGoalkeeperPairs();//TODO: impl
    private:
        Players getPrunedGoalkeepers();//TODO: impl
};


class GoalkeeperPair{
    public:
        GoalkeeperPair(Player goalkeeper1_, Player goalkeeper2_);

        // function members
        float getMaxObtainablePoints() const;
        float getSumOfAveragePredictedPoints() const;
        float getTotalValue() const;

        std::pair<Player,Player> getGoalkeeperPair() const;
    private:
        // function members
        void setMaxObtainablePoints();
        void setSumOfAveragePredictedPoints();
        void setTotalValue();
        void validate(Player goalkeeper1_, Player goalkeeper2_);

        // data members
        Player goalkeeper1,goalkeeper2;
        float maxObtainablePoints;
        float sumOfAveragePredictedPoints;
        float totalValue;
};
}//!namespace fantasypremierleague