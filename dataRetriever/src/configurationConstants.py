from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

PhantomJSExecutablePath = r'/Users/NiranPyzzle/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs'
driver = webdriver.PhantomJS(executable_path=PhantomJSExecutablePath)
# driver = webdriver.Firefox(executable_path=r'/Users/NiranPyzzle/Downloads/geckodriver') // use firefox visualise process in browser GUI
wait = WebDriverWait(driver, 30)
waitIntervalForStatisticsPageChange_secs = 1
waitIntervalForGeneralPageChanges = 3
waitIntervalToSimulateHumanUser = 10
minNoPlayerPerPage = 16
gameweekNo = 0
noPremierLeagueTeams = 20
noGWDifficultiesToExtract = 5
noStartingPlayers = 11
noSubs = 4
# css selectors
lastPageAnchorElementSelector = '#ismr-main > div > div.paginationContainer.ism-pagination > \
                    a.paginationBtn.ismjs-change-page.ism-pagination__button.ism-pagination__button--secondary'  # it's href attribute has the number of pages href='#17'

# MyTeam page css selectors

benchBoostButtonSelector = '#ismr-chips > ul > li:nth-child(1) > div > button'
# unused freehit selector -> '#ismr-chips > ul > li:nth-child(2) > div > button'
freehitButtonSelector = '#ismr-chips > ul > li:nth-child(2) > div > a > div.ism-button--chip--played__title'
ithPlayerInCurrentTeamNameSelector = "#ismr-detail > div > div:nth-child(%d) > div > table > tbody > tr:nth-child(%d) > td.ism-table--el__primary > div > div.ism-media__body.ism-table--el__primary-text > a"
ithPlayerInCurrentTeamClubShortNameSelector = "#ismr-detail > div > div:nth-child(%d) > div > table > tbody > tr:nth-child(%d) > td.ism-table--el__primary > div > div.ism-media__body.ism-table--el__primary-text > span"
passwordInputElementSelector = '#ismjs-password'
listViewButtonSelector = '#ismr-main > div > section:nth-child(5) > div.ism-squad-wrapper > div > ul > li:nth-child(2) > a'
usernameInputElementSelector = "#ismjs-username"

tripleCaptainButtonSelector = '#ismr-chips > ul > li:nth-child(3) > div > button'
noFreeTransfersElementSelector = '#ismr-scoreboard > div > div.ism-scoreboard > div:nth-child(4) > div > div'
bankBalanceElementSelector = '#ismr-scoreboard > div > div.ism-scoreboard > div:nth-child(6) > div > div'
wildCardAvailabilityElementSelector = '#ismr-scoreboard > div > div.ism-scoreboard > div:nth-child(3) > button'
gameweekNumberElementSelector = '#ismr-scoreboard > div > div.ism-deadline-bar > h4'
playerStatisticsTbodyElementSelector = '#ismr-main > div > div.table.ism-scroll-table > table > tbody'
playerStatisticsNextPageButtonSelector = '#ismr-main > div > div.paginationContainer.ism-pagination > a:nth-child(4)'

# statistics/minutes page css selector templates
playerNameSelectorTemplate = '#ismr-main > div > div.table.ism-scroll-table > table > tbody > tr:nth-child(%s) > td.ism-table--el__primary > div > div.ism-media__body.ism-table--el__primary-text > a'
playerPositionSelectorTemplate = '#ismr-main > div > div.table.ism-scroll-table > table > tbody > tr:nth-child(%s) > td.ism-table--el__primary > div > div.ism-media__body.ism-table--el__primary-text > span.ism-table--el__pos'
playerClubSelectorTemplate = '#ismr-main > div > div.table.ism-scroll-table > table > tbody > tr:nth-child(%s) > td.ism-table--el__primary > div > div.ism-media__body.ism-table--el__primary-text > span.ism-table--el__strong'
playerCostSelectorTemplate = '#ismr-main > div > div.table.ism-scroll-table > table > tbody > tr:nth-child(%s) > td:nth-child(3)'
playerFormSelectorTemplate = '#ismr-main > div > div.table.ism-scroll-table > table > tbody > tr:nth-child(%s) > td:nth-child(5)'
playerMinutesPlayedSelectorTemplate = '#ismr-main > div > div.table.ism-scroll-table > table > tbody > tr:nth-child(%s) > td:nth-child(7)'
PAGE_NUM_START_INDEX_IN_STATISTICS_PAGE_URL = 55
# used to extract goals, assists, bonus, clean sheets from statistics table
fifthColumnValueSelectorTemplate = '#ismr-main > div > div.table.ism-scroll-table > table > tbody > tr:nth-child(%s) > td:nth-child(7)'

