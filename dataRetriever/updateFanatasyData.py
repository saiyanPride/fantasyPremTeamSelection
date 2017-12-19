# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
import datetime
import xlsxwriter
from xlrd import open_workbook
from customDataStructures import Status
from customDataStructures import PlayerData
from pprint import pprint
from itertools import izip
import sqlDatabase

#TODO: switch to the dataRetriever directory
#driver = webdriver.Firefox(executable_path=r'/Users/NiranPyzzle/Downloads/geckodriver')
driver = webdriver.PhantomJS(
    executable_path=r'/Users/NiranPyzzle/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')
driver.get("https://fantasy.premierleague.com/")
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

#MyTeam page css selectors

benchBoostButtonSelector = '#ismr-chips > ul > li:nth-child(1) > div > button'
freehitButtonSelector = '#ismr-chips > ul > li:nth-child(2) > div > a > div.ism-button--chip--played__title'# unused freehit selector -> '#ismr-chips > ul > li:nth-child(2) > div > button'
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
# used to extract goals, assists, bonus, clean sheets from statistics table
fifthColumnValueSelectorTemplate = '#ismr-main > div > div.table.ism-scroll-table > table > tbody > tr:nth-child(%s) > td:nth-child(7)'

#statistics goalkeeper view page css selectors & templates
completeStatsGkPageLoadElementFlagSelector = "#ismr-main > div > div.table.ism-scroll-table > table > tbody > tr:nth-child(30) > td.ism-table--el__status > a > svg" #presenece of this elements indicates the page has loaded
gkInfoButtonSelectorTemplate = '#ismr-main > div > div.table.ism-scroll-table > table > tbody > tr:nth-child(%s) > td.ism-table--el__status > a > svg'
nthGameWeekDifficultySelector = '#ismr-element-fixtures > div > div > table > tbody > tr:nth-child(%s) > td:nth-child(4)'
# playerGoalsSelectorTemplate
# playerAssistsSelectorTemplate
# playerBonusSelectorTemplate
# urls
myTeamUrl="https://fantasy.premierleague.com/a/team/my"
transfersPageUrl = "https://fantasy.premierleague.com/a/squad/transfers"
minutesPlayedStatisticsPageUrl = "https://fantasy.premierleague.com/a/statistics/minutes"
goalsScoredStatisticsPageUrl = "https://fantasy.premierleague.com/a/statistics/goals_scored"
assistsStatisticsPageUrl = "https://fantasy.premierleague.com/a/statistics/assists"
bonusStatisticsPageUrl = "https://fantasy.premierleague.com/a/statistics/bonus"
cleanSheetsStatisticsPageUrl = "https://fantasy.premierleague.com/a/statistics/clean_sheets"
goalKeeperViewStatisticsPageUrl = "https://fantasy.premierleague.com/a/statistics/total_points/et_1"

#database
excelDataBaseName = 'fantasyPlayerData'
excelDataBaseExtension = '.xlsx'

# global data structures
startingLineup = [] # elements are of form "<PlayerName>;<Club>"
substitutes = [] # elements are of form "<PlayerName>;<Club>"

def login(username, password):
    # TODO (low priority): make sure arguments are strings
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, usernameInputElementSelector)))
    # find username field and send keys
    elem = driver.find_element_by_css_selector(usernameInputElementSelector)
    elem.send_keys(username)
    # find password field and send keys
    elem = driver.find_element_by_css_selector(passwordInputElementSelector)
    elem.send_keys(password)
    # hit enter
    elem.send_keys(Keys.RETURN)


