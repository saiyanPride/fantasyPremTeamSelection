## Saved Queries
SELECT Clubs.Name, FIRST_GW, SECOND_GW, THIRD_GW, FOURTH_GW, FIFTH_GW FROM 
GameweekDifficulty LEFT JOIN Clubs
            ON GameweekDifficulty.ClubId = Clubs.ClubId
            
		
SHOW DATABASES
USE fantasyPremierLeague

SELECT * FROM PlayerStats WHERE Position='FWD' ORDER BY AvgScore DESC
SELECT * FROM PlayerStats WHERE Position='MID' ORDER BY AvgScore DESC
SELECT * FROM PlayerStats WHERE Position='DEF' ORDER BY AvgScore DESC

#view outfield players sorted by score
SELECT Name, Form, Goals, Assists, Bonus, FirstGameweekScore, AvgScore FROM PlayerStats WHERE isFirstTeam > 0 AND Position != 'GKP' ORDER BY AvgScore DESC
#view goalies
SELECT Name, Form, Goals, Assists, Bonus, FirstGameweekScore, AvgScore FROM PlayerStats WHERE isFirstTeam > 0 AND Position = 'GKP' ORDER BY AvgScore DESC

#update Gameweek difficulty
DROP TABLE GameweekDifficulty;
CREATE TABLE GameweekDifficulty (
GId int NOT NULL PRIMARY KEY,
ClubId int NOT NULL,
FIRST_GW TINYINT,
SECOND_GW TINYINT,
THIRD_GW TINYINT,
FOURTH_GW TINYINT,
FIFTH_GW TINYINT,
FOREIGN KEY GameweekDifficulty(ClubId)
REFERENCES Clubs(ClubId)
);
SELECT * FROM GameweekDifficulty;

/*GW15 to gw19*/
insert into GameweekDifficulty VALUES (0,0,3,2,4,2,2);
insert into GameweekDifficulty VALUES (1,1,4,5,2,2,3);
insert into GameweekDifficulty VALUES (2,2,2,4,2,4,2);
insert into GameweekDifficulty VALUES (3,3,2,2,2,5,3);
insert into GameweekDifficulty VALUES (4,4,2,2,2,2,3);
insert into GameweekDifficulty VALUES (5,5,3,3,3,3,3);
insert into GameweekDifficulty VALUES (6,6,2,4,2,2,4);
insert into GameweekDifficulty VALUES (7,7,4,2,2,2,4);
insert into GameweekDifficulty VALUES (8,8,2,4,2,4,2);
insert into GameweekDifficulty VALUES (9,9,2,2,4,4,5);
insert into GameweekDifficulty VALUES (10,10,4,2,4,2,2);
insert into GameweekDifficulty VALUES (11,11,3,2,2,2,4);
insert into GameweekDifficulty VALUES (12,12,2,2,2,2,4);
insert into GameweekDifficulty VALUES (13,13,3,5,4,4,2);
insert into GameweekDifficulty VALUES (14,14,2,2,4,4,2);
insert into GameweekDifficulty VALUES (15,15,2,2,5,3,2);
insert into GameweekDifficulty VALUES (16,16,2,4,3,2,2);
insert into GameweekDifficulty VALUES (17,17,4,2,2,4,2);
insert into GameweekDifficulty VALUES (18,18,2,2,2,2,4);
insert into GameweekDifficulty VALUES (19,19,4,3,2,2,2);


SELECT COUNT(Name) FROM PlayerStats
SELECT COUNT(distinct Name) FROM PlayerStats

#determine non-uniue player names
SELECT Name, COUNT(Name) FROM PlayerStats GROUP BY Name HAVING COUNT(Name) > 1
#determine number of players with same name & club
SELECT Name, COUNT(Name) FROM PlayerStats GROUP BY Name,Club HAVING COUNT(Name) > 1

SELECT Name FROM PlayerStats WHERE isFirstTeam > 0
ALTER TABLE PlayerStats ADD isFirstTeam tinyint NOT NULL
UPDATE PlayerStats SET isFirstTeam = 2 WHERE Club ='CHE' AND Name = 'Courtois'