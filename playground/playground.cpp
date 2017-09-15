#include <queue>  
#include <algorithm>
#include <string>
#include <utility>
#include <unordered_map>
#include <iostream>
#include <array>
#include <cstdint>
#include <vector>
#include <stack>

#include <memory>
  
using namespace std;

void printStack(stack<int>& best,vector<int>& playerListDesc){
    int stackinitialSize=best.size();
    for(int i=0;i!=stackinitialSize;i++){
        cout<<playerListDesc.at(best.top())<<" ";
        best.pop();
    }
    cout<<"\n"<<endl;
}

/*
Approach 1
Given a list of numbers sorted in descending order 
One picks the n numbers which give the largest sum, where the largest sum has an upper bound (budget)
The result is a combination/representative-set where the members of the result are in descending order i.e. if result is {1,8,7}, representative set is {8,7,1}
The approach here is similar to a non-recursive implementation of DFS, but can be improved
Inefficiency: if one wants 3 numbers and is given ten numbers,
by inspection one knows that only the first 8 numbers in the list can be the first value in the result
Thus by the time number 9 is being considered as the first value of result, the algo should accept defeat

*/
stack<int> getBest(int desiredNoPlayers, vector<int>& playerListDesc){
    int budget=35, budgetLeft=35;  
    stack<int> bestPlayerCombinationStack;
    int nextPlayerInd=0;//loop should start from first player in list
    while(bestPlayerCombinationStack.size()!=desiredNoPlayers){
        
        if(nextPlayerInd==playerListDesc.size()){//if no more options to add, try to backtrack
            if(bestPlayerCombinationStack.empty()){//if no more options and stack is empty->no result
                cout<<"impossible to get players to fit into budget"<<endl;
                throw exception();
            }
            nextPlayerInd=bestPlayerCombinationStack.top()+1;
            bestPlayerCombinationStack.pop();
            budgetLeft+=playerListDesc.at(nextPlayerInd-1);//budgetLeft is updated to reflect removal of player
            continue;
        }
        //add player if budget allows
        if(playerListDesc.at(nextPlayerInd)<=budgetLeft){
            budgetLeft-=playerListDesc.at(nextPlayerInd);//budgetLeft is updated to reflect addition of player
            bestPlayerCombinationStack.push(nextPlayerInd); 
        }
            ++nextPlayerInd;
    }
    
    return bestPlayerCombinationStack;
};

/*
Approach 2
In this version, algo notes the stack top blacklist, the moment a number in the blacklist is being considered for the top spot
in the stack, the algo accepts defeat
 This approach is approx 10 times faster
*/
stack<int> getBest2(int desiredNoPlayers, vector<int>& playerListDesc){
        int lastPossibleFirstMemberOfResultInd=playerListDesc.size()-desiredNoPlayers+1;//(playerListDesc.size()-1)-desiredNoPlayers+2;
        int budget=35, budgetLeft=35;  
        stack<int> bestPlayerCombinationStack;
        int nextPlayerInd=0;//loop should start from first player in list
        while(bestPlayerCombinationStack.size()!=desiredNoPlayers){
            if(bestPlayerCombinationStack.empty() && nextPlayerInd==lastPossibleFirstMemberOfResultInd+1){//when considering adding the first blacklisted value to the top of stack then stop                    cout<<"impossible to get players to fit into budget"<<endl;
                    cout<<"impossible to get players to fit into budget"<<endl;
                    throw exception();
                }
            
            if(nextPlayerInd==playerListDesc.size()){//if no more options to add, try to backtrack
                nextPlayerInd=bestPlayerCombinationStack.top()+1;
                bestPlayerCombinationStack.pop();
                budgetLeft+=playerListDesc.at(nextPlayerInd-1);//budgetLeft is updated to reflect removal of player
                continue;
            }
            //add player if budget allows
            if(playerListDesc.at(nextPlayerInd)<=budgetLeft){
                budgetLeft-=playerListDesc.at(nextPlayerInd);//budgetLeft is updated to reflect addition of player
                bestPlayerCombinationStack.push(nextPlayerInd); 
            }
                ++nextPlayerInd;
        }
    
    return bestPlayerCombinationStack;
};

/*
Approach 3
aliter for getBest3 is to use a for loop to implement recursive calls similar to the approach used to generate combinations
this would be slower due to the number functions calls and the associated costs of create and unwinding stacks for each function call
-This approach would however also know the instant no result exists like approach 2
*/
int main(){

    
    //vector<int> playerList{{30,15,10,9,8,5}};
    //vector<int> playerList{{14,13,11,10,9,8,7,5}};
    //vector<int> playerList{{25,12,11,10,9,8,7,5,4}};
    //vector<int> playerList{{50,40,30,20,15,9,8,5}};
    vector<int> playerList{{100,90,80,70,8,5}};
    stack<int> best=getBest(3,playerList);
    
    //print result
    printStack(best,playerList);
    
}