def updateCurrentTeam():
    """
    Determine current members of your team, and update the datastore to reflect this
    """
    print("[INFO] updating current team")
    # validate current page is team url
    if driver.current_url != myTeamUrl:
        driver.get(myTeamUrl)

    #switch to list view so you can select your player's clubs, pitch view only shows the next opposition club for your players
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, listViewButtonSelector)))
    listViewButton = driver.find_element_by_css_selector(listViewButtonSelector)
    listViewButton.click()

    
    def getPlayerDetailsForPlayer(i, resultStore,flag):
        """
        Stores the details of the ith player in your team in the provided data structure
        i: refers to the ith player, and is used to generate the css selector for the ith player's name and club
        resultStore: data structure where player details will be stored
        flag: use 1 if player is a starter & 2 if player is a substitute
        """
        # wait for presence of player name element selectors
        playerNameSelector = ithPlayerInCurrentTeamNameSelector % (flag,i)
        clubNameSelector = ithPlayerInCurrentTeamClubShortNameSelector % (flag,i)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, playerNameSelector)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, clubNameSelector)))
        # extract name
        playerName = driver.find_element_by_css_selector(playerNameSelector).text
        clubShortName = driver.find_element_by_css_selector(clubNameSelector).text
        
        resultStore.append(playerName+';'+clubShortName)

    print("[INFO] Determining starting lineup")
    for i in range(1,noStartingPlayers+1):
        getPlayerDetailsForPlayer(i,startingLineup,1)

    print("[INFO] Determining substitutes")
    for i in range(1,noSubs+1):
        getPlayerDetailsForPlayer(i,substitutes,2)

    addNewColumnSQL = "ALTER TABLE PlayerStats ADD isFirstTeam tinyint DEFAULT 0"
    sqlDatabase.cursor.execute(addNewColumnSQL)
    markPlayerAsCurrentlySelectedSQLTemplate = "UPDATE PlayerStats SET isFirstTeam = %d WHERE Name = '%s' AND Club = '%s' "

    def setIsFirstTeamValueInDB(playerList, value):
        for element in playerList:
            playerData = element.split(";")
            sqlStatement = markPlayerAsCurrentlySelectedSQLTemplate % (value,playerData[0], playerData[1])
            #print("[INFO] executing %s" % sqlStatement)
            sqlDatabase.cursor.execute(sqlStatement)
    print("[INFO] Updating database to reflect current members of team")
    setIsFirstTeamValueInDB(startingLineup,2) # mark first team with flag of 2  
    setIsFirstTeamValueInDB(substitutes,1) # mark substitutes with flag of 1]
    sqlDatabase.connection.commit()

