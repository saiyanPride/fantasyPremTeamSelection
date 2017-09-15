
#include "Chips.hpp"
Chips *Chips::singleton = nullptr;

Chips &Chips::getChips()
{
    if (singleton == nullptr)
        singleton = new Chips();
    return *singleton;
}
Chips::Chips()
{
    update();
}
Chips::~Chips()
{
    if(singleton!=nullptr) delete singleton;
}

void Chips::update()
{
    //TODO2
    //update availability/status of all chips
    //throw exception if unsuccessful
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