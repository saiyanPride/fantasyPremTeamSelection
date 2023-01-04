# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from customDataStructures import Status
from customDataStructures import PlayerData

from xlrd import open_workbook
from pprint import pprint
from itertools import izip
from configurationConstants import *
from utility import *

import time
import datetime
import xlsxwriter
import sqlDatabase


def main():
    driver.get(fantasyPremierLeagueBaseUrl)
    password = raw_input('Enter your password: ')
    email = raw_input('Enter your login email address: ')
    login(email, password)
    # nebug: above this line should be deleted
    status = getStatus() # NEBUG: should be API call
    playersMap = predictPlayerScores(status.gameweekNo)
    updateDatabaseWithPlayers(playersMap)
    updateCurrentTeam()
    sqlDatabase.connection.close()


def test():
    password = raw_input('Enter your password: ')
    email = raw_input('Enter your login email address: ')
    login(email, password)
    updateCurrentTeam()

# data extraction and storage related functions


def login(username, password):
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


def getPlayerNameAndClub(i, resultStore, flag):
    """
    Extracts the name & club of the ith player and represents it in the form: "<PlayerName>;<Club>"
    i: refers to the integer id of the focus player
    resultStore: data structure where player details will be stored
    flag: use 1 if player is a starter & 2 if player is a substitute
    """
    # wait for presence of player name element selectors
    playerNameSelector = ithPlayerInCurrentTeamNameSelector % (flag, i)
    clubNameSelector = ithPlayerInCurrentTeamClubShortNameSelector % (
        flag, i)
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, playerNameSelector)))
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, clubNameSelector)))
    # extract name
    playerName = driver.find_element_by_css_selector(
        playerNameSelector).text
    clubShortName = driver.find_element_by_css_selector(
        clubNameSelector).text
    resultStore.append(playerName + ';' + clubShortName)


def getStatusFromTransfersPage(statusSelectors):
    """
    Navigate to transfers page, retrieve status and return tuple of the form
    (noFreeTransfers, bankBalance, wildCardAvailable, gameweekNo)
    """
    driver.get(transfersPageUrl)
    retrievedText = []

    for index, selector in enumerate(statusSelectors):
        try:
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, selector)))
            elem = driver.find_element_by_css_selector(selector)
            text = elem.text
            retrievedText.insert(index, text)
        except:
            if selector == wildCardAvailabilityElementSelector:
                retrievedText.insert(index, "unavailable")
            else:
                raise

    noFreeTransfers = int(retrievedText[0])
    bankBalance = ((float(retrievedText[1][1:]) * 10) // 1) / 10
    wildCardAvailable = retrievedText[2] == 'Play Wildcard'
    # TODO: make generic so that it works if gameweek is single digit or double digit, could use the expected size of the string to deduce
    gameweekNo = int(retrievedText[3][9:11])

    return (noFreeTransfers, bankBalance, wildCardAvailable, gameweekNo)


def getPlayerDataFromMinutesPlayedViewOfStatisticsPage(playerDataMap):
    """
    Extract data from statistics page view obtained by sorting data by `minutes played`
    Extracted data: name, club, position, cost, form and minutes played
    """
    for pageNo in range(totalNumberOfPages):
        if pageNo == lastPage:
            # allow extra time for other rows to load
            driver.implicitly_wait(waitIntervalForStatisticsPageChange_secs)
        else:
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, playerMinutesPlayedSelectorTemplate % (
                    minNoPlayerPerPage))))  # wait for data in table to appear in each iteration
            except TimeoutException:
                warn(
                    "timed out in page %s of stats, now applying extra time delay" % (pageNo))
                driver.implicitly_wait(
                    waitIntervalForStatisticsPageChange_secs)
        tbodyElem = driver.find_element_by_css_selector(
            playerStatisticsTbodyElementSelector)

        # determine the number of players on the page i.e. the no of child <tr> tags of the table's <tbody> tag
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

                # instantiate & store Player object in dictionary
                key = playerName + playerClub + playerPosition
                playerDataMap[key] = PlayerData(
                    playerClub, playerName, playerPosition, playerCost, playerForm, playerMinutesPlayed)
            except:
                error("issue with row %s of page %s" %
                      (playerDataRow, pageNo))
        if pageNo != lastPage:  # click on next page button if not on last page
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, playerStatisticsNextPageButtonSelector)))
            driver.find_element_by_css_selector(
                playerStatisticsNextPageButtonSelector).click()  # go to next page
    info("Data extraction from minutes played view of statistics page complete")


