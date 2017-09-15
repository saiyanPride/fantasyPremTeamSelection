from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from customDataStructures import Status
from customDataStructures import PlayerData
from pprint import pprint
from itertools import izip
import sqlDatabase

#driver = webdriver.Firefox(executable_path=r'/Users/NiranPyzzle/Downloads/geckodriver')
driver = webdriver.PhantomJS(
    executable_path=r'/Users/NiranPyzzle/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')
driver.get("https://fantasy.premierleague.com/")
wait = WebDriverWait(driver, 10)
waitIntervalForStatisticsPageChange_secs = 1
minNoPlayerPerPage = 16
gameweekNo = 0
# css selectors
lastPageAnchorElementSelector = '#ismr-main > div > div.paginationContainer.ism-pagination > \
                    a.paginationBtn.ismjs-change-page.ism-pagination__button.ism-pagination__button--secondary'  # it's href attribute has the number of pages href='#17'
usernameInputElementSelector = "#ismjs-username"
passwordInputElementSelector = '#ismjs-password'
benchBoostButtonSelector = '#ismr-chips > ul > li:nth-child(1) > div > button'
freehitButtonSelector = '#ismr-chips > ul > li:nth-child(2) > div > button'
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

# playerGoalsSelectorTemplate
# playerAssistsSelectorTemplate
# playerBonusSelectorTemplate
# urls
transfersPageUrl = "https://fantasy.premierleague.com/a/squad/transfers"
minutesPlayedStatisticsPageUrl = "https://fantasy.premierleague.com/a/statistics/minutes"
goalsScoredStatisticsPageUrl = "https://fantasy.premierleague.com/a/statistics/goals_scored"
assistsStatisticsPageUrl = "https://fantasy.premierleague.com/a/statistics/assists"
bonusStatisticsPageUrl = "https://fantasy.premierleague.com/a/statistics/bonus"
cleanSheetsStatisticsPageUrl = "https://fantasy.premierleague.com/a/statistics/clean_sheets"


def login(username, password):
    # TODO: make sure arguments are strings
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

    for index, selector in enumerate(cssSelectors):
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
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        elem = driver.find_element_by_css_selector(selector)
        text = elem.text
        retrievedText.insert(index, text)

    noFreeTransfers = int(retrievedText[0])
    # TODO: simplify
    bankBalance = ((float(retrievedText[1][1:]) * 10) // 1) / 10
    wildCardAvailable = False
    if retrievedText[2] == 'Play Wildcard':
        wildCardAvailable = True
    gameweekNo = int(retrievedText[3][9])

    # use retrieved information to instantiate status object
    result = "noFreeTransfers: %s \nbankBalance GBP: %f \nGameweek number: %s" % (
        noFreeTransfers, bankBalance, gameweekNo)
    print (result)
    if (wildCardAvailable):
        print "Wild card is available"

    return Status(wildCardAvailable, freehitAvailable, tripleCaptainAvailable, benchBoostAvailable, noFreeTransfers, bankBalance, gameweekNo)


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

    print("extracting data from minutes played page")  # DEbug
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

    print("Extracting data from other pages")  # debug
    # Extract goals scored, assists, bonus, clean sheets
    for pageUrl, playerDataUpdateFunction in izip(pageTypeUrls, playerDataUpdateFunctions):
        driver.get(pageUrl)
        for pageNo in range(totalNumberOfPages):
            print("*** page %s" % (pageNo))  # DEBUG
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


def updatePlayerScores(playersMap, gameweekNo):
    print("****updating player scores")  # DEBUG
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


def updateDatabaseWithPlayers(playersMap):
    sqlDatabase.cursor.execute("DROP TABLE Player")
    sqlDatabase.cursor.execute("CREATE TABLE Player (\
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
        FifthGameweekScore float \
        )")
    id = -1
    for key, player in playersMap.items():
        id += 1
        scores = player.gameweekScores
        firstGwScore = scores[0]
        secondGwScore = scores[1]
        thirdGwScore = scores[2]
        fourthGwScore = scores[3]
        fifthGwScore = scores[4]
        sqlDatabase.cursor.execute("INSERT INTO Player VALUES (%d,'%s','%s','%s',%f,%f,%d,%d,%d,%d,%d,%f,%f,%f,%f,%f)"
                                   % (id, player.club, player.name, player.position, player.value, player.form, player.minutesPlayed, player.goals, player.assists, player.bonus, player.cleansheets,
                                      firstGwScore, secondGwScore, thirdGwScore, fourthGwScore, fifthGwScore))
        sqlDatabase.connection.commit()


def main():
    password = raw_input('Enter your password: ')
    login("niranfor1@hotmail.com", password)
    status = getStatus()
    playersMap = updatePlayerData(status.gameweekNo)
    updateDatabaseWithPlayers(playersMap)
    sqlDatabase.connection.close()


if __name__ == '__main__':
    main()