def getStatus():
    # expectation is that current page is MyTeam
    chipAvailability = [False, False, False]

    cssSelectors = [benchBoostButtonSelector,
                    freehitButtonSelector, tripleCaptainButtonSelector]

    """
    Navigate to MyTeam page and determine the status of 
    1) BenchBoost
    2) Free hit
    3) Triple Captain
    """
    driver.get(myTeamUrl)
    for index, selector in enumerate(cssSelectors):
        print("[INFO] waiting for presence of selector")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        elem = driver.find_element_by_css_selector(selector)
        chipAction = elem.text
        if chipAction == 'PLAY':
            chipAvailability[index] = True

    benchBoostAvailable = chipAvailability[0]
    freehitAvailable = chipAvailability[1]
    tripleCaptainAvailable = chipAvailability[2]
    chipResult = "benchBoostAvailable:%r \nfreehitAvailable: %r \ntripleCaptainAvailable:%r" % (
        benchBoostAvailable, freehitAvailable, tripleCaptainAvailable)
    print chipResult



    """
    Navigate to transfers page and determine status of 
    1) Free transfers
    2) Bank balance
    3) Wild card
    4) Gameweek number
    """

    otherStatusSelectors = [noFreeTransfersElementSelector,
                            bankBalanceElementSelector,
                            wildCardAvailabilityElementSelector,
                            gameweekNumberElementSelector]
    driver.get(transfersPageUrl)
    retrievedText = []

    for index, selector in enumerate(otherStatusSelectors):
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            elem = driver.find_element_by_css_selector(selector)
            text = elem.text
            retrievedText.insert(index, text)
        except:
            if selector == wildCardAvailabilityElementSelector:
                retrievedText.insert(index, "unavailable")
            else: 
                raise             

    noFreeTransfers = int(retrievedText[0])
    # TODO: simplify
    bankBalance = ((float(retrievedText[1][1:]) * 10) // 1) / 10
    wildCardAvailable = False
    if retrievedText[2] == 'Play Wildcard':
        wildCardAvailable = True
    gameweekNo = int(retrievedText[3][9:11]) #TODO: make generic so that it works if gameweek is single digit or double digit, could use the expected size of the string to deduce

    # use retrieved information to instantiate status object
    result = "noFreeTransfers: %s \nbankBalance GBP: %f \nGameweek number: %s" % (
        noFreeTransfers, bankBalance, gameweekNo)
    print (result)
    if (wildCardAvailable):
        print "Wild card is available"

    status = Status(wildCardAvailable, freehitAvailable, tripleCaptainAvailable, benchBoostAvailable, noFreeTransfers, bankBalance, gameweekNo)
    statusJson=status.getJson()
    statusFile=open('status.json','w')
    statusFile.write(statusJson)
    statusFile.close()
    return status

def updatePlayerData(gameweekNo):
    # create map
    playersMap = {}  # key is playerName-Club-Position, value is Player object
    # navigate to statisitcs.minute
    driver.get(minutesPlayedStatisticsPageUrl)
    # determine number of pages and thus the number of times one needs to switch to next page
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, lastPageAnchorElementSelector)))
    numberPlayerStatisticPagesElem = driver.find_element_by_css_selector(
        lastPageAnchorElementSelector)
    totalNumberOfPages = int((numberPlayerStatisticPagesElem.get_attribute(
        'href')[55:]))  # page number starts from the 56th character in url
    lastPage = totalNumberOfPages - 1  # 0 indexed for use in loop

    print("[INFO] Extracting data from minutes played page")  # DEbug
    # Extract data from statistics/minutes page
    for pageNo in range(totalNumberOfPages):
        if pageNo == lastPage:
            # allow extra time for other rows to load
            driver.implicitly_wait(waitIntervalForStatisticsPageChange_secs)
        else:
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, playerMinutesPlayedSelectorTemplate % (
                    minNoPlayerPerPage))))  # wait for data in table to appear in each iteration
            except TimeoutException:
                print (
                    "timed out in page %s of stats, now applying time delay" % (pageNo))
                driver.implicitly_wait(
                    waitIntervalForStatisticsPageChange_secs)
        tbodyElem = driver.find_element_by_css_selector(
            playerStatisticsTbodyElementSelector)

        # determine the number of players on the page i.e. the no of child <tr> tags of <tbody>
        numberOfPlayersOnPage = tbodyElem.get_property('childElementCount')
        for playerDataRow in range(1, numberOfPlayersOnPage + 1):
            try:
                playerName = driver.find_element_by_css_selector(
                    playerNameSelectorTemplate % (playerDataRow)).text
                playerPosition = driver.find_element_by_css_selector(
                    playerPositionSelectorTemplate % (playerDataRow)).text
                playerClub = driver.find_element_by_css_selector(
                    playerClubSelectorTemplate % (playerDataRow)).text
                playerCost = float((driver.find_element_by_css_selector(
                    playerCostSelectorTemplate % (playerDataRow)).text)[1:])  # GBP is dropped
                playerForm = float(driver.find_element_by_css_selector(
                    playerFormSelectorTemplate % (playerDataRow)).text)
                playerMinutesPlayed = int(driver.find_element_by_css_selector(
                    playerMinutesPlayedSelectorTemplate % (playerDataRow)).text)

                # instantiate & store Player object in hash table
                key = playerName + playerClub + playerPosition
                playersMap[key] = PlayerData(
                    playerClub, playerName, playerPosition, playerCost, playerForm, playerMinutesPlayed)
            except:
                print("issue with row %s of page %s" %
                      (playerDataRow, pageNo))  # DEBUG
        if pageNo != lastPage:
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, playerStatisticsNextPageButtonSelector)))
            driver.find_element_by_css_selector(
                playerStatisticsNextPageButtonSelector).click()  # go to next page

    print("Done with minutes played page data")  # debug
    pageTypeUrls = [goalsScoredStatisticsPageUrl, assistsStatisticsPageUrl,
                    bonusStatisticsPageUrl, cleanSheetsStatisticsPageUrl]
    # functions for updating player objects

    def updateGoals(Player, goals): Player.goals = int(goals)

    def updateAssists(Player, assists): Player.assists = int(assists)

    def updateBonus(Player, bonus): Player.bonus = int(bonus)

    def updateCleanSheets(
        Player, cleansheets): Player.cleansheets = int(cleansheets)
    playerDataUpdateFunctions = [updateGoals,
                                 updateAssists, updateBonus, updateCleanSheets]

    print("[INFO] Extracting data (goals scored, assists, bonus, clean sheets) from relevant pages")  # debug
    # Extract goals scored, assists, bonus, clean sheets
    for pageUrl, playerDataUpdateFunction in izip(pageTypeUrls, playerDataUpdateFunctions):
        driver.get(pageUrl)
        for pageNo in range(totalNumberOfPages):
           # print("[DEBUG] page %s" % (pageNo))  # DEBUG
            if pageNo == lastPage:
                # allow extra time for other rows to load
                driver.implicitly_wait(
                    waitIntervalForStatisticsPageChange_secs)
            else:
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, fifthColumnValueSelectorTemplate % (
                        minNoPlayerPerPage))))  # wait for data in table to appear in each iteration
                except TimeoutException:
                    print (
                        "timed out in page %s of stats, now applying time delay" % (pageNo))
                    driver.implicitly_wait(
                        waitIntervalForStatisticsPageChange_secs)
            tbodyElem = driver.find_element_by_css_selector(
                playerStatisticsTbodyElementSelector)
            numberOfPlayersOnPage = tbodyElem.get_property('childElementCount')

            # loop through each row and update relevant page data for corresponding player
            for playerDataRow in range(1, numberOfPlayersOnPage + 1):
                playerName = driver.find_element_by_css_selector(
                    playerNameSelectorTemplate % (playerDataRow)).text
                playerPosition = driver.find_element_by_css_selector(
                    playerPositionSelectorTemplate % (playerDataRow)).text
                playerClub = driver.find_element_by_css_selector(
                    playerClubSelectorTemplate % (playerDataRow)).text
                key = playerName + playerClub + playerPosition
                extractedData = driver.find_element_by_css_selector(
                    fifthColumnValueSelectorTemplate % (playerDataRow)).text
                # update corresponding player object with extracted data
                playerDataUpdateFunction(
                    playersMap[key], extractedData)
            if pageNo != lastPage:
                wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, playerStatisticsNextPageButtonSelector)))
                driver.find_element_by_css_selector(
                    playerStatisticsNextPageButtonSelector).click()  # go to next page

    print("Done Extracting data from other pages")  # debug
    updatePlayerScores(playersMap, gameweekNo)
    return playersMap

