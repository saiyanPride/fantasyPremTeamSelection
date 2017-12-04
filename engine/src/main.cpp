#include "Team.hpp"
#include <memory>
#include <iostream>
#include "Chips.hpp"

void displaySuggestedChanges(std::shared_ptr<Team::Changes> suggestedChanges){
    //indicate whether changes are being recommended
    if (suggestedChanges.get()==nullptr) {
        std::cout<<"No changes are being recommended"<<std::endl;
        return;
    }
    //display players to sell and buy
    std::cout<<"The following players should be sold"<<std::endl;
    for(auto& playerToSell : suggestedChanges->toSell) playerToSell.display();    
    std::cout<<"The following players should be bought"<<std::endl;
    for(auto& playerToBuy : suggestedChanges->toBuy) playerToBuy.display();
    //display starting lineup
    std::cout<<"The following players should start"<<std::endl;
    for(auto& playerToStart : suggestedChanges->getSuggestedStartingLineUp()) playerToStart.display();
    //display captain, triple captain and if triple captain should be used
    std::cout<<std::string("-",20)<<std::endl;
    std::cout<<"Recommended Captain:"<<std::endl;
    suggestedChanges->getCaptain().display();
    std::cout<<std::string("-",20)<<std::endl;

    std::cout<<std::string("-",20)<<std::endl;
    std::cout<<"Recommended Vice Captain:"<<std::endl;
    suggestedChanges->getViceCaptain().display();
    std::cout<<std::string("-",20)<<std::endl;
    //display if other chips should be used
    std::cout<<"Use Bench Boost: "<<(suggestedChanges->isBenchBoostRecommended())<<std::endl;
    std::cout<<"Use Triple Captain: "<<(suggestedChanges->isTripleCaptainRecommended())<<std::endl;
}

bool shouldImplementChanges(){
    std::cout<<"Would you like the suggested changes to be implemented?"<<std::endl;
    std::cout<<"if yes: Enter 1, otherwise enter 0"<<std::endl;
    bool implement;
    std::cin>>implement;
    return implement;
}

void implementChanges(std::shared_ptr<Team::Changes> suggestedChanges){
    std::cout<<"implementing changes"<<std::endl;
};


void verifyGameWeekDifficultyUpdate(){
    bool response;
    std::cin>>response;
    if(!response) throw miscellaneous_exception("[Exception] You need to update gameweek difficulties");
   
}
int main(){
    //TODO (low priority) conditionally run the python update script based on user argument
    std::unique_ptr<Chips>& myChipsPtr = Chips::getChips(); //update status of chips
    std::cout<<"Have you updated gameweek difficulties in your database?\n enter '0' if you haven't"<<std::endl;
    try{
        verifyGameWeekDifficultyUpdate();
        Team myTeam;//create a Team object with your current team (starting lineup, substitutes etc)
        std::shared_ptr<Team::Changes> suggestedChanges=myTeam.suggestChanges();
        displaySuggestedChanges(suggestedChanges);   
        if(shouldImplementChanges()) implementChanges(suggestedChanges);
    }catch(no_suggestions_exception e){
        std::cout<<e.what()<<std::endl;
    }catch(miscellaneous_exception e){
        std::cout<<e.what()<<std::endl;
    }
    return 0;
}