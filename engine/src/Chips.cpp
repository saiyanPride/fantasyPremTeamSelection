
#include "Chips.hpp"

typedef std::map<std::string,std::string> JsonObject;
using namespace std;
JsonObject parseStatusJson(std::string myJson){
    size_t jsonSize=myJson.size();
    int currentCharIndex=0;
    int start,end,currentDelimeterInd=0;
    const char delimeters[4]={'"','"',':',','};
    std::string key,value;
    JsonObject parsedJson;

    while(currentCharIndex < jsonSize && myJson[currentCharIndex] != '}'){ //extract all key value pairs iteratively till end of json string
        //extract next key
            auto getVal = [&](int& resultStore) {
                while(currentCharIndex < jsonSize && (myJson[currentCharIndex]!= delimeters[currentDelimeterInd] && myJson[currentCharIndex] != '}')) ++currentCharIndex; //determine index of next delimeter
                if( myJson[currentCharIndex] == delimeters[currentDelimeterInd] || myJson[currentCharIndex] == '}' ) {
                    resultStore=currentCharIndex;
                    ++currentDelimeterInd;//next search should be for next delimeter
                    ++currentCharIndex;//starting position for next delimeter search should be from net character
                }
                else throw miscellaneous_exception("json file has syntax error");
            };

            getVal(start);
            getVal(end);
            key=myJson.substr(start+1,end-start-1);  
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
}


void Chips::update()
{
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
        noFreeTransfers=atoi(jsonMap["noFreeTransfersAvailable"].c_str());
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
    auto isChipAvailableStr = [] (bool chip){ return chip ? "Yes":"No";};
    printf("[Info] Displaying chip status\n[Info] ");
    printf("{noFreeTransfers: %d}; ",noFreeTransfers);
    printf("{wildCardExists: %s}; ",isChipAvailableStr(wildCardExists));
    printf("{freeHitExists: %s}; ",isChipAvailableStr(freeHitExists));
    printf("{tripleCaptainExists: %s}; ",isChipAvailableStr(tripleCaptainExists));
    printf("{benchBoostExists: %s};\n",isChipAvailableStr(benchBoostExists));
}