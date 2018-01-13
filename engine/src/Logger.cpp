#include "Logger.hpp"
void info(const char* message){
    std::cout<<"[INFO] "<<message<<std::endl;
}

void warn(const char* message){
    std::cout<<"[WARNING] "<<message<<std::endl;
}