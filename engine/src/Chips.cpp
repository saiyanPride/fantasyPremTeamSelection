
#include "Chips.hpp"

namespace FantasyPremTeamSelection{
std::map<std::string,std::string> parseStatusJson(std::string myJson){
    size_t jsonSize=myJson.size();
    int currentCharIndex=0;
    int start,end,currentDelimeterInd=0;
    const char delimeters[4]={'"','"',':',','};//note the last key/value pair of the JSON terminates with a '}' and not a ',' unlike the other key/value pairs
    std::string key,value;
    std::map<std::string,std::string> parsedJson;

    while(currentCharIndex < jsonSize && myJson[currentCharIndex] != '}'){ //extract all key value pairs iteratively till end of json string
        /*extract next JSON object {key, value} pair from Json and store in `parsedJson` map in each iteration
            - To extract the desired data e.g. noFreeTransfers, determine the index of each delimeter in delimeters
            - then using the indexes extract the relevant substrings from the overall Json string
        */
            auto getVal = [&](int& resultStore) {
                while(currentCharIndex < jsonSize &&  myJson[currentCharIndex] != '}' && myJson[currentCharIndex]!= delimeters[currentDelimeterInd]) ++currentCharIndex; //determine index of next delimeter
                
                if( myJson[currentCharIndex] == delimeters[currentDelimeterInd] || myJson[currentCharIndex] == '}' ) {//above loop terminated because desired delimeter was found
                    // || myJson[currentCharIndex] == '}' because the last key/value pair of then JSON object terminates with a '}' and not a ',' unlike the other key/value pairs
                    resultStore=currentCharIndex;
                    ++currentDelimeterInd;//next search should be for next delimeter
                    ++currentCharIndex;//starting position for next delimeter search should be from next character
                }
                else throw miscellaneous_exception("json file has syntax error");
            };

            getVal(start);//update `start` with the index of the double quote preceding the first char of the desired key
            getVal(end);//update `end` with the index of the double quote immediately following the last char of the desired key
            key=myJson.substr(start+1,end-start-1);  //end-start-1 is the no of chars enclosed by double quotes in the JSON

            //extract the corresponding value to `key` similarly
            getVal(start);
            getVal(end);
            value=myJson.substr(start+1,end-start-1);

            parsedJson[key]=value;    
            currentDelimeterInd=0;//reset so next iteration searches for next key enclosed by double quotes   
    }
    return parsedJson;
}


std::unique_ptr<Chips> Chips::myChips(nullptr); //initialise static variable

std::unique_ptr<Chips>& Chips::getChips()
{
    if (Chips::myChips.get() == nullptr) Chips::myChips.reset(new Chips());
    return Chips::myChips;
}

Chips::Chips()
{
    update();
    displayChips();
}


void Chips::update()
{//TODO(very low priority): switch data source to database
    //open the status json file
    std::ifstream statusFile("../../dataRetriever/status.json"); //attempt to open file
    std::string jsonString;
    if (statusFile.is_open()){
        std::getline(statusFile,jsonString);
        statusFile.close();
        auto jsonMap = parseStatusJson(jsonString);

        auto removeWhiteSpace=[](std::string value){
            std::string result;
            for(const char& character : value ){
                if(character != ' ') result+=character;
            }
            return result;
        };
        
        //assign initial values to data members
        noFreeTransfers=std::stoi(jsonMap["noFreeTransfersAvailable"]);
        wildCardExists=( removeWhiteSpace(jsonMap["isWildCardAvailable"]).compare("true")==0 ) ? true:false;
        tripleCaptainExists=( removeWhiteSpace(jsonMap["isTripleCaptainAvailable"]).compare("true") ==0 )? true:false;
        freeHitExists=( removeWhiteSpace(jsonMap["isFreehitAvailable"])=="true" )?true:false;     
        benchBoostExists=( removeWhiteSpace(jsonMap["isBenchBoostAvailable"])=="true" ) ? true:false;
    }else{
        std::printf("[ERROR]: could not find status file \n");
    }  
}

int8_t Chips::getNoAvailableFreeTransfers() const
{
    return noFreeTransfers;
}
bool Chips::doesWildCardExist() const
{
    return wildCardExists;
}
bool Chips::doesFreeHitExist() const
{
    return freeHitExists;
}

bool Chips::doesTripleCaptainExist() const
{
    return tripleCaptainExists;
}
bool Chips::doesBenchBoostExist() const
{
    return benchBoostExists;
}

void Chips::displayChips() const{
    auto convertToString = [] (bool chip){ return chip ? "Yes":"No";};
    printf("[Info] Displaying chip status\n[Info] ");
    printf("{noFreeTransfers: %d}; ",noFreeTransfers);
    printf("{wildCardExists: %s}; ",convertToString(wildCardExists));
    printf("{freeHitExists: %s}; ",convertToString(freeHitExists));
    printf("{tripleCaptainExists: %s}; ",convertToString(tripleCaptainExists));
    printf("{benchBoostExists: %s};\n",convertToString(benchBoostExists));
}
}//!namespace FantasyPremTeamSelection