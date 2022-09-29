#include "Transfers.hpp"
#include <numeric>
using namespace std;

namespace fantasypremierleague
{

vector<PotentialSquad> chooseTopNSquads(const Constraints& constraints, const int n, Team &currentTeam){
    /*
    TODO: actualy use this algo by calling this function in appropriate place

    //constraints by scenario //NEBUG: readTHis
        freeTransfer => Constraints(budget=B, numFreeTransfers = 1 or 2, numGameWeeksToConsider= DEFAULT);
        freeHit => Constraints(budget=B, numFreeTransfers = INT_MAX, numGameWeeksToConsider= 1)
        wildcard => Constraints(budget=B, numFreeTransfers = INT_MAX, numGameWeeksToConsider= DEFAULTe.g. 5)
    */
    FplAnalytics fplAnalytics(constraints); // TODO: sort out the FPLAnalytics class, interface etc

    // prune the players, to limit the numbers of players in scope for selection, and reduce degree of combinatorial explosion
    PlayersByPosition outfieldPlayersToConsider;

    outfieldPlayersToConsider[PlayerPostion::FORWARD] = fplAnalytics.getPrunedStrikers();
    outfieldPlayersToConsider[PlayerPostion::MIDFIELDER] = fplAnalytics.getPrunedMidfielders();
    outfieldPlayersToConsider[PlayerPostion::DEFENDER] = fplAnalytics.getPrunedDefenders();
    vector< std::pair<Player,Player> > goalkeepersToConsider = fplAnalytics.getPrunedGoalkeeperPairs(); // sorted list of goalkeeper pairs by appropriate ranking mechanism that ensure their fixtures are complementary

    // generate potential squads that satisfy constraints
    vector<PotentialSquad> candidateSquads = generateTeamsThatSatisfyBudgetConstraints(constraints, outfieldPlayersToConsider, goalkeepersToConsider);
    return getTopNSquads(candidateSquads,MAX_NUMBER_OF_BETTER_SQUADS_TO_CONSIDER_DURING_OVERHAULS,currentTeam, constraints);
}

class EnrichedSquad{ //TODO: optional consider relocating this
    PotentialSquad squad;
    vector<float> squadPredictedFutureGameWeekScores;
    float totalFutureGameWeekScores;//TODO: optional maybe weight scores by gameweek, with GW1 having greater weighting
    public:
    EnrichedSquad(const PotentialSquad& squad_):squad(squad_){
        
        if(squad_.empty()){
            cout<<"[ERROR] received an empty squad"<<endl;
        }else{

            totalFutureGameWeekScores = 0.0f;
            squadPredictedFutureGameWeekScores = vector<float>(squad_[0].getPredictedFutureGameWeekScores().size());
            
            for(int j =0; j<squad_.size(); ++j){
                const Player& player = squad_[j];
                const std::vector<float>& playerPredictedFutureGameWeekScores = player.getPredictedFutureGameWeekScores();
                for(int i=0; i<playerPredictedFutureGameWeekScores.size(); ++i){
                    totalFutureGameWeekScores += playerPredictedFutureGameWeekScores.at(i);
                    squadPredictedFutureGameWeekScores[i] += playerPredictedFutureGameWeekScores.at(i);
                }

            }
        }
    }

    PotentialSquad getSquad() const{ //TODO: return const&?
        return squad;
    }

    float getTotalFutureGameWeekScores() const{
        return totalFutureGameWeekScores;
    }
    
    /*

    Apply cost of free transfer, chip or anything to the gameweek scores
    */
    void applyCost(float cost){
        totalFutureGameWeekScores -= cost;
        squadPredictedFutureGameWeekScores[0] -= cost; // apply transfer costs to the next gameweek

    }


