ProjectRootDirectory=/Users/NiranPyzzle/Documents/softwareProjects/fantasyPremTeamSelection/engine
echo "[INFO] Switching to src directory"
cd $ProjectRootDirectory/src

echo "[INFO] Setting up Environment"
MySQLConnectorIncludePath=$ProjectRootDirectory/lib/mysql-connector-c++-1.1.7-osx10.10-x86-64bit
ExecutablePath=$ProjectRootDirectory/bin/fantasyAnalytics.exe
SourceFiles="main.cpp ProprietaryAlgorithms.cpp Team.cpp Settings.cpp Chips.cpp Player.cpp fantasyExceptions.cpp"
export DYLD_LIBRARY_PATH=$MySQLConnectorIncludePath/lib #makes sure the MySQL C++ connector dynamic library, can be found at runtime

echo "[INFO] Building binary"
g++ -std=c++14 -o $ExecutablePath $SourceFiles -I$MySQLConnectorIncludePath/include -I/Users/NiranPyzzle/Documents/boost/include -L$MySQLConnectorIncludePath/lib -lmysqlcppconn
echo "[INFO] build complete"

echo "[INFO] Executing binary"
$ExecutablePath