#include "Analytics.hpp"
#include "Settings.hpp"
#include "Logger.hpp"
#include <cassert>

namespace fantasypremierleague
{

//NEBUG TODO: impl
/*
Returns an unordered list of goalkeepers that are worth considering for selection

For example goalkeepers that don't play at all, shouldn't be considered

*/
Players FplAnalytics::getPrunedGoalkeepers(){
    //TODO: simple database select statement
}
/*
Returns a sequence of goalkeeper pairs ordered by score in descending order
The ith pairing should be considered a better choice than the (i+1)th pairing

    Approach: 
    generate combinations of every possible goalkeeper pair, but generate combinations of higher scoring pairs before lower scoring pairs
    # GIVEN
    goalkeepers = {G1,G2,G3,G4 ... , Gn}
     
    result should be ranked pairs in a way that encapsulates our desire to have pairs that complement each other
    
    result will look like: [ (G1,G2), (G1,G3), (G2,G3),(G1,G4 )...]

    Example Pair and their predicted scores for next 3 Gameweeks

    Pair1
    G1: 5   5   5   5   5
    G2: 5   5   5   5   5
    predicted obtainable goalie points = 25
    sum of average pair scores = 25

    Pair2
    G1: 5   5   1   5   5
    G2: 1   5   5   5   1
    predicted obtainable goalie points = 25
    sum of average pair scores = 19

    Pair3
    G1: 5   5   1   5   5
    G2: 1   1   5   1   1
    predicted obtainable goalie points = 25
    sum of average pair scores = 15

    
    Pair4
    G1: 5   5   1   5   5
    G2: 5   5   1   5   5
    predicted obtainable goalie points = 21
    sum of average pair scores = 21
    


    # THEN 
    priority/ranking in results should match
    Pair 1 > Pair 2
    Pair 2 > Pair 3 even though they have same predicted obtainable goalie points one pair has a better back up goalkeeper in case of injury and thus has a more powerful pair
    Pair 3 > Pair 4 due to better points up for grabs, even though Pair 4 has a stronger performing pair
    
    summary:
    sort by predicted obtainable goalie points
    if tie, then sort by sum of average pair scores
    and if tie predicted obtainable goalie points per value (in £)
    and if still tie just pick first one (doesn't matter)
*/
vector< std::pair<Player,Player> > FplAnalytics::getPrunedGoalkeeperPairs() {
    info("getting pruned goalkeepers");
    Players goalkeepers = getPrunedGoalkeepers();
    int numberGoalkeepers = goalkeepers.size();
    assert(numberGoalkeepers >= 2);

    vector<GoalkeeperPair> goalkeeperPairs;
    goalkeeperPairs.reserve(numberGoalkeepers * numberGoalkeepers-1); // total number of pairs is nC2 = n * n-1

    for(int i=0; i<numberGoalkeepers-1; ++i){
        for(int j=i+1; j<numberGoalkeepers; ++j){
            goalkeeperPairs.emplace_back(goalkeepers[i],goalkeepers[j]);
        }
    }
    
    sort(goalkeeperPairs.begin(),goalkeeperPairs.end(), 
        [](const auto& goalkeeperPair1, const auto& goalkeeperPair2){
            if(goalkeeperPair1.getMaxObtainablePoints() != goalkeeperPair2.getMaxObtainablePoints()){// can rank based on maxObtainablePoints
                return goalkeeperPair1.getMaxObtainablePoints() > goalkeeperPair2.getMaxObtainablePoints();
            }else if(goalkeeperPair1.getSumOfAveragePredictedPoints() != goalkeeperPair2.getSumOfAveragePredictedPoints()){
                return goalkeeperPair1.getSumOfAveragePredictedPoints() > goalkeeperPair2.getSumOfAveragePredictedPoints();
            }else{
                if(!(goalkeeperPair1.getTotalValue() > 0 && goalkeeperPair2.getTotalValue() > 0) ){
                    error("goalkeepers being processed have total values that are <= 0");
                }
                float gkPair1PointsPerValue = goalkeeperPair1.getMaxObtainablePoints()/goalkeeperPair1.getTotalValue();
                float gkPair2PointsPerValue = goalkeeperPair2.getMaxObtainablePoints()/goalkeeperPair2.getTotalValue();

                return gkPair1PointsPerValue >= gkPair2PointsPerValue; // final tie breaker
            }
        
        }
    );
    
    // generate result
    vector< std::pair<Player,Player> > result;
    result.reserve(goalkeeperPairs.size());

    std::transform(
        goalkeeperPairs.begin(),goalkeeperPairs.end(),result.begin(),
        [](const GoalkeeperPair& gkPair){ return gkPair.getGoalkeeperPair();}
    );

    return result;
}

GoalkeeperPair::GoalkeeperPair(Player goalkeeper1_, Player goalkeeper2_){
    validate(goalkeeper1_,goalkeeper2_);
    
    goalkeeper1 = goalkeeper1_;
    goalkeeper2 = goalkeeper2_;

    setMaxObtainablePoints();
    setSumOfAveragePredictedPoints();
    setTotalValue();
}

float GoalkeeperPair::getMaxObtainablePoints() const{
    return maxObtainablePoints;
}

float GoalkeeperPair::getSumOfAveragePredictedPoints() const{
    return sumOfAveragePredictedPoints;
}
float GoalkeeperPair::getTotalValue() const{
    return totalValue;
}

void GoalkeeperPair::validate(Player goalkeeper1_, Player goalkeeper2_){//TODO: minor: player object should have function for getting number of gameweeks worth of data it has

    info("validating goalkeepers");
    if(goalkeeper1_.getPosition() != PlayerPostion::GOALKEEPER) {
        error(goalkeeper1_.getName() + " is not a goalkeeper!");
    }
    
    if(goalkeeper2_.getPosition() != PlayerPostion::GOALKEEPER) {
        error(goalkeeper2_.getName() + " is not a goalkeeper!");
    }

    const auto& goalkeeper1PredictedFutureGameWeekScores = goalkeeper1.getPredictedFutureGameWeekScores();
    const auto& goalkeeper2PredictedFutureGameWeekScores = goalkeeper2.getPredictedFutureGameWeekScores();
    
    if(goalkeeper1PredictedFutureGameWeekScores.size() != goalkeeper2PredictedFutureGameWeekScores.size()){
        error(goalkeeper1_.getName()+" and " + goalkeeper2_.getName()+ " don't have the same amount of gameweek score data");
    }

    int numGameWeeksWithPointsData = goalkeeper1PredictedFutureGameWeekScores.size();

    if(NO_FUTURE_GAMEWEEKS_TO_CONSIDER > numGameWeeksWithPointsData){
        error("number of future gameweeks to consider, is larger than number of gameweeks with points data");
    }
}
void GoalkeeperPair::setMaxObtainablePoints(){
    
    const auto& goalkeeper1PredictedFutureGameWeekScores = goalkeeper1.getPredictedFutureGameWeekScores();
    const auto& goalkeeper2PredictedFutureGameWeekScores = goalkeeper2.getPredictedFutureGameWeekScores();

    maxObtainablePoints = 0;
    for(int i=0; i < NO_FUTURE_GAMEWEEKS_TO_CONSIDER; ++i){
        maxObtainablePoints += std::max(goalkeeper1PredictedFutureGameWeekScores[i],goalkeeper2PredictedFutureGameWeekScores[i]);
    }
}
void GoalkeeperPair::setSumOfAveragePredictedPoints(){
    const auto& goalkeeper1PredictedFutureGameWeekScores = goalkeeper1.getPredictedFutureGameWeekScores();
    const auto& goalkeeper2PredictedFutureGameWeekScores = goalkeeper2.getPredictedFutureGameWeekScores();
    
    sumOfAveragePredictedPoints = 0;
    for(int i=0; i < NO_FUTURE_GAMEWEEKS_TO_CONSIDER; ++i){
        sumOfAveragePredictedPoints += (goalkeeper1PredictedFutureGameWeekScores[i] + goalkeeper2PredictedFutureGameWeekScores[i])/2.0;
    }
}
void GoalkeeperPair::setTotalValue(){
    totalValue = goalkeeper1.getValue() + goalkeeper2.getValue();
}
std::pair<Player,Player> GoalkeeperPair::getGoalkeeperPair() const{
    return std::pair<Player,Player>(goalkeeper1,goalkeeper2);
}
} //!namespace fantasypremierleague