def getDataFromStatisticPageView(pageUrl, playerDataUpdateFunction, playerDataMap):
    """
    Navigates to  `pageUrl` and extracts the data of interest e.g. goals scored by each player
    Every player in playerDataMap, is then updated to reflect the extracted data
    """
    driver.get(pageUrl)
    for pageNo in range(totalNumberOfPages):
        # wait for page `pageNo` to finish loading
        if pageNo == lastPage:  # allow extra time for other rows to load
            driver.implicitly_wait(
                waitIntervalForStatisticsPageChange_secs)
        else:
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, fifthColumnValueSelectorTemplate % (
                    minNoPlayerPerPage))))  # wait for data in table to appear in each iteration
            except TimeoutException:
                warn("timed out in page %s of stats, now applying time delay" % (pageNo))
                driver.implicitly_wait(
                    waitIntervalForStatisticsPageChange_secs)
        tbodyElem = driver.find_element_by_css_selector(
            playerStatisticsTbodyElementSelector)
        numberOfPlayersOnPage = tbodyElem.get_property('childElementCount')

        # loop through each row in the statistics table and update relevant page data for corresponding player
        for playerDataRow in range(1, numberOfPlayersOnPage + 1):
            playerName = driver.find_element_by_css_selector(
                playerNameSelectorTemplate % (playerDataRow)).text
            playerPosition = driver.find_element_by_css_selector(
                playerPositionSelectorTemplate % (playerDataRow)).text
            playerClub = driver.find_element_by_css_selector(
                playerClubSelectorTemplate % (playerDataRow)).text
            key = playerName + playerClub + playerPosition
            extractedData = driver.find_element_by_css_selector(
                fifthColumnValueSelectorTemplate % (playerDataRow)).text  # the data of interest is in the 5th column
            # update corresponding player object with extracted data
            playerDataUpdateFunction(playerDataMap[key], extractedData)
        if pageNo != lastPage:
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, playerStatisticsNextPageButtonSelector)))
            driver.find_element_by_css_selector(
                playerStatisticsNextPageButtonSelector).click()  # go to next page


def getStatus():
    chipAvailability = [False, False, False]
    cssSelectors = [benchBoostButtonSelector,
                    freehitButtonSelector, tripleCaptainButtonSelector]

    driver.get(myTeamUrl)  # Navigate to MyTeam page

    # determine the status of these chips: 1) BenchBoost, 2) Free hit, 3) Triple Captain
    for index, selector in enumerate(cssSelectors):
        info("waiting for presence of benchboost/freehit/triple captain button")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        elem = driver.find_element_by_css_selector(selector)
        chipAction = elem.text
        if chipAction == 'PLAY':
            chipAvailability[index] = True

    statusSet1 = (benchBoostAvailable, freehitAvailable,
                  tripleCaptainAvailable) = chipAvailability
    chipStatusMessage = "benchBoostAvailable:%r \nfreehitAvailable: %r \ntripleCaptainAvailable:%r" % statusSet1
    info(chipStatusMessage)

    # Navigate to transfers page and determine status of: 1) Free transfers, 2) Bank balance, 3) Wild card, 4) Gameweek number
    otherStatusSelectors = [noFreeTransfersElementSelector,
                            bankBalanceElementSelector,
                            wildCardAvailabilityElementSelector,
                            gameweekNumberElementSelector]
    statusSet2 = (noFreeTransfers, bankBalance, wildCardAvailable,
                  gameweekNo) = getStatusFromTransfersPage(otherStatusSelectors)
    # use retrieved information to instantiate `Status` object
    chipStatusMessage = "noFreeTransfers: %s \nbankBalance GBP: %f \wildCardAvailable:%r \nGameweek number: %s" % statusSet2
    info(chipStatusMessage)

    # write status result to json file
    statusJson = Status(wildCardAvailable, freehitAvailable, tripleCaptainAvailable,
                        benchBoostAvailable, noFreeTransfers, bankBalance, gameweekNo).getJson()
    writeToFile('status.json', statusJson)
    return status #NEBUG: delete this line


def getPlayerStatistics(playerDataMap):
    """
    Extract latest player data from fantasy premier league statistics pages
    """
    driver.get(minutesPlayedStatisticsPageUrl)
    # determine number of player statistic pages
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, lastPageAnchorElementSelector)))
    numberPlayerStatisticPagesElem = driver.find_element_by_css_selector(
        lastPageAnchorElementSelector)
    totalNumberOfPages = int((numberPlayerStatisticPagesElem.get_attribute(
        'href')[PAGE_NUM_START_INDEX_IN_STATISTICS_PAGE_URL:]))
    lastPage = totalNumberOfPages - 1  # 0 indexed for use in loop

    getPlayerDataFromMinutesPlayedViewOfStatisticsPage(playerDataMap)

    # functions for updating player objects with extracted data from statistics page
    def updateGoals(Player, goals): Player.goals = int(goals)

    def updateAssists(Player, assists): Player.assists = int(assists)

    def updateBonus(Player, bonus): Player.bonus = int(bonus)

    def updateCleanSheets(
        Player, cleansheets): Player.cleansheets = int(cleansheets)

    info("Extracting data (goals scored, assists, bonus, clean sheets) from relevant views of the statistics page")
    getDataFromStatisticPageView(
        goalsScoredStatisticsPageUrl, updateGoals, playerDataMap)
    getDataFromStatisticPageView(
        assistsStatisticsPageUrl, updateAssists, playerDataMap)
    getDataFromStatisticPageView(
        bonusStatisticsPageUrl, updateBonus, playerDataMap)
    getDataFromStatisticPageView(
        cleanSheetsStatisticsPageUrl, updateCleanSheets, playerDataMap)
    info("goals scored, assists, bonus, clean sheets data extraction complete ")


