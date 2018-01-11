#include "UserEngagement.hpp"
namespace fantasypremierleague{

// Summarises team recommendations for the next gameweek
// Players to buy & sell, best starting lineup, the best candidate for captaincy and which chips to use if any are displayed
void displaySuggestedTeamChanges(std::shared_ptr<Team::Changes> suggestedTeamChanges){

    auto printHorizontalLine = [](){std::cout<<std::string("-",20)<<std::endl;};
    //indicate whether changes are being recommended
    if (suggestedTeamChanges.get()==nullptr) {
        std::cout<<"No changes are being recommended"<<std::endl;
        return;
    }

    //display players to sell and buy
    printHorizontalLine();
    std::cout<<"The following players should be sold"<<std::endl;
    for(auto& playerToSell : suggestedTeamChanges->toSell) playerToSell.display();    
    std::cout<<"The following players should be bought"<<std::endl;
    for(auto& playerToBuy : suggestedTeamChanges->toBuy) playerToBuy.display();
    printHorizontalLine();

    //display starting lineup
    printHorizontalLine();
    std::cout<<"The following players should be in the starting lineup"<<std::endl;
    for(auto& playerToStart : suggestedTeamChanges->getSuggestedStartingLineUp()) playerToStart.display();
    printHorizontalLine();

    //display captain, triple captain and if triple captain should be used
    printHorizontalLine();
    std::cout<<"Recommended Captain:"<<std::endl;
    suggestedTeamChanges->getCaptain().display();
    printHorizontalLine();

    printHorizontalLine();
    std::cout<<"Recommended Vice Captain:"<<std::endl;
    suggestedTeamChanges->getViceCaptain().display();
    printHorizontalLine();

    //display if other chips should be used
    printHorizontalLine();
    std::cout<<"Use Bench Boost: "<<(suggestedTeamChanges->isBenchBoostRecommended())<<std::endl;
    std::cout<<"Use Triple Captain: "<<(suggestedTeamChanges->isTripleCaptainRecommended())<<std::endl;
    printHorizontalLine();
}


bool shouldImplementTeamChanges(){
    std::cout<<"Would you like the suggested changes to be implemented?"<<std::endl;
    std::cout<<"if yes: PRESS 1, otherwise PRESS 0"<<std::endl;
    bool implement;
    std::cin>>implement;
    return implement;
}

void implementTeamChanges(std::shared_ptr<Team::Changes> suggestedTeamChanges){
    std::cout<<"implementing changes"<<std::endl;
    //TODO: invoke call to python selenium script to implement desired changes
};


void verifyGameWeekDifficultyUpdate(){
    std::cout<<"Have you updated gameweek difficulties in your database?\n If yes, PRESS 1 otherwise PRESS 0"<<std::endl;
    bool gameweekdifficultiesHaveBeenUpdated;
    std::cin>>gameweekdifficultiesHaveBeenUpdated;
    if(!gameweekdifficultiesHaveBeenUpdated) throw miscellaneous_exception("[Exception] You need to update gameweek difficulties");
   
}
}//! namespace fantasypremierleague
