CREATE TABLE Clubs (
ClubId int NOT NULL PRIMARY KEY,
Name varchar(255)
);

insert into Clubs (ClubId, Name) VALUES (0, 'HUD');
insert into Clubs (ClubId, Name) VALUES (1, 'MUN');
insert into Clubs (ClubId, Name) VALUES (2, 'SOU');
insert into Clubs (ClubId, Name) VALUES (3, 'TOT');
insert into Clubs (ClubId, Name) VALUES (4, 'CHE');
insert into Clubs (ClubId, Name) VALUES (5, 'CRY');
insert into Clubs (ClubId, Name) VALUES (6, 'EVE');
insert into Clubs (ClubId, Name) VALUES (7, 'ARS');
insert into Clubs (ClubId, Name) VALUES (8, 'MCI');
insert into Clubs (ClubId, Name) VALUES (9, 'BOU');
insert into Clubs (ClubId, Name) VALUES (10, 'BHA');
insert into Clubs (ClubId, Name) VALUES (11, 'BUR');
insert into Clubs (ClubId, Name) VALUES (12, 'LIV');
insert into Clubs (ClubId, Name) VALUES (13, 'WHU');
insert into Clubs (ClubId, Name) VALUES (14, 'WBA');
insert into Clubs (ClubId, Name) VALUES (15, 'SWA');
insert into Clubs (ClubId, Name) VALUES (16, 'STK');
insert into Clubs (ClubId, Name) VALUES (17, 'NEW');
insert into Clubs (ClubId, Name) VALUES (18, 'LEI');
insert into Clubs (ClubId, Name) VALUES (19, 'WAT');

SELECT * FROM Clubs;


/*Gameweek Difficulty*/

DROP TABLE GameweekDifficulty;
CREATE TABLE GameweekDifficulty (
GId int NOT NULL PRIMARY KEY,
ClubId int NOT NULL FOREIGN KEY REFERENCES Clubs(ClubId),
FIRST_GW TINYINT,
SECOND_GW TINYINT,
THIRD_GW TINYINT,
FOURTH_GW TINYINT,
FIFTH_GW TINYINT
);
SELECT * FROM GameweekDifficulty;

/*GW7 to gw11*/
insert into GameweekDifficulty VALUES (0,0, 4,2,4,4,2);
insert into GameweekDifficulty VALUES (1,1, 2,4,2,4,5);
insert into GameweekDifficulty VALUES (2,2, 2,2,2,2,2);
insert into GameweekDifficulty VALUES (3,3, 2,2,4,4,2);
insert into GameweekDifficulty VALUES (4,4, 4,2,2,2,4);
insert into GameweekDifficulty VALUES (5,5, 4,4,2,2,4);
insert into GameweekDifficulty VALUES (6,6, 2,2,4,3,2);
insert into GameweekDifficulty VALUES (7,7, 1,2,4,2,4);
insert into GameweekDifficulty VALUES (8,8, 5,2,2,2,4);
insert into GameweekDifficulty VALUES (9,9, 2,4,2,4,2);
insert into GameweekDifficulty VALUES (10,10, 4,3,2,2,2);
insert into GameweekDifficulty VALUES (11,11, 4,2,4,2,3);
insert into GameweekDifficulty VALUES (12,12, 2,4,4,2,2);
insert into GameweekDifficulty VALUES (13,13, 2,3,1,2,4);
insert into GameweekDifficulty VALUES (14,14, 2,3,3,4,2);
insert into GameweekDifficulty VALUES (15,15, 2,2,2,4,1);
insert into GameweekDifficulty VALUES (16,16, 2,4,2,2,2);
insert into GameweekDifficulty VALUES (17,17, 4,3,2,3,2);
insert into GameweekDifficulty VALUES (18,18, 2,2,2,3,2);
insert into GameweekDifficulty VALUES (19,19, 2,4,5,2,4);

#Query to view gameweek difficulties of clubs
SELECT Clubs.Name, FIRST_GW, SECOND_GW, THIRD_GW, FOURTH_GW, FIFTH_GW FROM 
GameweekDifficulty LEFT JOIN Clubs
ON GameweekDifficulty.ClubId = Clubs.ClubId