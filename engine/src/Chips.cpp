
#include "Chips.hpp"

namespace fantasypremierleague
{
int8_t Chips::getNoAvailableFreeTransfers() const
{
    return noFreeTransfers;
}
bool Chips::doesWildCardChipExist() const
{
    return wildCardExists;
}
bool Chips::doesFreeHitChipExist() const
{
    return freeHitExists;
}

bool Chips::doesTripleCaptainChipExist() const
{
    return tripleCaptainExists;
}
bool Chips::doesBenchBoostChipExist() const
{
    return benchBoostExists;
}

std::shared_ptr<Chips> Chips::myChips(nullptr); //initialise static variable

std::shared_ptr<Chips> &Chips::getChips()
{
    if (Chips::myChips.get() == nullptr)
        Chips::myChips.reset(new Chips());
    return Chips::myChips;
}

Chips::Chips()
{
    update();
    displayChips();
}

// parseStatusJson extracts the status of all chips by parsing a JSON file
// The algorithm determines key, value pairs as follows:
//  - keys are enclosed between quotation marks e.g. "<key>"
//  - values (excluding the last value) are enclosed between a colon and a comma,
//  - the last value is enclosed between a colon and a closing brace
// A std::unordered_map<std::string, std::string> of key-value pairs is returned
std::unordered_map<std::string, std::string> parseStatusJson(std::string &myJson)
{
    size_t jsonSize = myJson.size();
    size_t currentCharIndex = 0; // search starts from beginning of the file
    std::string key, value;
    std::unordered_map<std::string, std::string> keyValuePairs; // the extracted key-value pairs

    auto getIndexOfNextDelimeterOccurence = [&](const char &delimeter) -> size_t {
        // starting from the `currentCharIndex` search for the next occurence of a delimeter
        while (currentCharIndex < jsonSize && myJson[currentCharIndex] != '}' && myJson[currentCharIndex] != delimeter)
        { //search for the delimeter or '}'
            ++currentCharIndex;
        }

        if (myJson[currentCharIndex] == delimeter || myJson[currentCharIndex] == '}')
        {                              // delimeter was found or end of file reached
            return currentCharIndex++; //post incremented so that next search will start from the next char
        }
        else
        {
            throw miscellaneous_exception("Delimiter was not found");
        }
    };
    auto getSubstringEnclosedByDelimeters = [&myJson, &getIndexOfNextDelimeterOccurence](const char &startDelimeter, const char &endDelimeter) { //gets the next key or value, whichever comes first
        size_t start = getIndexOfNextDelimeterOccurence(startDelimeter);
        size_t end = getIndexOfNextDelimeterOccurence(endDelimeter);
        return myJson.substr(start + 1, end - start - 1);
    };
    // extract all key value pairs
    while (currentCharIndex < jsonSize)
    {
        key = getSubstringEnclosedByDelimeters('"', '"');   // extract the next key
        value = getSubstringEnclosedByDelimeters(':', ','); //extract the next value
        keyValuePairs[key] = value;
    }
    return keyValuePairs;
}

void Chips::update()
{ //TODO(very low priority): switch data source to database
    //open the status json file
    std::ifstream statusFile(STATUS_FILE_PATH); //attempt to open file
    std::string jsonString;
    if (statusFile.is_open())
    {
        std::getline(statusFile, jsonString);
        statusFile.close();
        auto statusHashTable = parseStatusJson(jsonString);

        auto removeWhiteSpace = [](std::string &word) {
            word.erase(std::remove_if(word.begin(), word.end(), [](const char &character) { return character == ' '; }),
                       word.end());
        };

        for (auto &statusEntry : statusHashTable)
            removeWhiteSpace(statusEntry.second);

        //set status of chips
        noFreeTransfers = std::stoi(statusHashTable["noFreeTransfersAvailable"]);
        wildCardExists = (statusHashTable["isWildCardAvailable"].compare("true") == 0) ? true : false;
        tripleCaptainExists = (statusHashTable["isTripleCaptainAvailable"].compare("true") == 0) ? true : false;
        freeHitExists = (statusHashTable["isFreehitAvailable"] == "true") ? true : false;
        benchBoostExists = (statusHashTable["isBenchBoostAvailable"] == "true") ? true : false;
    }
    else
    {
        std::printf("[ERROR]: could not find status file \n");
    }
}

void Chips::displayChips() const
{
    auto convertToString = [](bool chip) { return chip ? "Yes" : "No"; };
    printf("[Info] Displaying chip status\n[Info] ");
    printf("{noFreeTransfers: %d}; ", noFreeTransfers);
    printf("{wildCardExists: %s}; ", convertToString(wildCardExists));
    printf("{freeHitExists: %s}; ", convertToString(freeHitExists));
    printf("{tripleCaptainExists: %s}; ", convertToString(tripleCaptainExists));
    printf("{benchBoostExists: %s};\n", convertToString(benchBoostExists));
}
} //!namespace fantasypremierleague