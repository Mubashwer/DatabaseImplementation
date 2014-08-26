CREATE TABLE Game(
    GameID                  smallint       auto_increment, 
    Genre                   varchar(50),
    Review                  text,
    StarRating              smallint,
    ClassificationRating    varchar(5),
    PlatformNotes           text,
    PromotionLink           varchar(50),
    Cost                    decimal(5,2),      
    PRIMARY KEY(GameID)
) ENGINE=InnoDB;
    
CREATE TABLE Video {
    VideoID         smallint       auto_increment,
    URL             varchar(50)    NOT_NULL,
    Price           decimal(5,2),
    VideoType       varchar(45),
    InstanceRunID   smallint       NOT_NULL,
    GameID          smallint       NOT_NULL,
    PRIMARY KEY(AccountID),
    FOREIGN KEY (InstanceRunID) REFERENCES (InstanceRun)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (GameID) REFERENCES (Game)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
} ENGINE=InnoDB;

CREATE TABLE InstanceRun {
    InstanceRunID         smallint       auto_increment,
    SupervisorID          smallint       NOT_NULL,
    Name                  varchar(45),
    RecordedTime          DATETIME,
    CategoryName          varchar(50),
    PRIMARY KEY(InstanceRunID),
    FOREIGN KEY (SupervisorID) REFERENCES (Player)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
} ENGINE=InnoDB;

CREATE TABLE Achievement {
    AchievementID         smallint       auto_increment,
    InstanceRunID         smallint       NOT_NULL,
    WhenAchieved          DATETIME
    Name                  varchar(45),
    RewardBody            varchar(45),
    PRIMARY KEY(AchievementID, InstanceRunID),
    FOREIGN KEY (InstanceRunID) REFERENCES (InstanceRun)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
} ENGINE=InnoDB;