def getGameWeekDifficulties():
    #will break if excel file format changes
    print("[INFO] Extracting gameweek difficulties from excel")
    wb = open_workbook('gameweekDifficulties.xls')
    sheet = wb.sheets()[0]
    noRows = sheet.nrows
    noCols = sheet.ncols
    gameweekDifficultiesMap = {}
    print("[INFO] There are %d columns in the sheet" % noCols)
    for row in range(1,noRows):
        clubCode = sheet.cell(row,0).value

        #store gameweek difficulties for all clubs in map
        gameWeekDifficulties = []
        for col in range(1,noGWDifficultiesToExtract+1):
            gameWeekDifficulties.append(sheet.cell(row,col).value)

        gameweekDifficultiesMap[clubCode] = gameWeekDifficulties
        row +=1
    # no need to explicitly call wb.close()
    return gameweekDifficultiesMap

def updatePlayerScores(playersMap, gameweekNo):
    print("[INFO]updating player scores")  # DEBUG
    gameweekDifficultyByClubMap = {}

    # query database for gameweek difficulties
    sqlDatabase.cursor.execute("SELECT Clubs.Name, FIRST_GW, SECOND_GW, THIRD_GW, FOURTH_GW, FIFTH_GW FROM \
            GameweekDifficulty LEFT JOIN Clubs \
            ON GameweekDifficulty.ClubId = Clubs.ClubId")
    row = sqlDatabase.cursor.fetchone()

    # store the gameweek difficulties (for the next 5 matches) for each club in a list
    while row:
        gameWeekDifficultiesForClub = row[1:6]
        gameweekDifficultyByClubMap[str(row[0])] = gameWeekDifficultiesForClub
        row = sqlDatabase.cursor.fetchone()

     # estimate player scores
    for key, player in playersMap.items():
        player.getGameweekScoreEstimates(
            gameweekDifficultyByClubMap[player.club], gameweekNo)
