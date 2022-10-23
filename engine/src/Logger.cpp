#include "Logger.hpp"
void info(const char* message){
    std::cout<<"[INFO] "<<message<<std::endl;
}

void warn(const char* message){
    std::cout<<"[WARNING] "<<message<<std::endl;
}

void error(const char* message){
    std::cout<<"[ERROR] "<<message<<std::endl;
}

void error(const std::string& message){
    std::cout<<"[ERROR] "<<message<<std::endl;
}