# statistics goalkeeper view page css selectors & templates
# presenece of this elements indicates the page has loaded
completeStatsGkPageLoadElementFlagSelector = "#ismr-main > div > div.table.ism-scroll-table > table > tbody > tr:nth-child(30) > td.ism-table--el__status > a > svg"
gkInfoButtonSelectorTemplate = '#ismr-main > div > div.table.ism-scroll-table > table > tbody > tr:nth-child(%s) > td.ism-table--el__status > a > svg'
nthGameWeekDifficultySelector = '#ismr-element-fixtures > div > div > table > tbody > tr:nth-child(%s) > td:nth-child(4)'
# playerGoalsSelectorTemplate
# playerAssistsSelectorTemplate
# playerBonusSelectorTemplate

# urls
fantasyPremierLeagueBaseUrl = "https://fantasy.premierleague.com/"
myTeamUrl = fantasyPremierLeagueBaseUrl + "a/team/my"
transfersPageUrl = fantasyPremierLeagueBaseUrl + "a/squad/transfers"
minutesPlayedStatisticsPageUrl = fantasyPremierLeagueBaseUrl + "a/statistics/minutes"
goalsScoredStatisticsPageUrl = fantasyPremierLeagueBaseUrl + \
    "a/statistics/goals_scored"
assistsStatisticsPageUrl = fantasyPremierLeagueBaseUrl + "a/statistics/assists"
bonusStatisticsPageUrl = fantasyPremierLeagueBaseUrl + "a/statistics/bonus"
cleanSheetsStatisticsPageUrl = fantasyPremierLeagueBaseUrl + \
    "a/statistics/clean_sheets"
goalKeeperViewStatisticsPageUrl = fantasyPremierLeagueBaseUrl + \
    "a/statistics/total_points/et_1"

# database
excelDataBaseName = 'fantasyPlayerData'
excelDataBaseExtension = '.xlsx'
addNewColumnSQL = "ALTER TABLE PlayerStats ADD isFirstTeam tinyint DEFAULT 0"
markPlayerAsCurrentlySelectedSQLTemplate = "UPDATE PlayerStats SET isFirstTeam = %d WHERE Name = '%s' AND Club = '%s' "
GET_GAMEWEEK_DIFFICULTIES_SQL = "SELECT Clubs.Name, FIRST_GW, SECOND_GW, THIRD_GW, FOURTH_GW, FIFTH_GW FROM \
            GameweekDifficulty LEFT JOIN Clubs \
            ON GameweekDifficulty.ClubId = Clubs.ClubId"
DROP_PLAYERSTATS_TABLE_SQL = "DROP TABLE PlayerStats"
CREATE_PLAYERSTATS_TABLE_SQL = "CREATE TABLE PlayerStats (\
    PlayerID int NOT NULL PRIMARY KEY,\
    Club varchar(255),\
    Name varchar(255),\
    Position varchar(255),\
    Value float,\
    Form float,\
    MinutesPlayed int,\
    Goals int,\
    Assists int,\
    Bonus int,\
    Cleansheets int,\
    FirstGameweekScore float,\
    SecondGameweekScore float,\
    ThirdGameweekScore float,\
    FourthGameweekScore float,\
    FifthGameweekScore float, \
    AvgScore float\
    )"

# flags
STARTER = 2
SUBSTITUTE = 1
STARTER_SECTION = 1
SUBSTITUTE_SECTION = 2

# excel database
headers = ['PlayerID', 'Club', 'Name', 'Position', 'Value', 'Form', 'MinutesPlayed', 'Goals', 'Assists',
           'Bonus', 'Cleansheets', 'FirstGameweekScore', 'SecondGameweekScore',
           'ThirdGameweekScore', 'FourthGameweekScore', 'FifthGameweekScore', 'AvgScore']