    vector<float> getSquadPredictedFutureGameWeekScores() const{
        return squadPredictedFutureGameWeekScores;
    }

    
    
};

vector<PotentialSquad> getTopNSquads(const vector<PotentialSquad>& candidateSquads, const int n, Team &currentTeam, const Constraints& constraints){// TODO: test this!! important that order is correct

    EnrichedSquad currentSquad(currentTeam.getMergedTeamList());

    vector<EnrichedSquad> squadsBetterThanCurrentSquad;
    squadsBetterThanCurrentSquad.reserve(candidateSquads.size()); //TODO: consider performance implication of overallocating

    // populate `squadsBetterThanCurrentSquad`
    for (PotentialSquad& candidateSquad : candidateSquads){
        int numberOfTransfersRequired = currentTeam.getChangesRequiredToFormNewTeam(candidateSquad)->toSell.size();
        int numberOfNonFreeTransfers =  max(0, numberOfTransfersRequired - constraints.numFreeTransfers);
        float cost = constraints.costPerNonFreeTransfer * numberOfNonFreeTransfers;
        EnrichedSquad candidateSquadData(candidateSquad);
        candidateSquadData.applyCost(cost);

        if(// exclude candidate squads not better than current squad in terms of next GW points and future GW points 
            candidateSquadData.getSquadPredictedFutureGameWeekScores().at(0) <= currentSquad.getSquadPredictedFutureGameWeekScores().at(0) ||
            candidateSquadData.getTotalFutureGameWeekScores() <= currentSquad.getTotalFutureGameWeekScores()
        ){
            continue; //skip `candidateSquad`, not worth considering 
        }
        squadsBetterThanCurrentSquad.push_back(move(candidateSquadData));
    }
    
    auto isFirstSquadLessValuableThanSecond = [](const EnrichedSquad& first, const EnrichedSquad& second) -> bool
    {
        // check next gameweek points
        float next_gw_points_first = first.getSquadPredictedFutureGameWeekScores().at(0);
        float next_gw_points_second = second.getSquadPredictedFutureGameWeekScores().at(0);
        if(next_gw_points_first != next_gw_points_second){
            return next_gw_points_first < next_gw_points_second;
        }

        // tie breaker
        return first.getTotalFutureGameWeekScores() <= second.getTotalFutureGameWeekScores();
    };

    // get the top N squads Better Than CurrentSquad
    vector<EnrichedSquad>& viableSquadsMaxHeap = squadsBetterThanCurrentSquad;
    make_heap(viableSquadsMaxHeap.begin(), viableSquadsMaxHeap.end(),isFirstSquadLessValuableThanSecond);

    vector<PotentialSquad> topNSquads;
    topNSquads.reserve(n);

    for(int i=0; i<n; ++i){
        topNSquads.push_back(std::move(viableSquadsMaxHeap.front().getSquad()));
        std::pop_heap(viableSquadsMaxHeap.begin(), viableSquadsMaxHeap.end(),isFirstSquadLessValuableThanSecond);
    }
    return topNSquads;

}

vector<PotentialSquad> generateTeamsThatSatisfyBudgetConstraints(
    const Constraints& constraints, 
    const PlayersByPosition& outfieldPlayerOptions, 
    const GoalkeeperPairs& goalkeeperOptions){

        vector<PotentialSquad> results;
        PotentialSquad playersChosenSoFar;
        std::unordered_map<PlayerPostion, int> nextPlayerToConsiderIndexByPosition{
            {PlayerPostion::FORWARD,0},
            {PlayerPostion::MIDFIELDER,0},
            {PlayerPostion::DEFENDER, 0},
            {PlayerPostion::GOALKEEPER,0}
        };
        return generateTeamsThatSatisfyBudgetConstraints(results,playersChosenSoFar,constraints.budget,outfieldPlayerOptions,goalkeeperOptions,nextPlayerToConsiderIndexByPosition);
}

void generateTeamsThatSatisfyBudgetConstraints(vector<PotentialSquad>& results, PotentialSquad& playersChosenSoFar, 
    const float budget, const PlayersByPosition& outfieldPlayerOptions, 
    const GoalkeeperPairs& goalkeeperOptions, 
    std::unordered_map<PlayerPostion, int>& nextPlayerToConsiderIndexByPosition){//TODO: make `nextPlayerToConsiderIndexByPosition` a reference
    /*
    combinatorial Tree
    Assuming
    REQUIRED_NO_FORWARDS = 3;
    REQUIRED_NO_MIDFIELDER = 5;
    REQUIRED_NO_DEFENDERS = 5;
    REQUIRED_NO_GOALKEEPERS = 2;

    levels 0-2: choose strikers
    levels 3 to 7:  choose midfielders
    levels 8  to 12: choose defenders
    level 13: choose a goalkeeper pair i.e. 2 goalkeepers

    size(playersChosenSoFar) is equal to level in tree
    */

    auto descendInTree = [&](const PlayerPostion& playerPosition){//every descent leads to the next outfield player being chosen
        for(int i=nextPlayerToConsiderIndexByPosition[playerPosition]; i<outfieldPlayerOptions[playerPosition].size(); ++i){
            const auto& nextPlayer = outfieldPlayerOptions[playerPosition][i];
            if(nextPlayer.getValue() > budget) continue;
            playersChosenSoFar.push_back(nextPlayer);
            

            nextPlayerToConsiderIndexByPosition[playerPosition] = i+1;
            generateTeamsThatSatisfyBudgetConstraints(results,playersChosenSoFar,budget-nextPlayer.getValue(),outfieldPlayerOptions,goalkeeperOptions,nextPlayerToConsiderIndexByPosition);
            
            //reinstate original state
            playersChosenSoFar.pop_back();
            //nextPlayerToConsiderIndexByPosition[playerPosition] = i;//NEBUG: is this valid or needed. No call uses this value, each descent always has the right value set, so this shouldn't be needed i.e. at point of entry of each node, this value is always valid
        }

    };

    if(playersChosenSoFar.size() < REQUIRED_NO_FORWARDS){ // levels 0-2: choose strikers
        descendInTree(PlayerPostion::FORWARD);
    }else if(playersChosenSoFar.size() < REQUIRED_NO_FORWARDS + REQUIRED_NO_MIDFIELDER){ // levels 3 to 7:  choose midfielders
        descendInTree(PlayerPostion::MIDFIELDER);
    }else if(playersChosenSoFar.size() < REQUIRED_NO_FORWARDS + REQUIRED_NO_MIDFIELDER + REQUIRED_NO_DEFENDERS){// levels 8  to 12: choose defenders
        descendInTree(PlayerPostion::DEFENDER);
    }else{//leaf node // // level 13: choose a goalkeeper pair i.e. 2 goalkeepers and store result in results
        for(int i=0; i<goalkeeperOptions.size(); ++i){

            //choose pair of goalies
            const auto& nextGoalkeeperPair = goalkeeperOptions[i];
            auto goalie1 = nextGoalkeeperPair.first;
            auto goalie2 = nextGoalkeeperPair.second;
            if(goalie1.getValue() + goalie2.getValue() > budget) continue;
            
            // choosing this goalkeeper pair is within budget constraints
            playersChosenSoFar.push_back(goalie1);
            playersChosenSoFar.push_back(goalie2);
            
            // store result
            results.push_back(playersChosenSoFar);
            
            //reinstate original state in preperation for next iteration
            playersChosenSoFar.pop_back();
            playersChosenSoFar.pop_back();
        }    
    }
    
}

} //!namespace fantasypremierleague
//NEBUG: test code