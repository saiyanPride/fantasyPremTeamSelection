#include "Team.hpp"
#include <memory>
#include <iostream>
#include "Chips.hpp"
#include "Player.hpp"

namespace fantasypremierleague{
void displaySuggestedActions(std::shared_ptr<Team::Changes> suggestedActions){
    //indicate whether changes are being recommended
    if (suggestedActions.get()==nullptr) {
        std::cout<<"No changes are being recommended"<<std::endl;
        return;
    }
    //display players to sell and buy
    std::cout<<"The following players should be sold"<<std::endl;
    for(auto& playerToSell : suggestedActions->toSell) playerToSell.display();    
    std::cout<<"The following players should be bought"<<std::endl;
    for(auto& playerToBuy : suggestedActions->toBuy) playerToBuy.display();
    //display starting lineup
    std::cout<<"The following players should start"<<std::endl;
    for(auto& playerToStart : suggestedActions->getSuggestedStartingLineUp()) playerToStart.display();
    //display captain, triple captain and if triple captain should be used
    std::cout<<std::string("-",20)<<std::endl;
    std::cout<<"Recommended Captain:"<<std::endl;
    suggestedActions->getCaptain().display();
    std::cout<<std::string("-",20)<<std::endl;

    std::cout<<std::string("-",20)<<std::endl;
    std::cout<<"Recommended Vice Captain:"<<std::endl;
    suggestedActions->getViceCaptain().display();
    std::cout<<std::string("-",20)<<std::endl;
    //display if other chips should be used
    std::cout<<"Use Bench Boost: "<<(suggestedActions->isBenchBoostRecommended())<<std::endl;
    std::cout<<"Use Triple Captain: "<<(suggestedActions->isTripleCaptainRecommended())<<std::endl;
}

bool shouldImplementChanges(){
    std::cout<<"Would you like the suggested changes to be implemented?"<<std::endl;
    std::cout<<"if yes: Enter 1, otherwise enter 0"<<std::endl;
    bool implement;
    std::cin>>implement;
    return implement;
}

void implementChanges(std::shared_ptr<Team::Changes> suggestedActions){
    std::cout<<"implementing changes"<<std::endl;
};


void verifyGameWeekDifficultyUpdate(){
    bool response;
    std::cin>>response;
    if(!response) throw miscellaneous_exception("[Exception] You need to update gameweek difficulties");
   
}
}//! namespace fantasypremierleague

int main(){
    using namespace fantasypremierleague;
    //TODO (low priority) conditionally run the python update script based on user argument
    std::unique_ptr<Chips>& myChipsPtr = Chips::getChips(); //update status of chips
    std::cout<<"Have you updated gameweek difficulties in your database?\n enter '0' if you haven't"<<std::endl;
    try{
        verifyGameWeekDifficultyUpdate();
        Team myTeam;//create a Team object with your current team (starting lineup, substitutes etc)      
        std::shared_ptr<Team::Changes> suggestedActions = myTeam.suggestChanges();
        displaySuggestedActions(suggestedActions);   
        if(shouldImplementChanges()) implementChanges(suggestedActions);
    }catch(no_suggestions_exception e){
        std::cout<<e.what()<<std::endl;
    }catch(miscellaneous_exception e){
        std::cout<<e.what()<<std::endl;
    }
    return 0;
}
