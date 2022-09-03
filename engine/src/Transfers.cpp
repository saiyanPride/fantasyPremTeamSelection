#include "Transfers.hpp"

namespace fantasypremierleague
{

PotentialSquad chooseTopNSquads(const Constraints& constraints, const int n){
    /*
    TODO: actualy use this algo by calling this function in appropriate place

    //constraints by scenario //NEBUG: readTHis
        freeTransfer => Constraints(budget=B, numFreeTransfers = 1 or 2, numGameWeeksToConsider= DEFAULT);
        freeHit => Constraints(budget=B, numFreeTransfers = INT_MAX, numGameWeeksToConsider= 1)
        wildcard => Constraints(budget=B, numFreeTransfers = INT_MAX, numGameWeeksToConsider= DEFAULTe.g. 5)
    */
    FPLAnalytics(constraints.gameWeekHorizon) fplAnalytics; // TODO: sort out the FPLAnalytics class, interface etc

    // prune the players, to limit the numbers of players in scope for selection, and reduce degree of combinatorial explosion
    PlayersByPosition outfieldPlayersToConsider;

    outfieldPlayersToConsider[PlayerPostion::FORWARD] = fplAnalytics.getPrunedStrikers();
    outfieldPlayersToConsider[PlayerPostion::MIDFIELDER] = fplAnalytics.getMidfielders();
    outfieldPlayersToConsider[PlayerPostion::DEFENDER] = fplAnalytics.getDefenders();
    vector< std::pair<Player,Player> > goalkeepersToConsider = fplAnalytics.getGoalkeepers(); // sorted list of goalkeeper pairs by appropriate ranking mechanism that ensure their fixtures are complementary

    // generate potential squads that satisfy constraints
    vector<PotentialSquad> candidateSquads = generateTeamsThatSatisfyBudgetConstraints(constraints, outfieldPlayersToConsider, goalkeepersToConsider);
    return getTopNSquads(candidateSquads);
}

vector<PotentialSquad> getTopNSquads(const vector<PotentialSquad>& candidateSquads, const int n){// NEBUG: to impl
    vector<PotentialSquad> viableSquads = filterForViableSquads(candidateSquads, constraints);//TODO: optimise to reduce allocation
    vector<PotentialSquad>& viableSquadsMaxHeap = viableSquads;

    //TODO: rank squads by topPriority e.g. use heapify on viableSquadsHeap
    /*
    This gets a score for the next `gameWeekHorizon` for each squad and ranks them

    a simplistic approach will just total the predicted points, but because a lot can change in the future and there's room for transfers for future gameweeks
    implementation should assign higher weighting to gameweek i, than gameweek i+1

    This should factor in the cost of transfers as well, when determining total
    */
    vector<PotentialSquad> topNSquads;
    topNSquads.reserve(n);

    for(int i=0; i<n; ++i){
        topNSquads.push_back(std::move(viableSquadsMaxHeap.front()));
        //std::pop_heap(topNSquads.begin(), topNSquads.end()); //TODO: include the comparator for popping
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
    }elif(playersChosenSoFar.size() < REQUIRED_NO_FORWARDS + REQUIRED_NO_MIDFIELDER){ // levels 3 to 7:  choose midfielders
        descendInTree(PlayerPostion::MIDFIELDER);
    }elif(playersChosenSoFar.size() < REQUIRED_NO_FORWARDS + REQUIRED_NO_MIDFIELDER + REQUIRED_NO_DEFENDERS){// levels 8  to 12: choose defenders
        descendInTree(PlayerPostion::DEFENDER);
    }else{//leaf node // // level 13: choose a goalkeeper pair i.e. 2 goalkeepers and store result in results
        auto playerPosition =  PlayerPostion::GOALKEEPER;
        for(int i=nextPlayerToConsiderIndexByPosition[playerPosition]; i<goalkeeperOptions[playerPosition].size(); ++i){

            //choose pair of goalies
            const auto& nextGoalkeeperPair = goalkeeperOptions[playerPosition][i];
            auto goalie1 = nextGoalkeeperPair.first;
            auto goalie2 = nextGoalkeeperPair.second;
            if(goalie1.getValue() + goalie2.getValue() > budget) continue;
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


vector<PotentialSquad> filterForViableSquads(vector<PotentialSquad>& squads, const Constraints& constraints){// NEBUG: to impl
    //TODOs

    //TODO: should filter out squads that don't satisfy `constraints`, could use `getAttainableSquadsByNumberOfFreeTransfers` if sensible
        // if wildcard then cosntrains is different from when we have 2 free transfers versus freeHit

    // NEBUG: you already have a function for determining number of transfers needed to achieve a squad from current squad, RESUE IT!!
}


vector<PotentialSquad> getAttainableSquadsByNumberOfFreeTransfers(vector<PotentialSquad>& squads, const Constraints& constraints){// NEBUG: to impl if needed
    //TODO if needed
}

};// ! namespace fantasypremierleague


//NEBUG: test code