def predictPlayerScores(gameweekNo):
    """
    Extract latest player data from fantasy premier league statistics pages then
    predict player scores for `gameweekNo` and return dictionary of player objects
    """
    playerDataMap = {}  # key is playerName-Club-Position, value is Player object
    getPlayerStatistics(playerDataMap) #NEBUG: replace with API call
    calculatePlayerScores(playerDataMap, gameweekNo)
    return playerDataMap


def calculatePlayerScores(playersMap, gameweekNo):
    """
    predict player scores for `gameweekNo`
    """
    info("updating player scores")
    gameweekDifficultyByClubMap = {}

    # query database for gameweek difficulties
    sqlDatabase.cursor.execute(GET_GAMEWEEK_DIFFICULTIES_SQL)
    row = sqlDatabase.cursor.fetchone()

    # store the gameweek difficulties (for the next 5 matches) for each club in a list
    while row:
        gameWeekDifficultiesForClub = row[1:6]
        gameweekDifficultyByClubMap[str(row[0])] = gameWeekDifficultiesForClub
        row = sqlDatabase.cursor.fetchone()

    # calculate/estimate player scores
    for key, player in playersMap.items():
        player.getGameweekScoreEstimates(
            gameweekDifficultyByClubMap[player.club], gameweekNo)


def assignSquadStatusFlagInDB(playerList, flag):
    """
    Set's the `isFirstTeam` column in `Players` table to `flag`
    flag:  possible values are in the range [0,1,2]
        0 -> player not in team
        1 -> player in starting lineup
        2 -> player is a subsitute
    """
    for element in playerList:
        playerData = element.split(";")
        sqlStatement = markPlayerAsCurrentlySelectedSQLTemplate % (
            flag, playerData[0], playerData[1])
        sqlDatabase.cursor.execute(sqlStatement)


def updateCurrentTeam():
    """
    Determine current members of your team, and update the datastore (database) to reflect this
    """
    startingLineup = []  # will consist of string representations of the starting lineup e.g. "<PlayerName>;<Club>"
    # will consist of string representations of the substitutes e.g. "<PlayerName>;<Club>"
    substitutes = []
    info("updating current team")

    # validate current page is the "team page"
    if driver.current_url != myTeamUrl:
        driver.get(myTeamUrl)

    # switch to list view so that user's player's clubs are visible
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, listViewButtonSelector)))
    listViewButton = driver.find_element_by_css_selector(
        listViewButtonSelector)
    listViewButton.click()

    info("Determining starting lineup and substitutes")
    for i in range(1, noStartingPlayers + 1):
        getPlayerNameAndClub(i, startingLineup, STARTER_SECTION)

    for i in range(1, noSubs + 1):
        getPlayerNameAndClub(i, substitutes, SUBSTITUTE_SECTION)

    sqlDatabase.cursor.execute(addNewColumnSQL)

    info("Updating database to reflect current members of team")
    # mark first team with flag of 2
    assignSquadStatusFlagInDB(startingLineup, STARTER)
    assignSquadStatusFlagInDB(substitutes, SUBSTITUTE)
    sqlDatabase.connection.commit()


def updateDatabaseWithPlayers(playersMap):
    # TODO: make the database connection comply with RAII pattern
    sqlDatabase.cursor.execute(DROP_PLAYERSTATS_TABLE_SQL)
    sqlDatabase.cursor.execute(CREATE_PLAYERSTATS_TABLE_SQL)
    id = -1
    for key, player in playersMap.items():
        id += 1
        scores = player.gameweekScores
        firstGwScore = scores[0]
        secondGwScore = scores[1]
        thirdGwScore = scores[2]
        fourthGwScore = scores[3]
        fifthGwScore = scores[4]
        avgScore = sum(scores) / len(scores)
        sqlDatabase.cursor.execute("INSERT INTO PlayerStats VALUES (%d,'%s','%s','%s',%f,%f,%d,%d,%d,%d,%d,%f,%f,%f,%f,%f,%f)"
                                   % (id, player.club, player.name, player.position, player.value, player.form, player.minutesPlayed, player.goals, player.assists, player.bonus, player.cleansheets,
                                      firstGwScore, secondGwScore, thirdGwScore, fourthGwScore, fifthGwScore, avgScore))
        sqlDatabase.connection.commit()


if __name__ == '__main__':
    try:
        main()  # test()
    finally:
        driver.quit()