"""
Excel version
def updatePlayerScores(playersMap, gameweekNo):    
    gameweekDifficultyByClubMap = getGameWeekDifficulties()
    print("[INFO] Calculating player scores")
    for key, player in playersMap.items():
        player.getGameweekScoreEstimates(
            gameweekDifficultyByClubMap[player.club], gameweekNo)
"""

def updateExcelSheetWithPlayers(playersMap): 
    now = datetime.datetime.now()
    fileNameDateTimeSuffix = "_%d_%d_%d_%d_%d_%d"%(now.year,now.month,now.day,now.hour,now.minute,now.second)
    excelDataBasePath = excelDataBaseName+fileNameDateTimeSuffix+excelDataBaseExtension
    workbook = xlsxwriter.Workbook(excelDataBasePath)
    worksheet = workbook.add_worksheet()
    print("[INFO] Attempting to write player data to excel file named %s" % excelDataBasePath) 
    row = 1
    col = 0

    # create header row
    headers = ['PlayerID','Club','Name','Position','Value','Form','MinutesPlayed','Goals','Assists',
    'Bonus','Cleansheets','FirstGameweekScore','SecondGameweekScore',
    'ThirdGameweekScore','FourthGameweekScore','FifthGameweekScore','AvgScore']

    for colNo, header in enumerate(headers):
        worksheet.write(0, colNo, header)

    # write player data
    for player in playersMap.values():
        scores = player.gameweekScores
        firstGwScore = scores[0]
        secondGwScore = scores[1]
        thirdGwScore = scores[2]
        fourthGwScore = scores[3]
        fifthGwScore = scores[4]
        avgScore = sum(scores)/len(scores)
        
        playerDataList = [row, player.club, player.name, player.position, player.value, player.form, player.minutesPlayed, player.goals, player.assists, player.bonus, player.cleansheets,
                                      firstGwScore, secondGwScore, thirdGwScore, fourthGwScore, fifthGwScore,avgScore]
        for colNo, playerStat in enumerate(playerDataList):
            worksheet.write(row, colNo, playerStat)
        row += 1
    workbook.close() 

def updateDatabaseWithPlayers(playersMap):
    #TODO: make the database connection comply with RAII pattern
    sqlDatabase.cursor.execute("DROP TABLE PlayerStats")
    sqlDatabase.cursor.execute("CREATE TABLE PlayerStats (\
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
        )")
    id = -1
    defaultIsFirstTeamValue = 0 # 0 meaning not on team
    for key, player in playersMap.items():
        id += 1
        scores = player.gameweekScores
        firstGwScore = scores[0]
        secondGwScore = scores[1]
        thirdGwScore = scores[2]
        fourthGwScore = scores[3]
        fifthGwScore = scores[4]
        avgScore = sum(scores)/len(scores)
        sqlDatabase.cursor.execute("INSERT INTO PlayerStats VALUES (%d,'%s','%s','%s',%f,%f,%d,%d,%d,%d,%d,%f,%f,%f,%f,%f,%f)"
                                   % (id, player.club, player.name, player.position, player.value, player.form, player.minutesPlayed, player.goals, player.assists, player.bonus, player.cleansheets,
                                      firstGwScore, secondGwScore, thirdGwScore, fourthGwScore, fifthGwScore,avgScore))
        sqlDatabase.connection.commit()


