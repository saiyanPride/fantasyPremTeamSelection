#!/bin/bash

# this build script can be used to build the executable or run the executable or both
# sample usage:
# 'build.sh - b' -> build executable only
# 'build.sh - r' -> run executable only
# 'build.sh - a' -> perform all tasks i.e. build then run executable

ScriptName=`basename "$0"`
EngineDirectory=/Users/NiranPyzzle/Documents/softwareProjects/fantasyPremTeamSelection/engine
MySQLConnectorIncludePath=$EngineDirectory/lib/mysql-connector-c++-1.1.7-osx10.10-x86-64bit
ExecutablePath=$EngineDirectory/bin/fantasyAnalytics.exe
SourceFiles="main.cpp ProprietaryAlgorithms.cpp Team.cpp Settings.cpp Chips.cpp Player.cpp fantasyExceptions.cpp"

buildExecutable() {
    info "switching to src directory"
    cd $EngineDirectory/src
    info "building executable"
    g++ -std=c++14 -o $ExecutablePath $SourceFiles -I$MySQLConnectorIncludePath/include -I/Users/NiranPyzzle/Documents/boost/include -L$MySQLConnectorIncludePath/lib -lmysqlcppconn
    info "build complete"
}
 

runExecutable() {
    info "setting up Environment"
    export DYLD_LIBRARY_PATH=$MySQLConnectorIncludePath/lib #makes sure the MySQL C++ connector dynamic library, can be found at runtime
    info "executing binary"
    $ExecutablePath
}

buildExecutableThenRun() {
    buildExecutable
    runExecutable
}

info(){
    echo [$ScriptName:INFO] $1
}

#read arguments & respond accordingly
# the argument processor is located after the functions, otherwise it won't find them
while getopts "rba" opt; do
  case $opt in
    r)
      runExecutable
      ;;
    b)
      buildExecutable
      ;;
    a)
      buildExecutableThenRun
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done