def applyTimeDelay(interval):
    print("time delay of %d s" % (interval))
    time.sleep(interval)

def updateGameWeekDifficulty():
    #navigate to statistics Goalkeeper view page
    applyTimeDelay(5)
    print("navigating to stats page")
    driver.get(goalKeeperViewStatisticsPageUrl)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, completeStatsGkPageLoadElementFlagSelector)))
    gameWeekDiffcultiesByClubDic = dict()
    noClubsCompleted = 0
    row = 1
    #Extract data for each club
    """
    Each row is visited, and for each row
    One checks if data for the club has already been extracted
    if it hasn't then goalkeeper's info button is clicked on
    and the gameweek difficulty data is extracted
    """
    actions = ActionChains(driver) 
    #navigate to first by info button by pressing tab 16 times       
    actions.send_keys(Keys.TAB * 17)
    print("starting data extraction")
    while noClubsCompleted != noPremierLeagueTeams:
        try:
            print("current row is %s"% (row))
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, playerClubSelectorTemplate % (row))))
            playerClubElem = driver.find_element_by_css_selector(playerClubSelectorTemplate % (row))
            playerClub = playerClubElem.text
            print ("current club is %s"% (playerClub))
            if playerClub not in gameWeekDiffcultiesByClubDic: # data not extracted for club of current goalie
                print("extracting data for %s"% (playerClub))
                actions.send_keys(Keys.ENTER)
                actions.perform() #this is the last step in the simulation of clicking the info button
                applyTimeDelay(5)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, nthGameWeekDifficultySelector % (noGWDifficultiesToExtract))))
                def getGWD(ithWeekAway): return driver.find_element_by_css_selector(nthGameWeekDifficultySelector % (ithWeekAway)).text
                gameweekDifficultyList = [ getGWD(i) for i in range(1,noGWDifficultiesToExtract+1) ] # starts from 1 not 0, due to css selector nth child syntax

                #store {playerClub, gwdList} as {key, Value}
                gameWeekDiffcultiesByClubDic[playerClub] = gameweekDifficultyList
                noClubsCompleted = noClubsCompleted + 1
                actions.send_keys(Keys.ESCAPE) #close pop-up
                actions.perform()
                applyTimeDelay(5)
                print("no clubs compl %d" %(noClubsCompleted))
            #prepare for next player
            row = row +1        
            actions.send_keys(Keys.TAB * 2) # move to next row    
            actions.perform()  
        except Exception:
            driver.save_screenshot("screenshot.png")
            raise 
    print(gameWeekDiffcultiesByClubDic)

def main():
    password = raw_input('Enter your password: ')
    email = raw_input('Enter your login email address: ')
    login(email, password)
    status = getStatus()
    playersMap = updatePlayerData(status.gameweekNo)
    updateDatabaseWithPlayers(playersMap) #updateExcelSheetWithPlayers(playersMap)
    updateCurrentTeam()
    sqlDatabase.connection.close()

def test():
    password = raw_input('Enter your password: ')
    email = raw_input('Enter your login email address: ')
    login(email, password)
    updateCurrentTeam()

if __name__ == '__main__':
    try:
        main()#test()
    finally:
        driver.quit()
    #TODO:
    """
    Improve logging eg. log completion
    segregate related functions into modules
    complete other TODOs
    comply with python best practices
    """